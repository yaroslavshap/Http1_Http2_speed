import os
import httpx
import asyncio
import time
import numpy as np
import config

async def send_file(client, data, filename):
    filename_bytes = filename.encode('utf-8')
    data_to_send = filename_bytes + b'\0' + data
    start_time = time.time()
    print("---")
    response = await client.post(config.server_url, data=data_to_send)
    end_time = time.time()
    print(f"Ответ сервера: {response.text} за {end_time - start_time} секунд, {response.http_version}")
    return end_time - start_time

async def send_files():
    files = [f for f in os.listdir(config.folder) if os.path.isfile(os.path.join(config.folder, f)) and f != ".DS_Store"]
    async with httpx.AsyncClient() as client:
        tasks = [send_file(client, open(os.path.join(config.folder, file_name), "rb").read(), file_name) for file_name in files]
        print("+++++")
        times = await asyncio.gather(*tasks)

    total_time = sum(times)
    print(f"Общее время - {total_time}, Среднее время - {np.mean(times)}, Медиана - {np.median(times)}, количество - {len(times)}")

if __name__ == "__main__":
    asyncio.run(send_files())
