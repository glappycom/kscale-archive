import yaml
from pathlib import Path
import sys
import logging
import colorlogging

logger = logging.getLogger(__name__)
colorlogging.configure(
    logger=logger,
    remove_existing_handlers=True,
    hide_if_not_interactive=False,
    level=logging.DEBUG,
)

def load_config():
    config_path = Path.home() / ".config/klog-server.yaml"

    if not config_path.exists():
        print(f"configuration file not found at {config_path}.")
        sys.exit(1)

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    required_keys = ["log_dir", "mqtt_host", "mqtt_port"]
    missing_keys = [k for k in required_keys if k not in config]
    if missing_keys:
        print(f"Error: Missing required config keys: {', '.join(missing_keys)}")
        sys.exit(1)

    config["log_dir"] = Path(config["log_dir"]).expanduser().resolve()
    if not config["log_dir"].is_dir():
        print(f"Log directory does not exist: {config['log_dir']}. Creating it ...", end ='')
        try:
            config["log_dir"].mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f" FAILED!\n{e}")
            sys.exit(1)

    return config
