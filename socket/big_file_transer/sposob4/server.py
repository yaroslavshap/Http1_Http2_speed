import socket
HOST = "127.0.0.1"
PORT = 4453
SIZE = 1000000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("[+] Listening...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            with open(f"../recv_images1000.zip", "wb") as f:
                while True:
                    data = conn.recv(SIZE)
                    if not data:
                        break
                    f.write(data)



if __name__ == "__main__":
    main()
