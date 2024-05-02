import httpx
import time
import os
from tqdm import tqdm
import config

def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def send_file(client, file_path):
    file_size = os.path.getsize(file_path)
    start_time = time.time()
    with open(file_path, "rb") as file:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc=file_path) as pbar:
            for chunk in read_in_chunks(file, 1024):
                response = client.post(config.server_url, data=chunk)
                pbar.update(len(chunk))
    end_time = time.time()
    print(f"Ответ сервера: {response.text} за {end_time - start_time} секунд, {response.http_version}")
    return end_time - start_time

def send_large_file():
    file_path = config.filepath
    with httpx.Client(timeout=360.0) as client:
        send_file(client, file_path)

if __name__ == "__main__":
    send_large_file()
