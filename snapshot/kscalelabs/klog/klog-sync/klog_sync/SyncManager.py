import time
import subprocess
import shutil
from pathlib import Path
import logging
import colorlogging
import json
import sys
import threading

logger = logging.getLogger(__name__)
colorlogging.configure(
    logger=logger,
    remove_existing_handlers=True,
    hide_if_not_interactive=False,
    level=logging.DEBUG,
)

RunId = str

class SyncManager():
    def __init__(self):
        pass

    def new(self, src: Path, dst: str,
                 max_dir_size: float,
                 min_remaining_disk_space: float,
                 sync_state_changed_callback: callable) -> None:
        # Setup params
        self.log_dir: Path = Path(src)
        self.dst: str = dst
        self.max_dir_size: float = max_dir_size
        self.min_remaining_disk_space: float = min_remaining_disk_space
        self.sync_queue: dict[RunId, dict] = {}
        self.syncing: threading.Event = threading.Event()
        self.rsync_proc = None
        self.sync_thread = threading.Thread(target=self.sync_loop, daemon=True)
        self.sync_state_changed_callback = sync_state_changed_callback
        
        self.scan_sync_statuses()
        threading.Thread(target=self.sync_loop, daemon=True).start()
        self.sync()

    def sync_loop(self):
        while True:
            self.syncing.wait()
            for run_id in list(self.sync_queue.keys()):
                if run_id and self.ready_to_sync(run_id):
                    self.sync_run(run_id)
            time.sleep(1)

    def pause(self):
        self.syncing.clear()
        if self.rsync_proc:
            self.rsync_proc.terminate()

    def sync(self):
        self.syncing.set()

    def ready_to_sync(self, run_id: RunId) -> bool:
        run_dir: Path = self.log_dir / run_id

        latest_mtime = 0.0
        for p in run_dir.rglob("*"):
            try:
                mtime = p.stat().st_mtime
                if mtime > latest_mtime:
                    latest_mtime = mtime
            except FileNotFoundError:
                continue

        if time.time() - latest_mtime > 10:
            logger.debug("Run %s is ready to sync", run_id)
            return True

        else:
            logger.debug("Run %s is not ready to sync yet", run_id)
            return False


    def queue(self, run_id: RunId) -> None:
        if run_id not in self.sync_queue:
            self.sync_queue[run_id] = {"status": "not_synced"}
        else:
            logger.warning("Run %s is already queued for sync", run_id)

    def scan_sync_statuses(self) -> None:
        logger.debug("Updating sync status for %s", self.log_dir)
        self.sync_status = {}
        for run_dir in self.log_dir.iterdir():
            if run_dir.is_dir():
                run_id: RunId = run_dir.name
                if (run_dir / ".sync_status").exists():
                    try:
                        run_sync_status = json.loads((run_dir / ".sync_status").read_text())
                    except json.JSONDecodeError:
                        logger.error("Failed to decode sync status for run %s", run_id)
                        run_sync_status = {"status": "not_synced", "last_attempt": time.time()}
                else:
                    run_sync_status = {"status": "not_synced"}

                if run_sync_status.get("status") != "completed":
                    self.sync_queue[run_id] = run_sync_status

    def sync_run(self, run_id: RunId) -> bool:
        src_dir: Path = self.log_dir / run_id
        src_str: str = str(src_dir.resolve())

        logger.debug("Syncing %s to %s", src_dir, self.dst)
        self.sync_state_changed_callback(run_id, "syncing")

        return_code = None
        try:
            self.rsync_proc = subprocess.Popen([
                "rsync",
                "-ah", # archive mode for syncing a directory, human-readable output
                "--compress",
                "--verbose",
                "--stats",
                "--info=progress2", # show live progress on the whol edirectory
                "--no-perms", # Don't sync file permissions
                "--chmod=Du=rwx,Dg=rwx,Do=rx,Fu=rw,Fg=rw,Fo=r", # overkill since the rsync daemon should be set up with recieve permissions
                "--skip-compress=jpg/jpeg/png/gif/mp4/mov/avi/flv/mkv/webm/gz/bz2", # these formats are already compressed
                "--exclude=.sync_status", # the server doesn't want this
                src_str,
                self.dst,
            ])
            return_code = self.rsync_proc.wait()

        except Exception as e:
            logger.error("Rsync failed for run %s. Error: %s", run_id, e)

        finally:
            self.enforce_size_limits()

            if return_code == 0:
                logger.info("Sucessfully synced run %s", run_id)
                del self.sync_queue[run_id]
                (src_dir / ".sync_status").write_text(json.dumps({"status": "completed", "last_attempt": time.time()}))
                self.sync_state_changed_callback(run_id, "done")
                return True

            elif not self.syncing.is_set():
                logger.warning("Sync paused")
                self.sync_state_changed_callback(run_id, "paused")
                return False

            else:
                if return_code is not None:
                    logger.error("Rsync failed with exit code %s", return_code)
                self.sync_queue[run_id] = {"status": "failed", "last_attempt": time.time()}
                (src_dir / ".sync_status").write_text(json.dumps(self.sync_queue[run_id]))
                self.sync_state_changed_callback(run_id, "failed", failure_type=f"rsync_error: {return_code}")
                return False

    # TODO clean up
    def enforce_size_limits(self):
        while self.get_size() > self.max_dir_size:
            logger.warning("Source directory size exceeds maximum limit (%s GB).", self.max_dir_size)
            self.delete_oldest_or_exit()

        while self.free_space() < self.min_remaining_disk_space:
            logger.warning("Free disk space is below minimum limit (%s GB).", self.min_remaining_disk_space)
            if self.free_space() + self.get_size() < self.min_remaining_disk_space:
                logger.error("Not enough disk space will be freed by deletion of items in %s. "
                             "Can't enforce size limits.", self.log_dir)
                sys.exit(3)

            self.delete_oldest_or_exit()

    def delete_oldest_or_exit(self) -> bool:
        """Delete the oldest directory in the log_dir that is not in the sync queue. Exits if fails."""
        run_dirs = sorted(self.log_dir.glob("*/"), key=lambda d: d.stat().st_ctime)
        candidates = [d for d in run_dirs if d.name not in self.sync_queue]

        if len(candidates) <= 1:
            logger.error("No old directories to delete in %s", self.log_dir)
            sys.exit(3)

        logger.warning("Deleting oldest item in %s: %s", self.log_dir, candidates[0])
        try:
            shutil.rmtree(candidates[0], ignore_errors=True)
        except OSError as e:
            logger.error("Failed to delete directory %s: %s", candidates[0], e)
            sys.exit(3)
        return True

    def get_size(self) -> float:
        size_bytes: int = sum(f.stat().st_size for f in self.log_dir.glob("**/*") if f.is_file())
        size_GB: float = size_bytes / 1.0e9  # Convert bytes to GB
        logger.debug("Size of directory %s: %.2f GB", self.log_dir, size_GB)
        return size_GB

    def free_space(self) -> float:
        free_space: float = shutil.disk_usage(self.log_dir.as_posix()).free / 1.0e9  # Get free space in GB
        logger.debug("Free space on disk: %.2f GB", free_space)
        return free_space
