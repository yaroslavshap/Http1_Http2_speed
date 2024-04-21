import os
from concurrent import futures
import httpx
import asyncio
import time
import numpy as np
import config

# http2=True, verify=False, cert=("cert.pem", "key.pem")


# def send_file(client, data, filename):
#     filename_bytes = filename.encode('utf-8')
#     data_to_send = filename_bytes + b'\0' + data
#     start_time = time.time()  # Засекаем время передачи
#     response = client.post(config.server_url, data=data_to_send)
#     end_time = time.time()  # Засекаем время завершения передачи
#     print(f"Ответ сервера: {response.text} за {end_time - start_time} секунд, {response.http_version}")
#     return end_time - start_time

#
def send_file(client, file_path):
    with open(file_path, "rb") as f:
        data = {"file_data": f.read(), "file_name": os.path.basename(file_path)}
        start_time = time.time()  # Засекаем время передачи
        response = client.post(config.server_url, data=data)
        end_time = time.time()  # Засекаем время завершения передачи
    return end_time - start_time


def send_files():
    client = httpx.Client()
    files = [f for f in os.listdir(config.folder) if os.path.isfile(os.path.join(config.folder, f)) and f != ".DS_Store"]
    times = []
    start = time.time()
    with futures.ThreadPoolExecutor(max_workers=None) as executor:
        # future_to_patch = {executor.submit(send_file, client, open(os.path.join(config.folder, file_name), "rb").read(), file_name): file_name for file_name in files}
        future_to_patch = {executor.submit(send_file, client, os.path.join(config.folder, file_name)): file_name for file_name in files}

        for future in futures.as_completed(future_to_patch):
            res = future.result()
            print(res)
            times.append(res)
    print(f"Результат {time.time()-start}")

    total_time = sum(times)
    print(f"Общее время - {total_time}, Среднее время - {np.mean(times)}, Медиана - {np.median(times)}, количество - {len(times)}")


if __name__ == "__main__":
    send_files()
