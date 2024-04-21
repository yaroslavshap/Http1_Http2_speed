import grpc
from concurrent import futures
import my_pb2
import my_pb2_grpc
import os


class FileTransferService(my_pb2_grpc.FileTransferServiceServicer):

    def __init__(self):
        self.image_name = None

    def work_with_img(self, request, context, case_nom):
        image_bytes = request.image
        self.image_name = request.filename
        output_folder = f"images_case_{case_nom}"
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, self.image_name)
        with open(output_path, "wb") as file:
            file.write(image_bytes)


    def Case1(self, request, context):
        print(f"Пришедшее изображение: {request.filename}")
        #self.work_with_img(request, context, case_nom=1)
        response = my_pb2.FileResponse(message=f"Successfully {request.filename}")
        return response

    def Case2(self, request_iterator, context):
        all_img = []
        for request in request_iterator:
            print(f"Пришедшее изображение: {request.filename}")
            #self.work_with_img(request, context, case_nom=2)
            all_img.append(self.image_name)
        response = my_pb2.FileResponse(message=f"Successfully. You have sent {len(all_img)}")
        return response

    def Case4(self, request_iterator, context):
        for request in request_iterator:
            print(f"Пришедшее изображение: {request.filename}")
            self.work_with_img(request, context, case_nom=4)
            response = my_pb2.FileResponse(message=f"Received {request.filename}")
            yield response


def run_server():
    host = '127.0.0.1'
    port = '8099'

    # # Загрузите сертификаты
    # with open('/Users/aroslavsapoval/myProjects/Practic3/GRPC_practic/cert.pem', 'rb') as f:
    #     server_certificate = f.read()
    # with open('/Users/aroslavsapoval/myProjects/Practic3/GRPC_practic/key.pem', 'rb') as f:
    #     server_key = f.read()
    #
    # # Создайте учетные данные сервера
    # server_credentials = grpc.ssl_server_credentials(((server_key, server_certificate),))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         options=[('grpc.max_receive_message_length', 2000 * 1024 * 1024)])
    my_pb2_grpc.add_FileTransferServiceServicer_to_server(FileTransferService(), server)

    server.add_insecure_port(f'{host}:{port}')    # , server_credentials
    server.start()
    print(f"Сервер запущен на {host}:{port}") # http://{host}:{port}
    server.wait_for_termination()


if __name__ == '__main__':
    run_server()
