import asyncio
import os
import struct
import time
import config
from tqdm import tqdm

IP = 'localhost'
PORT = 4456
SIZE = 1024

async def send_file(writer, filepath):
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    writer.write(f"{filename}:{filesize}".encode())
    await writer.drain()

    with open(filepath, 'rb') as f:
        for _ in tqdm(range(filesize), f"Отправка {filename}", unit="B", unit_scale=True, unit_divisor=1024):
            bytes_read = f.read(SIZE)
            if not bytes_read:
                # Файл полностью прочитан
                break
            writer.write(bytes_read)
            await writer.drain()

async def client_program():
    reader, writer = await asyncio.open_connection(IP, PORT)

    print("Подключение к серверу.")
    print("Передача файла...")
    start = time.time()
    await send_file(writer, config.filepath)
    end = time.time()
    my_time = end - start
    print(f"Отправлено за {my_time} сек.")
    writer.close()

asyncio.run(client_program())
