import socket
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 8192
FORMAT = "utf-8"

def receive_file(conn, filename, filesize):
    output_folder = "get_images"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, filename)
    with open(output_path, 'wb') as f:
        bytes_received = 0
        while bytes_received < filesize:
            bytes_to_receive = min(filesize - bytes_received, SIZE)
            chunk = conn.recv(bytes_to_receive)
            f.write(chunk)
            bytes_received += len(chunk)

def server_program():
    server = socket.socket()
    server.bind(ADDR)
    server.listen()
    print("Server is listening...")

    conn, address = server.accept()
    print(f"Connected to {address}")

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        if not data:
            break
        filename, filesize = data.split(":")
        filesize = int(filesize)
        print(f"Received filename {filename} and filesize {filesize}")
        conn.send("Data received.".encode(FORMAT))
        receive_file(conn, filename, filesize)

    conn.close()

if __name__ == '__main__':
    server_program()
