import socket
from tqdm import tqdm
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 9000000
FORMAT = "utf-8"

def main():
    """ Creating a TCP server socket """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[+] Listening...")

    """ Принятие соединения от клиента """
    conn, addr = server.accept()
    print(f"[+] Client connected from {addr[0]}:{addr[1]}")


    while True:
        """ Получение имени файла и его размера от клиента """
        # data = conn.recv(SIZE).decode(FORMAT)



        data = b""
        while not data.endswith(b"\n"):
            chunk = conn.recv(1)  # получаем один байт за раз
            if not chunk:
                break
            data += chunk
        data = data.decode(FORMAT).strip()  # удаляем разделитель



        # Если данные пусты, клиент закрыл соединение, и мы выходим из цикла
        if not data:
            break

        item = data.split(":")
        FILENAME = item[0]
        FILESIZE = int(item[1])

        print(f"[+] Filename {FILENAME} and filesize {FILESIZE} received from the client.")
        # conn.send(f"Filename {FILENAME} and filesize {FILESIZE} received".encode(FORMAT))

        output_folder = "get_images"
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, FILENAME)
        with open(output_path, "wb") as f:
            bytes_received = 0
            while bytes_received < FILESIZE:
                data = conn.recv(min(SIZE, FILESIZE - bytes_received))
                if not data:
                    break
                f.write(data)
                bytes_received += len(data)



    """ Closing connection. """
    conn.close()
    server.close()

if __name__ == "__main__":
    main()
