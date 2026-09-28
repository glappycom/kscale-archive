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

def create_config_interactively(config_path: Path) -> dict:
    """Prompt the user for configuration values and create the config file."""
    logger.warning(f"Configuration file not found at {config_path}.")
    print("Please provide the following configuration values to create a new one:")

    defaults = {
        "log_dir": "~/kinfer-logs",
        "mqtt_host": "klog",
        "mqtt_port": 1883,
    }
    config = {}

    for key, default_value in defaults.items():
        prompt = f"  - Enter {key} [default: {default_value}]: "
        user_input = input(prompt).strip()
        config[key] = user_input if user_input else default_value

    try:
        config["mqtt_port"] = int(config["mqtt_port"])
    except (ValueError, TypeError):
        logger.warning(f"Invalid port '{config['mqtt_port']}'. Using default {defaults['mqtt_port']}.")
        config["mqtt_port"] = defaults["mqtt_port"]

    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        logger.info(f"Configuration saved to {config_path}")
    except Exception as e:
        logger.error(f"Could not write configuration file to {config_path}: {e}")
        sys.exit(1)

    return config


def load_config():
    config_path = Path.home() / ".config/klog-robot.yaml"

    if not config_path.exists():
        config = create_config_interactively(config_path)
    else:
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
