import os
import httpx
import asyncio
import time

client = httpx.AsyncClient(timeout=160.0)
# http2=True, verify=False,

async def send_file(file_name, folder):
    file_path = os.path.join(folder, file_name)
    with open(file_path, "rb") as file:
        start_time = time.time()  # Засекаем время передачи
        response = await client.post("http://127.0.0.1:8025/receive_images/", files={"file": file})
        end_time = time.time()  # Засекаем время завершения передачи
        transfer_time = end_time - start_time
        print(f"Ответ сервера: {response.text} за {transfer_time} секунд, {response.http_version}")
        return transfer_time

async def send_files():
    folder = "/Users/aroslavsapoval/myProjects/data/images1000"
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    tasks = [asyncio.ensure_future(send_file(file_name, folder)) for file_name in files]
    times = await asyncio.gather(*tasks)

    total_time = sum(times)
    print(f"Общее время - {total_time}")

if __name__ == "__main__":
    asyncio.run(send_files())
