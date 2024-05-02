import socket
import os
import time

from tqdm import tqdm

HOST = "127.0.0.1"
PORT = 4453
filepath = "/Users/aroslavsapoval/myProjects/data/images1000.zip"
FILENAME = os.path.basename(filepath)
FILESIZE = os.path.getsize(filepath)
SIZE = 1000000

import os
from tqdm import tqdm

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        file_size = os.path.getsize(filepath)
        progress = tqdm(total=file_size, unit="iB", unit_scale=True)
        start = time.time()
        with open(filepath, "rb") as f:
            for data in iter(lambda: f.read(SIZE), b''):  # читает данные из файла по 1400000 байтов за раз и продолжает это делать, пока не достигнет конца файла
                s.sendall(data)
                progress.update(len(data))
        print(f"Result time = {time.time() - start} seconds")
        progress.close()

        # data = s.recv(1024)

    # print(f"Received {data!r}")


if __name__ == "__main__":
    main()
