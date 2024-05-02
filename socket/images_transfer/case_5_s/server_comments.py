import socket
import struct
import os

class ServerSocket():
    def __init__(self, sock):
        self._sock = sock

    def recvall(self, n):
        print("n = ", n) # размер данных в байтах который нам нужно получить (то есть говорим что нужно получить 6425335 байт данных)
        data = b''
        while len(data) < n: # цикл пока уже полученные данные не сравняются с данными которые нам нужно получить
            packet = self._sock.recv(n - len(data)) # принимаем данные в размере (какой бы нам хотелось (всего сколько нужно данных минус размер тех которые уже получили)
            print(f"Say that we can get = {n - len(data)}") # говорим что нам нужно например 6425335
            print(f"Actually get = {len(packet)}") # но присылает клиент нам меньше данных (по разным причинам) например 179648
            if not packet:
                return None
            data += packet
            print("Now DATA = ", len(data))
        return data

    def recv_msg(self):
        print("I am in (recv_msg)")
        print("New Image")
        raw_msglen = self.recvall(4) # (b'\x00b\n\xf7') байтовое представление размера 1 изображения (то есть мы приняли размер изображения и тут оно записано в виде байтовой строки, а не числом)
        # raw_msglen = self.recvall(8)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0] # (6425335) раскодировали этот размер, теперь он в виде числа
        print("msglen = struct.unpack('>I', raw_msglen)[0] = ", struct.unpack('>I', raw_msglen)[0])
        # msglen = struct.unpack('>Q', raw_msglen)[0]
        data = self.recvall(msglen) # передаем количество данных которое нужно получить (6425335)
        return data # возвращаем полученные данные изображения в виде байтов

    def recv_images(self, output_dir):
        i = 0
        output_folder = "get_images"
        os.makedirs(output_folder, exist_ok=True)
        while True:
            data = self.recv_msg()
            if data is None:
                break
            with open(os.path.join(output_folder, f'image_{i}.jpg'), 'wb') as f:
                f.write(data)
            i += 1

def main():
    HOST = "127.0.0.1"
    PORT = 4456
    output_dir = "/Users/aroslavsapoval/myProjects/Http1_Http2_speed/socket/images_transfer/case_5_s/get_images"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server is listening...")
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            server = ServerSocket(conn)
            server.recv_images(output_dir)

if __name__ == "__main__":
    main()
