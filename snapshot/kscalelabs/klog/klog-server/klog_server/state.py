from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Callable
from datetime import datetime as dt
import time
import logging
import colorlogging
import threading

# Set up logger for this module
logger = logging.getLogger(__name__)
colorlogging.configure(
    logger=logger,
    remove_existing_handlers=True,
    hide_if_not_interactive=False,
    level=logging.DEBUG,
)

# Type aliases
RunId = str
RobotId = str
DevId = str

# State enums
class CollectionState(Enum):
    starting = "starting"
    collecting = "collecting"
    done = "done"
    failed = "failed"

class SyncState(Enum):
    syncing = "syncing"
    paused = "paused"
    done = "done"
    failed = "failed"

class KlogDeviceType(Enum):
    kbot = "klog-kbot"
    cam = "klog-cam"
    unknown = "unknown"

class KlogDeviceStatus(Enum):
    online = "online"
    offline = "offline"

class RunState(Enum):
    running = "running"
    syncing = "syncing"
    processing = "processing"
    done = "done"

# Custom types for states
@dataclass
class KlogDevice:
    dev_id: DevId
    dev_type: KlogDeviceType
    status: KlogDeviceStatus
    last_update: float = field(default_factory=time.time)

    # should always be set after first collection
    collection_state: Optional[CollectionState] = None
    sync_state: Optional[SyncState] = None

    description: Optional[str] = None
    disconnect_type: Optional[str] = None
    collection_run: Optional[RunId] = None
    collection_failure_type: Optional[str] = None
    sync_run: Optional[RunId] = None
    sync_failure_type: Optional[str] = None

@dataclass
class Run:
    run_id: RunId
    state: RunState
    robot: DevId
    start_time: dt
    log_devices: list[DevId]

