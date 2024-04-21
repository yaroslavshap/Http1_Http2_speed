import httpx
import time
import config
import os
import numpy as np
import asyncio

client = httpx.Client(timeout=240.0) # http2=True, verify=False, cert=("cert.pem", "key.pem"),



async def send_file1():
    try:
        with open(config.filepath, "rb") as file:
            start_time = time.time()
            response = client.post(config.server_url, files={"file": file})
            end_time = time.time()
            print(f"{end_time - start_time} секунд")
            print(response.http_version)
        if response.status_code == 200:
            print(f"Ответ сервера: {response.text} за {round(end_time - start_time, 5)} секунд, {response.http_version}")
        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Ошибка отправки: {e}")
    return round(end_time - start_time, 5)


async def send_file2():
    end_time = None
    start_time = None
    try:
        with open(config.filepath, "rb") as file:
            data_to_send = file.read()
            filename_bytes = os.path.basename(config.filepath).encode('utf-8')
            print(filename_bytes)
            data_to_send = filename_bytes + b'\0' + data_to_send
            start_time = time.time()
            response = client.post(config.server_url, data=data_to_send)
            end_time = time.time()
            print(f"{end_time - start_time} секунд")
            print(response.http_version)
        if response.status_code == 200:
            print(f"Ответ сервера: {response.text} за {round(end_time - start_time, 5)} секунд, {response.http_version}")
        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Ошибка отправки: {e}")
    return round(end_time - start_time, 5) if end_time else None


if __name__ == "__main__":
    total_time = []
    kol = 5
    for i in range(kol):
        total_time.append(asyncio.run(send_file2()))
    print(f"Время передачи файлов - {total_time}; Среднее время: {np.mean(total_time)}")
