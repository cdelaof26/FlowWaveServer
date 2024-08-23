from pathlib import Path
from threading import Thread
import subprocess
import server


PORT = 80
python = "python" if server.command_worker.IS_WINDOWS else "python3"
frontend = Path("../FlowWave")

if not frontend.exists():
    print(f"The directory {frontend.resolve()} does not exist")
    exit(1)

process = None


def run_http():
    global process
    print(f"[INFO] HTTP Server (client) running")
    try:
        process = subprocess.Popen(
            python + f" -m http.server {PORT}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, cwd=frontend
        )
        process.wait()
    except OSError as e:
        print(e)
    print(f"[INFO] HTTP Server (client) TERMINATED")


t = Thread(target=run_http)
t.start()

try:
    server.run()
except KeyboardInterrupt:
    if process is not None:
        process.terminate()
