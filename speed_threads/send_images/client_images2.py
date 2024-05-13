import os
from concurrent import futures
import httpx
import time
import numpy as np
import config


def send_file(client, data, filename):
    filename_bytes = filename.encode('utf-8')
    data_to_send = filename_bytes + b'\0' + data
    start_time = time.time()
    response = client.post(config.server_url, data=data_to_send)
    end_time = time.time()
    print(f"Ответ сервера: {response.text} за {end_time - start_time} секунд, {response.http_version}")
    return end_time - start_time


def send_files():
    client = httpx.Client()
    files = [f for f in os.listdir(config.folder) if os.path.isfile(os.path.join(config.folder, f))]
    times = []
    start = time.time()
    with futures.ThreadPoolExecutor(max_workers=None) as executor:
        future_to_patch = {executor.submit(send_file,
                                           client,
                                           open(os.path.join(config.folder, file_name), "rb").read(),
                                           file_name): file_name for file_name in files}

        for future in futures.as_completed(future_to_patch):
            res = future.result()
            print(res)
            times.append(res)

    total_time = sum(times)


    print(f"Общее время - {total_time}, Среднее время - {np.mean(times)}, Медиана - {np.median(times)}, количество - {len(times)}")
    print(f"Result time = {time.time()-start} seconds")


if __name__ == "__main__":
    send_files()
