from typing import Union
from utils import config_loader
from datetime import datetime
from pathlib import Path
import subprocess
import platform
import logging
import sys
import re

VERSION = "v0.0.4"
PLATFORM = f"    FlowWave Server {VERSION} - %s\nPython {sys.version} on {platform.platform()}"
OS = platform.system()
IS_WINDOWS = OS == "Windows"
_serving_path = None
current_path = Path.home()


def set_serving_path(serving_path: Path):
    global _serving_path, current_path
    _serving_path = serving_path
    current_path = _serving_path


def uls(input_data: str) -> str:
    global current_path
    directory_data = ""
    allow_hidden = "true" in input_data.lower()

    try:
        for e in sorted(current_path.iterdir()):
            if not allow_hidden and e.name.startswith("."):
                continue

            _stat = e.stat()
            # name = re.sub(f"{e.suffix}$", "", e.name)
            name = e.name
            modification_date = datetime.fromtimestamp(_stat.st_mtime).strftime("%d %b %Y, %H:%M")
            directory_data += f"{name};{modification_date};{e.is_dir()}\n"
    except (PermissionError, FileNotFoundError):
        return "ls: "

    return f"ls: {directory_data}"


def pwd() -> str:
    global current_path
    return f"pwd: {current_path}"


def cd(input_data: str) -> str:
    global current_path
    input_data = input_data.replace("cd ", "")
    if "~" in input_data:
        new_path = Path(input_data.replace("~", str(Path.home())))
    else:
        new_path = current_path.joinpath(input_data).resolve()

    if not config_loader.can_fully_access_the_filesystem():
        if not config_loader.can_access_subdirectory_filesystem():
            return "cd: operation not permitted (subdirectory access)"

        if str(_serving_path) not in str(new_path):
            return "cd: operation not permitted (filesystem access)"

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
    can_execute_any_command = config_loader.can_execute_any_command()

    if not can_execute_any_command:
        cmd = cmd.split(" ")

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   cwd=current_path, shell=can_execute_any_command)
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
    except FileNotFoundError:
        return "Invalid command"


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


def get_server_platform(can_execute_anything: bool):
    allow_full_filesystem_access = config_loader.can_fully_access_the_filesystem()
    if allow_full_filesystem_access and can_execute_anything:
        return PLATFORM % "unrestricted"
    elif not allow_full_filesystem_access and not can_execute_anything:
        return PLATFORM % "fully restricted"

    if not allow_full_filesystem_access:
        return PLATFORM % "filesystem restricted"
    return PLATFORM % "shell restricted"


def execute_command(input_data: str) -> Union[str, Path]:
    global PLATFORM

    response_data = "Invalid command"
    can_execute_anything = config_loader.can_execute_any_command()

    if input_data == "server_platform":
        response_data = get_server_platform(can_execute_anything)

    elif input_data == "upload_policy":
        response_data = "Upload files is " + ("allowed" if config_loader.can_upload_files() else "not allowed")

    elif not re.sub(r"cd .+", "", input_data):
        response_data = cd(input_data)

    elif not re.sub(r"uls .+", "", input_data):
        response_data = uls(input_data)

    elif input_data == "pwd":
        response_data = pwd()

    elif can_run_ls_uname_command(input_data):
        return run_command(input_data)

    elif not re.sub(r"get .+", "", input_data):
        if config_loader.can_download_files():
            return get(input_data)
        response_data = "Server: operation not permitted (download)"

    elif can_execute_anything:
        return run_command(input_data)

    return response_data
