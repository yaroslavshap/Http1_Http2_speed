from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
import os
import uvicorn

app = FastAPI()


async def work_with_img(file):
    # Сохраняем полученные изображения на диск
    image_bytes = await file.read()
    output_folder = "get_images"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, file.filename)
    with open(output_path, "wb") as file1:
        file1.write(image_bytes)


@app.post("/receive_images/")
async def receive_images(file: UploadFile = File(...)):
    try:
        #await work_with_img(file)
        print(f"{file.filename}")

        return f"Изображение {file.filename} принято"
    except Exception as e:
        return {"message": f"Error receiving and processing images: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8089)