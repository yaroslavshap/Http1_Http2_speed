import asyncio
import aiofiles
import os
import time
import config

IP = 'localhost'
PORT = 4456
SIZE = 1024

async def send_file(writer, filepath):
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    writer.write(f"{filename}:{filesize}".encode())
    await writer.drain()

    async with aiofiles.open(filepath, 'rb') as f:
        while True:
            chunk = await f.read(SIZE)
            if not chunk:
                # We have read the file completely.
                break
            writer.write(chunk)
            await writer.drain()
async def client_program():
    reader, writer = await asyncio.open_connection(IP, PORT)

    directory = config.folder
    start = time.time()
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            await send_file(writer, os.path.join(directory, filename))

    print(f"Result transfer time = {time.time() - start} seconds")
    writer.close()

asyncio.run(client_program())
