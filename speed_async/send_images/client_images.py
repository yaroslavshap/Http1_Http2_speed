import os
import httpx
import asyncio
import time
import aiofiles
import config


async def send_file(client, data, filename):
    filename_bytes = filename.encode('utf-8')
    data_to_send = filename_bytes + b'\0' + data
    start_time = time.time()
    response = await client.post(config.server_url, data=data_to_send)
    end_time = time.time()
    print(f"Ответ сервера: {response.text} за {end_time - start_time} секунд, {response.http_version}")
    return end_time - start_time


async def send_files():
    folder = config.folder
    files = [f for f in os.listdir(config.folder) if os.path.isfile(os.path.join(config.folder, f)) and f != ".DS_Store"]
    async with httpx.AsyncClient(timeout=160.0) as client:
        tasks = []
        start = time.time()
        for file_name in files:
            file_path = os.path.join(folder, file_name)
            async with aiofiles.open(file_path, "rb") as file:
                file_content = await file.read()
                tasks.append(asyncio.create_task(send_file(client, file_content, file_name)))
        times = await asyncio.gather(*tasks)
        print(f"Result time = {time.time()-start} seconds")

    total_time = sum(times)
    print(f"Общее время - {total_time}")

if __name__ == "__main__":
    asyncio.run(send_files())
