import socket
import struct
import os
import time
from tqdm import tqdm
import config


class ClientSocket():
    def __init__(self, sock):
        self._sock = sock

    def send_msg(self, msg):
        msg = struct.pack('>I', len(msg)) + msg
        # msg = struct.pack('>Q', len(msg)) + msg
        # self._sock.send(msg)
        self._sock.sendall(msg)


    def send_images(self, image_paths):
        for image_path in tqdm(image_paths, unit="image"):
            with open(image_path, 'rb') as f:
                data = f.read()
                self.send_msg(data)

def main():
    HOST = "127.0.0.1"
    PORT = 4456
    image_dir = config.folder
    image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    # print(f"Размер файла '{os.path.basename(image_paths[0])}' составляет {os.path.getsize(image_paths[0])} байт или {os.path.getsize(image_paths[0]) / 1048576} мегабайт.")
    # image_paths = [config.filepath]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        client = ClientSocket(s)
        start = time.time()
        client.send_images(image_paths)
        print(f"Result time = {time.time()-start} seconds")


if __name__ == "__main__":
    main()
