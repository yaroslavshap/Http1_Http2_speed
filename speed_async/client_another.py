import os
import httpx
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

client = httpx.Client()


def send_file(file_name, folder):
    file_path = os.path.join(folder, file_name)
    with open(file_path, "rb") as file:
        start_time = time.time()  # Засекаем время передачи
        response = client.post("http://127.0.0.1:8089/receive_images/", files={"file": file})
        end_time = time.time()  # Засекаем время завершения передачи
        transfer_time = end_time - start_time
        # print(f"Ответ сервера: {response.text} за {transfer_time} секунд, {response.http_version}")
        return transfer_time


async def send_files():
    folder = "/Users/aroslavsapoval/myProjects/data/images1000"
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f != ".DS_Store"]
    times = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        start_time = time.time()
        for i in range(0, len(files), 8):
            # Запуск задач асинхронно
            future1 = executor.submit(send_file, files[i], folder)
            future2 = executor.submit(send_file, files[i + 1], folder)
            future3 = executor.submit(send_file, files[i + 2], folder)
            future4 = executor.submit(send_file, files[i + 3], folder)
            future5 = executor.submit(send_file, files[i + 4], folder)
            future6 = executor.submit(send_file, files[i + 5], folder)
            future7 = executor.submit(send_file, files[i + 6], folder)
            future8 = executor.submit(send_file, files[i + 7], folder)
            # Получение результатов выполнения функций
            result1 = future1.result()
            result2 = future2.result()
            result3 = future3.result()
            result4 = future4.result()
            result5 = future5.result()
            result6 = future6.result()
            result7 = future7.result()
            result8 = future8.result()
            times.append(result1)
            times.append(result2)
            times.append(result3)
            times.append(result4)
            times.append(result5)
            times.append(result6)
            times.append(result7)
            times.append(result8)
            print(
                f"{files[i]} : {result1}, {files[i + 1]} : {result2}, {files[i + 2]} : {result3}, {files[i + 3]} : {result4},"
                f" {files[i + 4]} : {result5}, {files[i + 5]} : {result6}, {files[i + 6]} : {result7}, {files[i + 7]} : {result8}")
        end_time = time.time()
        rez_time = end_time - start_time
    print(rez_time)
    print(times)
    total_time = sum(times)
    print(f"Общее время - {total_time}, количество - {len(times)}")


if __name__ == "__main__":
    asyncio.run(send_files())
