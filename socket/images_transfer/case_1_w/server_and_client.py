import asyncio
import time

import websockets
import os
import config

# Код сервера
async def server(websocket, path):
    while True:
        filename = await websocket.recv()
        # Получаем данные изображения от клиента
        data = await websocket.recv()
        # Сохраняем данные обратно в изображение

        output_folder = "get_images"
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, filename)
        with open(output_path, "wb") as f:
            f.write(data)
        # Отправляем обратно сообщение об успешной передаче
        await websocket.send("Изображение успешно получено!")

start_server = websockets.serve(server, "localhost", 8765, max_size=100**7)

# Код клиента
async def client():
    uri = "ws://localhost:8765"
    folder = config.folder
    files = [f for f in os.listdir(config.folder) if
             os.path.isfile(os.path.join(config.folder, f)) and f != ".DS_Store"]
    async with websockets.connect(uri, max_size=100**7) as websocket:
        # Перебираем все изображения в директории
        start = time.time()
        for filename in files:
            file_path = os.path.join(folder, filename)
            await websocket.send(filename)
            # Открываем каждое изображение и отправляем его данные на сервер
            with open(file_path, "rb") as img_file:
                await websocket.send(img_file.read())
                # Получаем ответ от сервера
                response = await websocket.recv()
                print(response)

        end = time.time()
        result_time = end - start
        print("Result ", result_time, " seconds")
# Запускаем сервер и клиента
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(client())
asyncio.get_event_loop().run_forever()
