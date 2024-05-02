import os
import socket
import time
import config

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 8192
FORMAT = "utf-8"

def send_file(conn, filepath):
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    conn.send(f"{filename}:{filesize}".encode(FORMAT))
    msg = conn.recv(SIZE).decode(FORMAT)
    print(f"SERVER: {msg}")

    with open(filepath, 'rb') as f:
        bytes_to_send = filesize
        while bytes_to_send != 0:
            chunk = f.read(min(bytes_to_send, SIZE))
            conn.send(chunk)
            bytes_to_send -= len(chunk)

def client_program():
    client = socket.socket()
    client.connect(ADDR)

    directory = config.folder
    start = time.time()
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            send_file(client, os.path.join(directory, filename))

    print(f"Result transfer time = {time.time() - start} seconds")
    client.close()

if __name__ == '__main__':
    client_program()
