import asyncio
import websockets
import json
import signal
import itertools
# import ssl

CLIENTS = set()
id_counter = itertools.count(1)
client_ids = {}

def make_msg(msg_type, **kwargs):
    return json.dumps({"type": msg_type, **kwargs})

async def handler(websocket):
    CLIENTS.add(websocket)
    client_ids[websocket] = next(id_counter)
    print("Connection from ",websocket.remote_address)
    try:
        async for message in websocket:
            if message[:6] == "/nick ":
                print("Got /nick command")
                print(f"new nick is {message[6:]}")
                old_id=client_ids[websocket]
                client_ids[websocket]=message[6:]
                await websocket.send(make_msg("status",text=f"nickname changed to {message[6:]}"))
                others = CLIENTS - {websocket}
                data=make_msg("status",text=f"{old_id} changed nickname to {client_ids[websocket]}")
                websockets.broadcast(others, data)
                pass
            await websocket.send(make_msg("echo", text=f"{message}"))
            others = CLIENTS - {websocket}
            # ip=websocket.remote_address
            data=make_msg("chat", from_id=client_ids[websocket], msg=message)
            websockets.broadcast(others, data)
    except websockets.ConnectionClosed:
        pass
    finally:
        print("Disconnection: ",websocket.remote_address)
        CLIENTS.discard(websocket)
        del client_ids[websocket]
async def main():
#    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#    ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
#
#    i took the cert that I got from Let's Encrypt with my https server
#    split the secret key into the key.pem file and left the cert/ca in cert.pem
#
#    there is an openssl command to read the pem files, found it on google...
#    if you want to verify the contents =)

    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    ip="localhost"
#    async with websockets.serve(handler, ip, 8443,ssl=ssl_context):
#        print(f"Server running on wss://{ip}:8443")
    async with websockets.serve(handler, ip, 8765):
        print(f"Server running on wss://{ip}:8765")
        await stop  # Run until SIGTERM

if __name__ == "__main__":
    asyncio.run(main())
