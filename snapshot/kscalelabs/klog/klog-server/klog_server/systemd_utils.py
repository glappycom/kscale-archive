import subprocess
from pathlib import Path
import sys
import logging
import inspect
import colorlogging
import os

logger = logging.getLogger(__name__)
colorlogging.configure(
    logger=logger,
    remove_existing_handlers=True,
    hide_if_not_interactive=False,
    level=logging.DEBUG,
)


def systemd_service(service_name: str, description: str | None = None):
    """
    Decorator to create a systemd service helpers for a function.
    """

    def decorator(func):
        return SystemdService(func, service_name, description)

    return decorator


class SystemdService:
    def __init__(
        self, func: callable, service_name: str, description: str | None = None
    ):
        sig = inspect.signature(func)
        if any(
            param.kind
            in (param.POSITIONAL_OR_KEYWORD, param.POSITIONAL_ONLY, param.KEYWORD_ONLY)
            for param in sig.parameters.values()
        ):
            raise TypeError(f"Function {func.__name__} must not accept any arguments.")

        self.func = func
        self.service_name = service_name
        self.description = description or service_name
        self.commands = {
            "start": self.start,
            "restart": self.restart,
            "stop": self.stop,
            "status": self.status,
            "enable": self.enable,
            "disable": self.disable,
            "install": self.install_service,
            "uninstall": self.uninstall_service,
            "journal": self.journal,
        }

    def __call__(self, *args, **kwargs):
        if len(sys.argv) > 1:
            if sys.argv[1] in self.commands:
                return self.commands[sys.argv[1]]()
            else:
                return self.func(*args, **kwargs)

        return self.func(*args, **kwargs)

    def start(self):
        proc = subprocess.run(["systemctl", "--user", "start", self.service_name], check=False)
        print(f"Exit code: {proc.returncode}")

    def restart(self):
        proc = subprocess.run(["systemctl", "--user", "restart", self.service_name], check=False)
        print(f"Exit code: {proc.returncode}")

    def stop(self):
        proc = subprocess.run(["systemctl", "--user", "stop", self.service_name], check=False)
        print(f"Exit code: {proc.returncode}")

    def status(self):
        proc = subprocess.run(["systemctl", "--user", "status", self.service_name], check=False)
        print(f"Exit code: {proc.returncode}")

    def enable(self):
        proc = subprocess.run(["systemctl", "--user", "enable", self.service_name], check=False)
        print(f"Exit code: {proc.returncode}")

    def disable(self):
        proc = subprocess.run(["systemctl", "--user", "disable", self.service_name], check=False)
        print(f"Exit code: {proc.returncode}")

    def journal(self):
        proc = subprocess.run(["journalctl", "--user", "-o", "cat", "-fxeu", self.service_name], check=False)
        print(f"Exit code: {proc.returncode}")

    def install_service(self):
        env_path = Path(sys.executable).parent

        # create a systemd unit
        user_systemd = Path.home() / ".config/systemd/user"
        user_systemd.mkdir(parents=True, exist_ok=True)

        xdg_runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
        environment_line = ""
        if xdg_runtime_dir:
            environment_line = f'Environment="XDG_RUNTIME_DIR={xdg_runtime_dir}"'
        path_line = f'Environment="PATH={env_path}:{os.environ.get("PATH", "")}"'

        unit_file = user_systemd / f"{self.service_name}.service"
        unit_file.write_text(f"""
    [Unit]
    Description={self.description}
    After=network.target
    StartLimitIntervalSec=300
    StartLimitBurst=10

    [Service]
    ExecStart={sys.executable} -m {self.func.__module__}
    {environment_line}
    {path_line}
    Restart=always
    RestartSec=5s

    [Install]
    WantedBy=default.target
    """)

        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)

    def uninstall_service(self):
        user_systemd = Path.home() / ".config/systemd/user"
        unit_file = user_systemd / f"{self.service_name}.service"

        if unit_file.exists():
            unit_file.unlink()
            subprocess.run(["systemctl", "--user", "daemon-reload"])
            logger.info(f"Uninstalled service {self.service_name}.")
        else:
            logger.warning(f"Service {self.service_name} is not installed.")
