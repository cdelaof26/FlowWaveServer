from pathlib import Path
import logging
import re

DEFAULTS = """# FlowWave Server Configuration File

host_ip: localhost
port: 6789
password: 
mode: websocket

# You may change the serving path to somewhere else by specifying the path,
# use 'default' (no quotes) to serve user home directory
serving_path: default

# Setting 'allow_full_filesystem_access' to 'True' will allow the user to use 'cd' command
# to navegate to any location on the filesystem
allow_full_filesystem_access: False

# Setting 'allow_subdir_filesystem_access' to 'False' will prohibit the user to move into any 
# directories inside the 'serving_path'
# Note: setting 'allow_full_filesystem_access' to 'True' will overwrite this property
allow_subdir_filesystem_access: True

# Always allowed commands: server_platform, uname, ls, pwd
# Use 'True' to specify that the user is capable of executing code without limitations
allow_shell_full_access: False

# Allow 'get' command
allow_download_files: True

# Allow 'put' command
allow_upload_files: True
"""


CONFIG_FILE = Path("config")
config = dict()


def get_config_property(prop: str) -> any:
    global config

    if prop not in config:
        return None
    return config[prop]


def save_defaults():
    global DEFAULTS, CONFIG_FILE
    with open(CONFIG_FILE, "w") as file:
        file.write(DEFAULTS)


def read_config() -> Path:
    global DEFAULTS, CONFIG_FILE, config
    if not CONFIG_FILE.exists():
        save_defaults()

    with open(CONFIG_FILE, "r") as file:
        data = file.read()

    data = re.sub("#.*", "", data)
    data = re.sub("\n+", "\n", data)
    data = re.sub("^\n", "", data)
    data = re.sub("\n$", "", data)

    for line in data.split("\n"):
        logging.info(f"Reading line: {line}")
        prop, value = line.replace(": ", ":").split(":")
        if not value:
            value = None
        elif not re.sub(r"\d+", "", value):
            value = int(value)
        elif value.lower() in ["true", "false"]:
            value = value.lower() == "true"

        config[prop] = value

    for prop in ["host_ip", "port", "mode"]:
        if prop not in config:
            raise ValueError(f"Property {prop} requires a value!")

    return get_serving_path()


def get_serving_path() -> Path:
    serving_path = get_config_property("serving_path")
    if serving_path is None or serving_path is not None and serving_path == "default":
        return Path.home()

    serving_path = Path(serving_path)
    if not serving_path.exists() or not serving_path.is_dir():
        raise ValueError(f"Serving path '{serving_path}' not found or is not a directory")

    return serving_path


def can_execute_any_command() -> bool:
    allow_shell_full_access = get_config_property("allow_shell_full_access")
    return allow_shell_full_access is not None and allow_shell_full_access


def can_download_files() -> bool:
    allow_download_files = get_config_property("allow_download_files")
    return allow_download_files is not None and allow_download_files


def can_upload_files() -> bool:
    allow_upload_files = get_config_property("allow_upload_files")
    return allow_upload_files is not None and allow_upload_files


def can_access_subdirectory_filesystem() -> bool:
    allow_subdir_filesystem_access = get_config_property("allow_subdir_filesystem_access")
    return allow_subdir_filesystem_access is not None and allow_subdir_filesystem_access


def can_fully_access_the_filesystem() -> bool:
    allow_full_filesystem_access = get_config_property("allow_full_filesystem_access")
    return allow_full_filesystem_access is not None and allow_full_filesystem_access
