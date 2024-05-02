import os
import socket
import struct
import config
import time
from tqdm import tqdm

def send_file(sck: socket.socket, filename):
    # Получение размера файла.
    filesize = os.path.getsize(filename)
    # В первую очередь сообщим серверу, сколько байт будет отправлено.
    sck.sendall(struct.pack("<Q", filesize))
    # Отправка файла блоками по 1024 байта.
    progress = tqdm(range(filesize), f"Отправка {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        for _ in progress:
            bytes_read = f.read(8192)
            if not bytes_read:
                # Файл полностью прочитан
                break
            sck.sendall(bytes_read)
            progress.update(len(bytes_read))

with socket.create_connection(("localhost", 6190)) as conn:
    print("Подключение к серверу.")
    print("Передача файла...")
    start = time.time()
    send_file(conn, config.filepath)
    end = time.time()
    my_time = end - start
    print(f"Отправлено за {my_time} сек.")
print("Соединение закрыто.")
