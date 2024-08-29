from typing import Union
from utils import config_loader
from pathlib import Path
import subprocess
import platform
import logging
import sys
import re

VERSION = "v0.0.3_1"
PLATFORM = f"    FlowWave Server {VERSION} - %s\nPython {sys.version} on {platform.platform()}"
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


def get(input_data: str) -> Union[str, Path]:
    global current_path
    input_data = input_data.replace("get ", "")
    new_path = current_path.joinpath(input_data).resolve()

    if new_path.exists():
        if new_path.is_file():

            new_path.__sizeof__()
            return new_path
        return f"get: not a file: {new_path.name}"
    return f"get: no such file or directory: {input_data}"


def run_command(cmd: str) -> str:
    process = None
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=current_path, shell=True)
        output, err = process.communicate(timeout=10)
        return output.decode()
    except subprocess.TimeoutExpired:
        try:
            if process is not None and process.poll() is None:
                process.terminate()
        except PermissionError:
            logging.error("Cannot terminate process for %a" % cmd)
        return f"Subprocess has been terminated. Timeout."
    except subprocess.CalledProcessError:
        output, err = process.communicate()
        return f"{output.decode()}\nSubprocess ended with code {process.returncode}"
    except PermissionError as e:
        return f"Subprocess: ({e.errno}) {e.strerror}"
    except UnicodeDecodeError as e:
        return f"Subprocess: {e.reason}"


def can_execute_any_command() -> bool:
    allow_shell_full_access = config_loader.get_config_property("allow_shell_full_access")
    return allow_shell_full_access is not None and allow_shell_full_access


def can_download_files() -> bool:
    allow_download_files = config_loader.get_config_property("allow_download_files")
    return allow_download_files is not None and allow_download_files


def can_upload_files() -> bool:
    allow_upload_files = config_loader.get_config_property("allow_upload_files")
    return allow_upload_files is not None and allow_upload_files


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


def execute_command(input_data: str) -> Union[str, Path]:
    global PLATFORM

    response_data = "Invalid command"
    can_execute_anything = can_execute_any_command()

    if input_data == "server_platform":
        response_data = PLATFORM % ("unrestricted" if can_execute_anything else "restricted")

    elif input_data == "upload_policy":
        response_data = "Upload files is " + ("allowed" if can_upload_files() else "not allowed")

    elif not re.sub(r"cd .+", "", input_data):
        response_data = cd(input_data)

    elif input_data == "pwd":
        response_data = pwd()

    elif can_run_ls_uname_command(input_data):
        return run_command(input_data)

    elif not re.sub(r"get .+", "", input_data):
        if can_download_files():
            return get(input_data)
        response_data = "Server: operation not permitted (download)"

    elif can_execute_anything:
        return run_command(input_data)

    return response_data
