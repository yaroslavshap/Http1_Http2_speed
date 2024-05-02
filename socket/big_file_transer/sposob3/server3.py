import socket
from tqdm import tqdm

IP = socket.gethostbyname(socket.gethostname())
print(socket.gethostname())
print(IP)
PORT = 4456
ADDR = (IP, PORT)
SIZE = 8192
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

    """ Получение имени файла и его размера от клиента """
    data = conn.recv(SIZE).decode(FORMAT)
    item = data.split("_")
    FILENAME = item[0]
    FILESIZE = int(item[1])

    print(f"[+] Filename {FILENAME} and filesize {FILESIZE} received from the client.")
    conn.send(f"Filename {FILENAME} and filesize {FILESIZE} received".encode(FORMAT))

    """ Data transfer """
    bar = tqdm(range(FILESIZE), f"Receiving {FILENAME}", unit="B", unit_scale=True, unit_divisor=SIZE)

    with open(f"recv_{FILENAME}", "wb") as f:
        while True:
            data = conn.recv(SIZE)

            if not data:
                break

            f.write(data)
            # Убираем подтверждения после каждой отправки данных и время ускоряется очень сильно
            # conn.send("Data received.".encode(FORMAT))

            bar.update(len(data))

    """ Closing connection. """
    conn.close()
    server.close()

if __name__ == "__main__":
    main()
