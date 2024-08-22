from pathlib import Path
import websockets
import asyncio
import sys


home = Path.home()


def ls() -> str:
    global home
    data = [f'"{e.name.replace(e.suffix, "")}"' for e in home.iterdir()]

    return '{"data": [' + ', '.join(data) + ']}'


def parse_data(data: str) -> str:
    if data == "ls":
        return ls()

    return '{"data": "Comando desconocido"}'


async def echo(socket: websockets.WebSocketServerProtocol):
    async for message in socket:
        print(f"Received data: {message}")
        await socket.send(parse_data(message))


if __name__ == "__main__":
    port = 6789
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    start_server = websockets.serve(echo, "localhost", port)

    asyncio.get_event_loop().run_until_complete(start_server)
    print("Server started at ws://localhost:6789")
    asyncio.get_event_loop().run_forever()
