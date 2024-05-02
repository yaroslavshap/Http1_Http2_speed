import asyncio
import os
import struct

IP = 'localhost'
PORT = 4456
SIZE = 1024

async def receive_file_size(reader):
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    print("expected_bytes",expected_bytes)
    received_bytes = 0
    stream = bytes()
    while received_bytes < expected_bytes:
        chunk = await reader.read(expected_bytes - received_bytes)
        stream += chunk
        received_bytes += len(chunk)
        print("received_bytes",received_bytes)
    filesize = struct.unpack(fmt, stream)[0]
    return filesize

async def receive_file(reader, writer, filename):
    filesize = await receive_file_size(reader)
    with open(filename, "wb") as f:
        received_bytes = 0
        while received_bytes < filesize:
            chunk = await reader.read(1024)
            if chunk:
                f.write(chunk)
                received_bytes += len(chunk)

async def handle_client(reader, writer):
    print("Получаем файл...")
    await receive_file(reader, writer, "file-received.zip")
    print("Файл получен.")
    print("Соединение закрыто.")
    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, IP, PORT)
    async with server:
        await server.serve_forever()

asyncio.run(main())
