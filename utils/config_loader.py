from pathlib import Path
import re

DEFAULTS = """# FlowWave Server Configuration File

host_ip: localhost
port: 6789
password: 
mode: websocket

# Always allowed commands: server_platform, uname, cd, ls, pwd
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


def read_config():
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
            raise ValueError
