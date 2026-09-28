import asyncio
from dataclasses import dataclass
from typing import Any

from .port_handler import PortHandler
from .protocol_packet_handler import ProtocolPacketHandler
from .sms_sts import SMS_STS


def _degrees_to_ticks(position_deg: float) -> int:
    """Map degrees to raw ticks with 0° at mechanical center.

    Convention:
    - 0° -> 2048 ticks
    - -180° -> 0 ticks
    - +180° -> 4095 ticks
    Values outside [-180, 180] are wrapped then clamped to ticks range.
    """
    # Wrap to [-180, 180)
    wrapped = ((position_deg + 180.0) % 360.0) - 180.0
    ticks_float = 2048.0 + wrapped * (4096.0 / 360.0)
    ticks = int(round(ticks_float))
    if ticks < 0:
        ticks = 0
    if ticks > 4095:
        ticks = 4095
    return ticks


def _ticks_to_degrees(position_ticks: int | None) -> float | None:
    """Map raw ticks to degrees with 0° at 2048 ticks.

    Returns degrees in [-180, 180).
    """
    if position_ticks is None:
        return None
    wrapped = float(position_ticks) - 2048.0
    deg = wrapped * (360.0 / 4096.0)
    # Normalize to [-180, 180)
    deg = ((deg + 180.0) % 360.0) - 180.0
    return deg


@dataclass
class ActuatorState:
    actuator_id: int
    position_deg: float | None = None


@dataclass
class ActuatorsStateResponse:
    states: list[ActuatorState]


