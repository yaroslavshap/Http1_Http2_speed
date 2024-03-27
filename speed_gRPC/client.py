import math
import grpc
from my_pb2 import FileRequest
from my_pb2_grpc import FileTransferServiceStub
from os.path import join
import time
import os



def get_client_stream_requests(images, path, stub):
    for file_name in images:
        file_path = os.path.join(path, file_name)
        with open(file_path, "rb") as file:
            image_bytes = file.read()
        request = FileRequest(image=image_bytes, filename=file_name)
        yield request


# поток от клиента
def run_client_case2(files, path, stub):
    start_time = time.time()
    result = stub.Case2(get_client_stream_requests(files, path, stub))
    end_time = time.time()
    res_time = end_time - start_time
    print(f"Способ 2: {result.message}")
    return res_time

# двунаправленный поток
def run_client_case4(images, path, stub):
    all_resp = []
    start_time = time.time()  # Засекаем начальное время перед отправкой
    response_stream = stub.Case4(get_client_stream_requests(images, path, stub))
    for response in response_stream:
        all_resp.append(response)
    print("Ответ от сервера: ", len(all_resp))
    end_time = time.time()  # Засекаем время после получения ответа
    res_time = end_time - start_time
    return res_time



# унарная передача
def run_client_case1(files, path, stub):
    all_time = []
    for file_name in files:
        file_path = os.path.join(path, file_name)
        with open(file_path, "rb") as file:
            image_bytes = file.read()
        request = FileRequest(image=image_bytes, filename=file_name)

        start_time = time.time()  # Засекаем начальное время перед отправкой
        result = stub.Case1(request)
        # print(f"Способ 1: {result.message}")
        end_time = time.time()  # Засекаем время после получения ответа
        res_time = end_time - start_time
        all_time.append(res_time)
        vrem = math.fsum(all_time)
    return vrem




def run():
    host = '127.0.0.1'
    port = '8099'
    # Устанавливаем максимальный размер сообщения на клиенте в 2000 МБ
    max_message_length = 2000 * 1024 * 1024
    channel = grpc.insecure_channel(f'{host}:{port}', options=(('grpc.max_send_message_length', max_message_length),))
    stub = FileTransferServiceStub(channel)
    images_folder = "/Users/aroslavsapoval/myProjects/data/images1000"
    images = [f for f in os.listdir(images_folder) if
              os.path.isfile(os.path.join(images_folder, f)) and f != ".DS_Store"]
    all_time = []
    kol = 5
    for i in range(kol):
        print(f"Попытка {i+1}")
        vremya_rez = run_client_case4(images, images_folder, stub)
        sred_time = vremya_rez / len(images)
        all_time.append(vremya_rez)
        print(f"Общее время: {vremya_rez}, Среднее время: {sred_time}")
    k = 1
    for i in all_time:
        print(f"Среднее время {k} попытки - {i}")
        k += 1
    print(f"Среднее время за {kol} попыток: {math.fsum(all_time) / len(all_time)}")


if __name__ == '__main__':
    run()
