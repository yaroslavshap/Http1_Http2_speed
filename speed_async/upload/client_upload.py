import os
import httpx
import asyncio
import time

import config

client = httpx.AsyncClient()


async def send_files(mayak):
    files = [f for f in os.listdir(config.folder) if os.path.isfile(os.path.join(config.folder, f)) and f != ".DS_Store"]
    total_time = 0
    for file_name in files:
        file_path = os.path.join(config.folder, file_name)
        print(file_path)

        if mayak == True:
            with open(file_path, "rb") as file:
                # file = file.read()
                start_time = time.time()
                # response = await client.post(config.server_url, files={"file": file})
                response = await client.post(config.server_url, files={"file_data": file})
                end_time = time.time()
                transfer_time = end_time - start_time
                total_time += transfer_time
                print(f"Ответ сервера: {response.text} за {transfer_time} секунд, {response.http_version}")

        elif mayak == False:
            with open(file_path, "rb") as file:
                file_content = file.read()
                start_time = time.time()  # Засекаем время передачи
                response = await client.post(config.server_url2, files={"file": file_content}, data={"filename": file_name})
                end_time = time.time()  # Засекаем время завершения передачи
                transfer_time = end_time - start_time
                total_time += transfer_time
                print(f"Ответ сервера: {response.text} за {transfer_time} секунд, {response.http_version}")

    print(f"Общее время - {total_time}")


if __name__ == "__main__":
    asyncio.run(send_files(mayak=True))
