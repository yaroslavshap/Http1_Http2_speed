from fastapi import FastAPI, UploadFile, File, Form
import os
import uvicorn
from PIL import Image
import config

app = FastAPI()


def work_with_img_upload_bytes(file:bytes, filename):
    output_folder = "saved_images_upload_bytes"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, filename)
    with open(output_path, "wb") as file1:
        file1.write(file)

def work_with_img_upload(file):
    image = Image.open(os.path.join(config.folder, file.filename))
    output_folder = "saved_images_upload"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{file.filename}")
    image.save(output_path, format="PNG")

@app.post("/receive_images/")
def receive_images(file: UploadFile):
    try:
        print("Filename - ", file.filename)
        work_with_img_upload(file)
        return f"Изображение {file.filename} принято"
    except Exception as e:
        return {"message": f"Error receiving and processing images: {str(e)}"}

@app.post("/receive_images2/")
def receive_images(file: bytes = File(...), filename: str = Form(...)):
    try:
        print("Filename - ", filename)
        work_with_img_upload_bytes(file, filename)
        return f"Изображение {filename} принято"
    except Exception as e:
        return {"message": f"Error receiving and processing images: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)