class FeetechActuatorService:
    def __init__(self, sms: SMS_STS, actuator_ids: list[int], auto_torque: bool = True):
        self._sms = sms
        self._actuator_ids = actuator_ids
        self._auto_torque = auto_torque
        self._torque_enabled_for: set[int] = set()
        # Cache last sent ticks per actuator for duplicate suppression
        self._last_sent_ticks: dict[int, int] = {}
        self._last_sent_speed: dict[int, int] = {}

    async def get_actuators_state(self) -> ActuatorsStateResponse:
        async def ping_one(sid: int) -> int | None:
            def _ping_blocking() -> bool:
                ok, _ = self._sms.ping(sid)
                return ok

            ok = await asyncio.to_thread(_ping_blocking)
            return sid if ok else None

        results = await asyncio.gather(*[ping_one(s) for s in self._actuator_ids])
        valid_ids = [sid for sid in results if sid is not None]
        return ActuatorsStateResponse(states=[ActuatorState(actuator_id=sid) for sid in valid_ids])

    async def command_actuators(self, commands: list[dict[str, Any]]) -> None:
        # Build move set: id -> (pos_ticks, time_ms, speed)
        moves: dict[int, tuple[int, int, int]] = {}
        ids_to_enable: set[int] = set()

        for cmd in commands:
            sid = int(cmd["actuator_id"])  # required
            pos_deg = float(cmd.get("position", 0.0))
            time_ms = int(cmd.get("time_ms", 0))
            # Accept both "speed" and "velocity" (alias) for compatibility
            if "speed" in cmd:
                speed = int(cmd.get("speed", 0))
            else:
                speed = int(cmd.get("velocity", 0))

            pos_ticks = _degrees_to_ticks(pos_deg)

            # Duplicate suppression: only include if changed vs last sent
            if self._last_sent_ticks.get(sid) != pos_ticks or self._last_sent_speed.get(sid) != speed:
                moves[sid] = (pos_ticks, time_ms, speed)

            if self._auto_torque and sid not in self._torque_enabled_for:
                ids_to_enable.add(sid)

        def _do_blocking():
            for sid in ids_to_enable:
                self._sms.enable_torque(sid, True)
                self._torque_enabled_for.add(sid)
            if moves:
                self._sms.sync_write_positions(moves)
                # Update caches after successful send
                for sid, (pos_ticks, _t, speed) in moves.items():
                    self._last_sent_ticks[sid] = pos_ticks
                    self._last_sent_speed[sid] = speed

        await asyncio.to_thread(_do_blocking)

    async def configure_actuator(self, actuator_id: int, *, kp: int | None = None, kd: int | None = None,
                                 acceleration: int | None = None, torque_enabled: bool | None = None,
                                 zero_position: bool | None = None) -> bool:
        """Minimal configuration helper common options.

        - kp, kd: 0..255 speed loop gains (writes single-byte regs)
        - acceleration: 0..255 (direct value to SMS_STS_ACC)
        - torque_enabled: enable/disable
        - zero_position: if True, sets 0..4095 limits and mode=position, torque=0x80
        """
        # Register addresses for gains (matching kos_zbot.actuator.ADDR_KP/ADDR_KD)
        ADDR_KP = 21
        ADDR_KD = 22

        ok = True

        def _block():
            nonlocal ok
            if kp is not None:
                if not (0 <= int(kp) <= 255):
                    ok = False; return
                res, _ = self._sms.p.write1(actuator_id, ADDR_KP, int(kp))
                ok &= (res == 0)
            if kd is not None:
                if not (0 <= int(kd) <= 255):
                    ok = False; return
                res, _ = self._sms.p.write1(actuator_id, ADDR_KD, int(kd))
                ok &= (res == 0)
            if acceleration is not None:
                acc = int(acceleration)
                if not (0 <= acc <= 255):
                    ok = False; return
                res, _ = self._sms.p.write1(actuator_id, 41, acc)
                ok &= (res == 0)
            if torque_enabled is not None:
                res, _ = self._sms.enable_torque(actuator_id, bool(torque_enabled))
                ok &= (res == 0)
            if zero_position:
                # Unlock, set 0..4095, position mode=0, torque 0x80, lock
                self._sms.p.write1(actuator_id, 55, 0)         # LOCK=0
                self._sms.p.write2(actuator_id, 9, 0x0000)     # MIN_ANGLE_LIMIT
                self._sms.p.write2(actuator_id, 11, 0x0FFF)    # MAX_ANGLE_LIMIT
                self._sms.p.write1(actuator_id, 33, 0)         # MODE=position
                self._sms.p.write1(actuator_id, 40, 0x80)      # TORQUE_ENABLE special
                self._sms.p.write1(actuator_id, 55, 1)         # LOCK=1
        await asyncio.to_thread(_block)
        if torque_enabled:
            self._torque_enabled_for.add(actuator_id)
        elif torque_enabled is False:
            self._torque_enabled_for.discard(actuator_id)
        return ok

    async def read_positions(self, actuator_ids: list[int] | None = None) -> ActuatorsStateResponse:
        ids = actuator_ids or self._actuator_ids

        def _read_blocking() -> list[ActuatorState]:
            out: list[ActuatorState] = []
            for sid in ids:
                pos_ticks, _, _ = self._sms.read_position(sid)
                out.append(ActuatorState(actuator_id=sid, position_deg=_ticks_to_degrees(pos_ticks)))
            return out

        states = await asyncio.to_thread(_read_blocking)
        return ActuatorsStateResponse(states=states)


class FT_HAL:
    """Minimal KOS-compatible wrapper exposing .actuator service for Feetech servos.

    Usage:
        # First scan for actuators
        from kbot_puppet.utils.feetech_scan import scan_actuators
        actuators = await scan_actuators("/dev/ttyACM0")
        ids = [a["id"] for a in actuators]
        
        # Then use explicit IDs
        ftch = FT_HAL(port="/dev/tty.usbserial-xxx", actuator_ids=[1,2,3], baudrate=1_000_000)
        await ftch.actuator.get_actuators_state()
        await ftch.actuator.command_actuators([{"actuator_id": 1, "position": 45.0}])
        await ftch.close()
    """

    def __init__(self, port: str, actuator_ids: list[int], baudrate: int = 1_000_000, auto_torque: bool = True):
        self._ph = PortHandler(port, baudrate)
        self._ph.openPort()
        self._proto = ProtocolPacketHandler(self._ph)
        self._sms = SMS_STS(self._proto)
        self.actuator = FeetechActuatorService(self._sms, actuator_ids=actuator_ids, auto_torque=auto_torque)

    async def close(self) -> None:
        def _close_blocking():
            self._ph.closePort()

        await asyncio.to_thread(_close_blocking)


