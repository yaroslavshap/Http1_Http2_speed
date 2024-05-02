import os
import socket
import time
from tqdm import tqdm
import config

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 9000000
FORMAT = "utf-8"


def main():
    """TCP socket and connecting to the server"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    files = [f for f in os.listdir(config.folder) if os.path.isfile(os.path.join(config.folder, f)) and f != ".DS_Store"]
    start = time.time()
    for file_name in files:
        file_path = os.path.join(config.folder, file_name)
        filesize = os.path.getsize(file_path)

        """ Sending the filename and filesize to the server. """
        # data = f"{file_name}:{filesize}"
        data = f"{file_name}:{filesize}\n"  # добавляем разделитель после каждого файла
        client.send(data.encode(FORMAT))
        # msg = client.recv(SIZE).decode(FORMAT)
        # print(f"SERVER: {msg}")

        """ Data transfer. """
        with open(file_path, "rb") as f:
            while True:
                data = f.read(SIZE)

                if not data:
                    break

                client.send(data)
    end = time.time()
    rez_time = end-start
    print("Result", rez_time, "sec")
    """ Closing the connection """
    client.close()


if __name__ == "__main__":
    main()
