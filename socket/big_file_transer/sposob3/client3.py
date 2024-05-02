import os
import socket
import time

from tqdm import tqdm
import config

IP = socket.gethostbyname(socket.gethostname())
print(IP)
PORT = 4456
ADDR = (IP, PORT)
SIZE = 8192
FORMAT = "utf-8"
filepath = "/Users/aroslavsapoval/myProjects/data/images1000.zip"
FILENAME = os.path.basename(filepath)
FILESIZE = os.path.getsize(filepath)



def main():
    """TCP socket and connecting to the server"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создается объект сокета
    client.connect(ADDR) # подключение к серверу


    start = time.time()
    """ Sending the filename and filesize to the server. """
    data = f"{FILENAME}_{FILESIZE}"
    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"SERVER: {msg}")

    """ Data transfer. """
    # bar = tqdm(range(FILESIZE), f"Sending {FILENAME}", unit="B", unit_scale=True, unit_divisor=SIZE)

    with open(filepath, "rb") as f:
        while True:
            data = f.read(SIZE)

            if not data:
                break

            client.send(data)
            # msg = client.recv(SIZE).decode(FORMAT)

            # bar.update(len(data))
    print(f"Result time = {time.time()-start} seconds")
    """ Closing the connection """
    client.close()

if __name__ == "__main__":
    main()
