import os
import httpx
import time
import config

client = httpx.Client()


def send_file(client, data, filename):
    filename_bytes = filename.encode('utf-8')
    data_to_send = filename_bytes + b'\0' + data
    start_time = time.time()
    response = client.post(config.server_url, data=data_to_send)
    end_time = time.time()
    print(f"Ответ сервера: {response.text} за {end_time - start_time} секунд, {response.http_version}")
    return end_time - start_time


def send_files():
    files = [f for f in os.listdir(config.folder) if os.path.isfile(os.path.join(config.folder, f)) and f != ".DS_Store"]
    total_time = 0
    for file_name in files:
        file_path = os.path.join(config.folder, file_name)
        with open(file_path, "rb") as file:
            file_to_send = file.read()
            total_time = total_time + send_file(client, file_to_send, file_name)
    print(f"Общее время - {total_time}")




if __name__ == "__main__":
    send_files()
