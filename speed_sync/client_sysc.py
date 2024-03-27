import os
import httpx
import time

client = httpx.Client()


# http2=True, verify=False


def send_files():
    folder = "/Users/aroslavsapoval/myProjects/data/images1000"
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f != ".DS_Store"]
    total_time = 0
    for file_name in files:
        file_path = os.path.join(folder, file_name)
        with open(file_path, "rb") as file:
            start_time = time.time()  # Засекаем время передачи
            response = client.post("http://127.0.0.1:8089/receive_images/", files={"file": file})
            end_time = time.time()  # Засекаем время завершения передачи
            transfer_time = end_time - start_time
            total_time += transfer_time
            print(f"Ответ сервера: {response.text} за {transfer_time} секунд, {response.http_version}")
    print(f"Общее время - {total_time}")


if __name__ == "__main__":
    send_files()
