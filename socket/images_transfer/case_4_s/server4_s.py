import asyncio
import os
import aiofiles

IP = 'localhost'
PORT = 4456
SIZE = 1024

async def receive_file(reader, filename, filesize):
    output_folder = "get_images"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, filename)
    async with aiofiles.open(output_path, 'wb') as f:
        while filesize > 0:
            chunk = await reader.read(min(filesize, SIZE))
            await f.write(chunk)
            filesize -= len(chunk)

async def server_program():
    server = await asyncio.start_server(handle_client, IP, PORT)
    async with server:
        await server.serve_forever()

async def handle_client(reader, writer):
    while True:
        data = await reader.read(SIZE)
        filename, filesize = data.decode().split(":")
        filesize = int(filesize)
        print(f"Received filename {filename} and filesize {filesize}")
        await receive_file(reader, filename, filesize)
        writer.write("Data received.".encode())
        await writer.drain()

asyncio.run(server_program())
