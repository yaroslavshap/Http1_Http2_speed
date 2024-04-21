import os
import httpx
import asyncio
import time
from concurrent import futures

import config

client = httpx.Client()


def send_file(file_name):
    file_path = os.path.join(config.folder, file_name)
    with open(file_path, "rb") as file:
        start_time = time.time()  # Засекаем время передачи
        response = client.post(config.server_url, files={"file": file})
        end_time = time.time()  # Засекаем время завершения передачи
        transfer_time = end_time - start_time
        print(f"Ответ сервера: {response.text} за {transfer_time} секунд, {response.http_version}")
        return transfer_time


async def send_files():
    files = [f for f in os.listdir(config.folder) if os.path.isfile(os.path.join(config.folder, f)) and f != ".DS_Store"]

    with futures.ThreadPoolExecutor(max_workers=None) as executor:
        times = list(executor.map(send_file, files))
        for future in futures.as_completed(times):
            res = future.result()
            print(res)
            times.append(res)


    print(times)
    total_time = sum(times)
    print(f"Общее время - {total_time}, количество - {len(times)}")


if __name__ == "__main__":
    asyncio.run(send_files())
