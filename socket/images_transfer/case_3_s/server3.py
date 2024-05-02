import socket
from tqdm import tqdm
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def main():
    """ Creating a TCP server socket """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создем объект сокета
    server.bind(ADDR)
    server.listen()
    print("[+] Listening...")

    """ Принятие соединения от клиента """
    conn, addr = server.accept()
    print(f"[+] Client connected from {addr[0]}:{addr[1]}")

    while True:
            data = b""
            while not data.endswith(b"\n"):
                chunk = conn.recv(SIZE)
                data += chunk
                if b"\n" in chunk:
                    # Если символ новой строки присутствует в блоке, разбиваем данные на две части
                    data, file_data = data.rsplit(b"\n", 1)
                    break
            data = data.decode(FORMAT)

            if not data:
                break

            FILENAME, FILESIZE = data.split(":")
            FILESIZE = int(FILESIZE)

            print(f"[+] Filename {FILENAME} and filesize {FILESIZE} received from the client.")
            output_folder = "get_images"
            os.makedirs(output_folder, exist_ok=True)
            output_path = os.path.join(output_folder, FILENAME)
            with open(output_path, "wb") as f:
                # Если есть данные файла в блоке, записываем их в файл
                if file_data:
                    f.write(file_data)
                bytes_received = len(file_data)
                while bytes_received < FILESIZE:
                    to_receive = min(SIZE, FILESIZE - bytes_received)
                    data = conn.recv(to_receive)
                    if not data:
                        break
                    f.write(data)
                    bytes_received += len(data)



    """ Closing connection. """
    conn.close()
    server.close()

if __name__ == "__main__":
    main()
