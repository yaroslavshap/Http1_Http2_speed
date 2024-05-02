import httpx
import time

import config


def send_file(client, file_path):
    with open(file_path, "rb") as file:
        file_content = file.read()
    start_time = time.time()
    response = client.post(config.server_url, data=file_content)
    end_time = time.time()
    print(f"Ответ сервера: {response.text} за {end_time - start_time} секунд, {response.http_version}")
    return end_time - start_time

def send_large_file():
    file_path = config.filepath
    with httpx.Client(timeout=360.0) as client:
        send_file(client, file_path)

if __name__ == "__main__":
    send_large_file()