import yaml
from pathlib import Path
import shutil
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
required_keys = ["source_dir", "remote_host", "remote_user", "rsync_module", "mqtt_host"]

def create_config_interactively(config_path: Path) -> dict:
    """Prompt the user for configuration values and create the config file."""
    logger.warning(f"Configuration file not found at {config_path}.")
    print("Please provide the following configuration values to create a new one:")

    config = {}

    for key in required_keys:
        prompt = f"  - Enter {key}: "
        user_input = input(prompt).strip()
        config[key] = user_input

    source_dir = handle_source_dir(Path(config["source_dir"]))
    total_gb = shutil.disk_usage(source_dir).total / 1.0e9 # disk size
    defaults = {"max_dir_size": total_gb, # GB
                "min_remaining_disk_space": 1, # GB
                "mqtt_port": 1883,
               }

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
    config_path = Path.home() / ".config/klog-sync.yaml"

    if not config_path.exists():
        config = create_config_interactively(config_path)
        sys.exit(1)

    with open(config_path, 'r') as f:
        user_config = yaml.safe_load(f)

    missing_keys = [k for k in required_keys if k not in user_config]
    if missing_keys:
        print(f"Error: Missing required config keys: {', '.join(missing_keys)}")
        sys.exit(1)

    user_config["source_dir"] = Path(user_config["source_dir"]).expanduser().resolve()

    total_gb = shutil.disk_usage(user_config["source_dir"]).total / 1.0e9 # disk size
    defaults = {"max_dir_size": total_gb, # GB
                "min_remaining_disk_space": 1, # GB
                "mqtt_port": 1883,
               }

    all_known_keys = required_keys + list(defaults.keys())
    unknown_keys = [k for k in user_config if k not in all_known_keys]
    if unknown_keys:
        print(f"Warning: Unrecognized config keys: {', '.join(unknown_keys)}")
    
    config = {**defaults, **user_config}


    return config

def handle_source_dir(source_dir: Path):
    source_dir = source_dir.expanduser().resolve()
    if not source_dir.is_dir():
        print(f"Source directory does not exist: {source_dir}. Creating it.")
        try:
            source_dir.mkdir(parents=True, exist_ok=True)
            return source_dir
        except Exception as e:
            print(f" FAILED!\n{e}")
            sys.exit(1)
