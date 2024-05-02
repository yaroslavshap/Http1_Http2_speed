import os
import httpx
import time
import requests
import config


def send_files(mayak):
    files = [f for f in os.listdir(config.folder) if os.path.isfile(os.path.join(config.folder, f)) and f != ".DS_Store"]
    total_time = 0
    for file_name in files:
        file_path = os.path.join(config.folder, file_name)
        print(file_path)

        if mayak == True:
            with open(file_path, "rb") as file:
                start_time = time.time()
                response = requests.post(config.server_url, files={"file": file})
                end_time = time.time()
                transfer_time = end_time - start_time
                total_time += transfer_time
                print(f"Ответ сервера: {response.text} за {transfer_time} секунд, HTTP/{response.raw.version}")

        elif mayak == False:
            with open(file_path, "rb") as file:
                file_r = file.read()
                start_time = time.time()
                response = requests.post(config.server_url2, files={"file": file_r}, data={"filename": file_name})
                end_time = time.time()
                transfer_time = end_time - start_time
                total_time += transfer_time
                print(f"Ответ сервера: {response.text} за {transfer_time} секунд, HTTP/{response.raw.version}")

    print(f"Общее время - {total_time}")


if __name__ == "__main__":
    send_files(mayak=False)