# The beast
@dataclass
class GlobalState:
    runs: dict[RunId, Run] = field(default_factory=dict)
    devices: dict[DevId, KlogDevice] = field(default_factory=dict)

    _send_all_ready: Optional[Callable[[RunId], None]] = None
    _send_stop_run: Optional[Callable[[RunId], None]] = None
    _postprocess: Optional[Callable[[RunId], None]] = None
    _send_registered: Optional[Callable[[DevId], None]] = None

    _device_timeout: float = 20.0 # seconds
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False, compare=False)

    # This is to avoid circular imports, there's likely a better way
    def set_callbacks(self, send_all_ready: Callable[[RunId], None], send_stop_run: Callable[[RunId], None],
                      postprocess: Callable[[RunId], None], send_registered: Optional[Callable[[DevId], None]] = None):
        self._send_all_ready = send_all_ready
        self._send_stop_run = send_stop_run
        self._postprocess = postprocess
        self._send_registered = send_registered

    # Runs are deleted from the state when finished processing
    def run_done(self, run_id: RunId):
        logger.info(f"[RUN_DONE] Run {run_id} done processing.")
        with self.lock:
            del self.runs[run_id]

    # async function to wait for all devices to be collecting data on a given run, and send the all_ready message when
    # they are
    def _wait_for_devices_collecting(self, run_id: RunId):
        start_time = time.time()
        while time.time() - start_time < self._device_timeout:
            with self.lock:
                if self.runs[run_id].state != RunState.running:
                    # Run stopped
                    break
                devices_left = [dev_id for dev_id in self.runs[run_id].log_devices
                                if self.devices[dev_id].collection_state != CollectionState.collecting
                                and self.devices[dev_id].status == KlogDeviceStatus.online]
            if not devices_left:
                self._send_all_ready(run_id)
                break
            time.sleep(0.2)
        else: # timed out
            logger.warning(f"[WAIT_FOR_DEVICES] Timeout waiting for devices to collect data for run {run_id}. "
                           f"Devices left: {devices_left}")

    def start_run(self, run_id: RunId, robot: RobotId):
        # error if trying to start a run that already exists
        if run_id in self.runs:
            logger.warning(f"[RUN] Run {run_id} already exists, not starting a new one.")
            return

        online_devs = [dev_id for dev_id, dev in self.devices.items() if dev.status == KlogDeviceStatus.online]
        logger.info(f"[RUN] Starting run {run_id} with robot {robot} and devices: {online_devs}")
        self.runs[run_id] = Run(
            run_id=run_id,
            state=RunState.running,
            robot=robot,
            start_time=dt.now(),
            log_devices=online_devs
        )
        t = threading.Thread(target=self._wait_for_devices_collecting, args=(run_id,))
        t.start()

    def stop_run(self, run_id: RunId):
        if run_id not in self.runs:
            logger.debug(f"[STOP_RUN] Attempted to stop unknown run {run_id}.")
            return
        elif self.runs[run_id].state != RunState.running:
            logger.debug(f"[STOP_RUN] Attempted to stop run {run_id} that is not running. Current state: {self.runs[run_id].state.value}.")
            return

        logger.info(f"[STOP_RUN] Stopping run {run_id}.")
        with self.lock:
            self.runs[run_id].state = RunState.syncing
        return

    def update_sync_state(self, dev_id: DevId, state: SyncState, run_id: RunId, failure_type: Optional[str] = None):
        if dev_id in self.devices:
            with self.lock:
                self.devices[dev_id].sync_state = state
                self.devices[dev_id].sync_run = run_id
                self.devices[dev_id].sync_failure_type = failure_type
                self.devices[dev_id].last_update = time.time()
        else:
            logger.debug(f"[UPDATE_SYNC_STATE] Sync state update for unregistered device {dev_id}.")

        # Expected behavior: known device, known run
        match state:
            case SyncState.failed:
                logger.warning(f"[UPDATE_SYNC_STATE] {dev_id} sync failed for run {run_id}. Failure type: {failure_type}.")
            case SyncState.paused:
                logger.debug(f"[UPDATE_SYNC_STATE] {dev_id} paused run {run_id}.")
            case SyncState.syncing:
                logger.debug(f"[UPDATE_SYNC_STATE] {dev_id} syncing run {run_id}.")
            case SyncState.done:
                logger.info(f"[UPDATE_SYNC_STATE] {dev_id} done syncing run {run_id}.")
                if run_id in self.runs:
                    # TODO call this device's decoder in another thread
                    if all(self.devices[d].sync_state == SyncState.done for d in self.runs[run_id].log_devices):
                            self.runs[run_id].state = RunState.processing
                            logger.info(f"[UPDATE_SYNC_STATE] All devices done syncing for run {run_id}. Starting postprocessing.")
                            self._postprocess(run_id)
                else:
                    logger.warning(f"[UPDATE_SYNC_STATE] {dev_id} done syncing unkown run {run_id}.")
                    threading.Thread(target=self._postprocess, args=(run_id,)).start()
                    # This really shouldn't happen because the server should know about all runs,
                    # but if it does we still want to process the run
        return

    def update_collection_state(self, dev_id: DevId, state: CollectionState, run_id: RunId, failure_type: Optional[str] = None):
        if run_id not in self.runs:
            logger.debug(f"[UPDATE_COLLECTION_STATE] Collection state update for unknown run id {run_id} for device {dev_id}.")
            return

        if dev_id not in self.devices:
            logger.debug(f"[UPDATE_COLLECTION_STATE] Collection state update for unregistered device {dev_id}.")
            return

        with self.lock:
            self.devices[dev_id].collection_state = state
            self.devices[dev_id].collection_run = run_id
            self.devices[dev_id].collection_failure_type = failure_type
            self.devices[dev_id].last_update = time.time()

        match state:
            case CollectionState.failed:
                logger.warning(f"[UPDATE_COLLECTION_STATE] {dev_id} collection failed for run {run_id}. Failure type: {failure_type}.")
            case CollectionState.collecting:
                logger.info(f"[UPDATE_COLLECTION_STATE] {dev_id} started collecting data for run {run_id}.")
            case CollectionState.starting:
                logger.info(f"[UPDATE_COLLECTION_STATE] {dev_id} is starting collection for run {run_id}.")
            case CollectionState.done:
                logger.info(f"[UPDATE_COLLECTION_STATE] {dev_id} done collecting for run {run_id}.")
        return

    def update_status(self, dev_id: DevId, status: KlogDeviceStatus, disconnect_type: Optional[str] = None):
        if status == KlogDeviceStatus.online:
            if dev_id in self.devices:
                # Expected behavior: known device coming back online
                if not self.devices[dev_id].status == KlogDeviceStatus.online:
                    with self.lock:
                        self.devices[dev_id].status = status
                        self.devices[dev_id].last_update = time.time()
                    logger.info(f"[UPDATE_STATUS] Device {dev_id} is back online.")
                else:
                    logger.debug(f"[UPDATE_STATUS] Device {dev_id} is already online.")
            else:
                logger.debug(f"[UPDATE_STATUS] Unregistered device {dev_id} is online.")
                return

        else:
            if dev_id in self.devices:
                # If you lost a robot, stop the run. If you lost a device, just log it.
                for run_id, run in list(self.runs.items()):
                    if run.state == RunState.running:
                        if run.robot == dev_id:
                            logger.warning(f"[UPDATE_STATUS] Robot for run {run_id} went offline. Stopping run. "
                                        f"Disconnect type: {disconnect_type}")
                            self._send_stop_run(run_id)
                        elif dev_id in run.log_devices:
                            logger.warning(f"[UPDATE_STATUS] Device {dev_id} went offline during run {run_id}. "
                                           f"Disconnect type: {disconnect_type}")
                logger.info(f"[UPDATE_STATUS] Device {dev_id} is now offline. Disconnect type: {disconnect_type}")
                with self.lock:
                    self.devices[dev_id].status = status
                    self.devices[dev_id].disconnect_type = disconnect_type
                    self.devices[dev_id].last_update = time.time()
            else: logger.debug(f"[UPDATE_STATUS] Unregistered device {dev_id} has gone offline.")

    def register_device(self, dev_id: DevId, dev_type: KlogDeviceType, description: Optional[str] = None):
        if dev_id in self.devices:
            logger.debug(f"[REGISTER_DEVICE] Device {dev_id} already registered. Re-registering.")

        logger.info(f"[REGISTER_DEVICE] Registering new device {dev_id} of type {dev_type.value}.")
        with self.lock:
            self.devices[dev_id] = KlogDevice(
                dev_id=dev_id,
                dev_type=dev_type,
                status=KlogDeviceStatus.online,
                description=description
            )
        self._send_registered(dev_id)

