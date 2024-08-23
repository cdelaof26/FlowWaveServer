from utils import command_worker, config_loader
import websockets
import asyncio
import re


def parse_data(input_data: str) -> str:
    response_data = command_worker.execute_command(input_data)
    response_data = re.sub("\n$", "", response_data)
    response_data = response_data.replace("\n", "\\n")
    return '{"data": "' + response_data + '"}'


async def echo(socket: websockets.WebSocketServerProtocol):
    async for message in socket:
        print(f"Received data: {message}")
        await socket.send(parse_data(message))


if __name__ == "__main__":
    print("[INFO] Loading configuration file...")
    try:
        config_loader.read_config()
    except ValueError as e:
        print("[ERROR] Invalid configuration file")
        print("        Delete the file 'config' to load the defaults")
        print("\n", e)
        exit(1)

    if command_worker.can_execute_any_command():
        print("[WARNING] Unrestricted access to shell is allowed!")

    host_ip = config_loader.config["host_ip"]
    port = config_loader.config["port"]

    """import ssl
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    start_server = websockets.serve(echo, host_ip, port, ssl=ssl_context)"""

    start_server = websockets.serve(echo, host_ip, port)

    asyncio.get_event_loop().run_until_complete(start_server)
    print(f"[INFO] Server started at ws://{host_ip}:{port}")
    asyncio.get_event_loop().run_forever()
