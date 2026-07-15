import asyncio
import websockets
import json
import signal
import subprocess

clients = set()

def make_msg(msg_type, **kwargs):
    return json.dumps({"type": msg_type, **kwargs})

async def handler(websocket):
    clients.add(websocket)
    print(f"Connection from {websocket.remote_address}" )

    try:
        # Keep the connection alive by waiting for messages from the client
        # (or just sleep forever if the client only receives data)
        async for message in websocket:
            pass
    except asyncio.CancelledError:
        pass
    finally:
        print("Client disconnected.")
        clients.remove(websocket)

# await websocket.send(make_msg("chat",msg=f"time: {t2}"))

async def calc_load():
    command="uptime|awk '{print$10}'|sed \"sx,xxg\" "
    while True:
        # 1. Fetch the data EXACTLY ONCE
        payload = json.dumps({"type": "cpu", "value": 42})
        try:
            output=subprocess.check_output(command,shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Command failed with code {e.returncode}")
            print(f"Error output: {e.stderr}")
        load=output.decode()
        payload=(make_msg("load",text=f"{load}"))
        if clients:
            await asyncio.gather(
                *[client.send(payload) for client in clients],
                return_exceptions=True
                # Prevents one dead client from breaking the whole loop
             )
        await asyncio.sleep(1)

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    asyncio.create_task(calc_load())

    ip="localhost"
    pt=8777
    async with websockets.serve(handler,ip,pt,ping_interval=20,ping_timeout=5):
        print(f"Dashboard server running on ws://{ip}:{pt}")
        try:
            await stop  # Run until SIGTERM
        except asyncio.exceptions.CancelledError:
            print("Got control-C'd")
        finally:
            pass 

if __name__ == "__main__":
    asyncio.run(main())

