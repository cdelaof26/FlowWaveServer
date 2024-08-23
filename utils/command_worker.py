from utils import config_loader
from pathlib import Path
import subprocess
import platform
import sys
import re


PLATFORM = f"    FlowWave Server v0.0.2 - %s\\nPython {sys.version} on {platform.platform()}"
OS = platform.system()
IS_WINDOWS = OS == "Windows"
current_path = Path.home()


def pwd() -> str:
    global current_path
    return str(current_path)


def cd(input_data: str) -> str:
    global current_path
    input_data = input_data.replace("cd ", "")
    if input_data == "~":
        new_path = Path.home()
    else:
        new_path = current_path.joinpath(input_data).resolve()

    if new_path.exists():
        if new_path.is_dir():
            current_path = new_path
            return ""

        return f"cd: not a directory: {new_path.name}"
    return f"cd: no such file or directory: {input_data}"


def run_command(cmd: str) -> str:
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=10, cwd=current_path, shell=True).decode()
    except subprocess.TimeoutExpired:
        return "Subprocess has been killed. Timeout"
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
        return f"{output}\nSubprocess ended with code {e.returncode}"
    except PermissionError as e:
        return f"Subprocess: ({e.errno}) {e.strerror}"
    except UnicodeDecodeError as e:
        return f"Subprocess: {e.reason}"


def can_execute_any_command() -> bool:
    allow_shell_full_access = config_loader.get_config_property("allow_shell_full_access")
    if allow_shell_full_access is None or not allow_shell_full_access:
        return False

    return True


def can_run_ls_uname_command(input_data: str) -> bool:
    if input_data in ["ls", "uname"]:
        return True

    if re.sub("ls .+", "", input_data) and re.sub("uname .+", "", input_data):
        return False

    not_allowed_symbols = ["&", ";", "|", "<", ">", "{", "}"]

    opened_strings = 0
    for c in input_data:
        if c == '"':
            opened_strings = 1 if opened_strings == 0 else 0
            continue

        if c in not_allowed_symbols:
            if opened_strings == 0:
                return False

    return True


def execute_command(input_data: str) -> str:
    global PLATFORM

    response_data = "Invalid command"
    can_execute_anything = can_execute_any_command()

    if input_data == "server_platform":
        response_data = PLATFORM % ("unrestricted" if can_execute_anything else "restricted")

    elif not re.sub(r"cd .+", "", input_data):
        response_data = cd(input_data)

    elif input_data == "pwd":
        response_data = pwd()

    elif can_run_ls_uname_command(input_data):
        return run_command(input_data)

    elif can_execute_anything:
        return run_command(input_data)

    return response_data
