from typing import Union
from utils import command_worker, config_loader
import websockets
import asyncio
import logging
import math
import re


def parse_data(input_data: str) -> Union[str, any]:
    if input_data and not re.sub(r"\d+up:.+", "", input_data):
        data = input_data.split("up:")
        return int(data[0]), data[1]

    response_data = command_worker.execute_command(input_data)
    if isinstance(response_data, str) and "download" in response_data:
        logging.info("Rejected request to download: %a" % str(input_data))

    if not isinstance(response_data, str):
        return response_data

    response_data = re.sub("\n$", "", response_data)
    response_data = response_data.replace("\n", "\\n")
    return '{"data": "' + response_data + '"}'


dropped_data = 0
filesize = 0
file_name = ""


async def echo(socket: websockets.WebSocketServerProtocol):
    global dropped_data, filesize, file_name

    can_upload_files = command_worker.can_upload_files()

    async for message in socket:
        if not can_upload_files and isinstance(message, bytes):
            dropped_data += 1
            logging.info(f"Skip upload data ({dropped_data}/10)")
            if dropped_data > 9:
                dropped_data = 0
                await socket.close()

            continue

        logging.info(f"Received data: {message}")
        response = parse_data(message)

        if isinstance(response, str):  # Text messages
            await socket.send(response)

        elif isinstance(response, tuple):  # Upload request
            filesize, file_name = response
            if can_upload_files:
                uploaded = 0
                logging.info(f"A file is being uploaded")
                with open(command_worker.current_path.joinpath(file_name), "wb") as file:
                    while uploaded < filesize:
                        chunk = await socket.recv()
                        uploaded += len(chunk)
                        file.write(chunk)
                        logging.info(f"Progress for '{file_name}' is {math.trunc(uploaded * 100 / filesize)}%")
            else:
                logging.info(f"Rejected request to upload: %a [size:{filesize}]" % str(file_name))
                await socket.send('{"data": "Server: operation not permitted (upload)"}')

        else:  # Download request
            await socket.send(f"{response.stat().st_size}:{response.name}")
            with open(response, "rb") as file:
                for chunk in file:
                    await socket.send(chunk)


def run():
    logging.basicConfig(level=logging.INFO)

    logging.info("Loading configuration file...")
    try:
        config_loader.read_config()
    except ValueError as e:
        logging.error("[ERROR] Invalid configuration file")
        logging.error("        Delete the file 'config' to load the defaults")
        logging.error("\n", e)
        exit(1)

    if command_worker.can_execute_any_command():
        logging.warning("Unrestricted access to shell is allowed!")

    host_ip = config_loader.config["host_ip"]
    port = config_loader.config["port"]

    """import ssl
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    start_server = websockets.serve(echo, host_ip, port, ssl=ssl_context)"""

    start_server = websockets.serve(echo, host_ip, port)

    asyncio.get_event_loop().run_until_complete(start_server)
    logging.info(f"Server started at ws://{host_ip}:{port}")
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    run()
