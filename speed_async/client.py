import os
import httpx
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

client = httpx.Client()


def send_file(file_name):
    folder = "/Users/aroslavsapoval/myProjects/data/images1000"
    file_path = os.path.join(folder, file_name)
    with open(file_path, "rb") as file:
        start_time = time.time()  # Засекаем время передачи
        response = client.post("http://127.0.0.1:8089/receive_images/", files={"file": file})
        end_time = time.time()  # Засекаем время завершения передачи
        transfer_time = end_time - start_time
        print(f"Ответ сервера: {response.text} за {transfer_time} секунд, {response.http_version}")
        return transfer_time


async def send_files():
    folder = "/Users/aroslavsapoval/myProjects/data/images1000"
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f != ".DS_Store"]

    with ThreadPoolExecutor(max_workers=None) as executor:
        start_time = time.time()
        times = list(executor.map(send_file, files))
        end_time = time.time()
        rez_time = end_time - start_time

    print(rez_time)
    print(times)
    total_time = sum(times)
    print(f"Общее время - {total_time}, количество - {len(times)}")


if __name__ == "__main__":
    asyncio.run(send_files())
