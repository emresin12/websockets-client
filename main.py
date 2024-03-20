
import asyncio
import time

import websockets


latencies = []
n_conn = 500
async def listen_to_server(i):
    await asyncio.sleep(0)
    uri = "ws://localhost:8765"
    beginning = time.time()
    n_messages = 0
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                message = await websocket.recv()
                n_messages += 1
                if message == "close":
                    break
                # You can process the message here
            await websocket.close()
            end = time.time()
            print(f"Connection {i} received {n_messages} messages in {end - beginning} seconds")
        except websockets.exceptions.ConnectionClosed:
            print(f"Connection {i} closed by the server")
            pass  # Expected when the server closes the connection

async def latency_test():
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as websocket:
        for i in range(10):
            await asyncio.sleep(0)
            start_time = time.time()
            await websocket.send("x"*1024)
            await websocket.recv()
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # in milliseconds
            latencies.append(latency)


async def receive_data():
    await asyncio.gather(*(listen_to_server(i) for i in range(n_conn)))

async def conduct_latency_test():
    await asyncio.gather(*(latency_test() for i in range(n_conn)))
    print(f"Average latency: {sum(latencies) / len(latencies)} ms")
    print(f"Max latency: {max(latencies)} ms")
    print(f"Min latency: {min(latencies)} ms")

asyncio.get_event_loop().run_until_complete(receive_data())