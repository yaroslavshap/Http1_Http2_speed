from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from PIL import Image
import io
import asyncio
import uvicorn
import os


app = FastAPI()

# Глобальная переменная для отслеживания количества обрабатываемых изображений
processing_images = 0

async def process_image(file: io.BytesIO, filename):
    global processing_images
    processing_images += 1
    print(f"Начата обработка изображения. Всего обрабатывается изображений: {processing_images}")
    print(filename)
    # image = Image.open(file)
    # output_folder = "new_images"
    # os.makedirs(output_folder, exist_ok=True)
    # output_path = os.path.join(output_folder, filename)
    # image.save(output_path, format="PNG")
    processing_images -= 1
    print(f"Завершена обработка изображения. Всего обрабатывается изображений: {processing_images}")

@app.post("/receive_images/")
async def receive_images(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        image_stream = io.BytesIO(await file.read())  # Преобразуем асинхронный файл в синхронный поток
        background_tasks.add_task(process_image, image_stream, file.filename)  # Добавляем задачу на обработку изображения в фоне
        return {"message": f"Изображение {file.filename} успешно принято и будет обработано."}
    except Exception as e:
        return {"message": f"Ошибка в отправленном изображении: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8025)
