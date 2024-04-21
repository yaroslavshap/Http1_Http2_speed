import os
import httpx
import time

import config

client = httpx.Client() #http2=True, verify=False, cert=("cert.pem", "key.pem")


def send_files():
    files = [f for f in os.listdir(config.folder) if os.path.isfile(os.path.join(config.folder, f)) and f != ".DS_Store"]
    total_time = 0
    for file_name in files:
        file_path = os.path.join(config.folder, file_name)
        with open(file_path, "rb") as file:
            data = {"file_data": file.read(), "file_name": file_name}
            start_time = time.time()  # Засекаем время передачи
            response = httpx.post(config.server_url, data=data)
            end_time = time.time()  # Засекаем время завершения передачи
            transfer_time = end_time - start_time
            total_time += transfer_time
            print(f"Ответ сервера: {response.text} за {transfer_time} секунд, {response.http_version}")
    print(f"Общее время - {total_time}")


if __name__ == "__main__":
    send_files()
