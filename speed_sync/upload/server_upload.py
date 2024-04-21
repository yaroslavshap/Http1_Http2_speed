from fastapi import FastAPI, UploadFile, File
import os
import uvicorn

app = FastAPI()


def work_with_img(file):
    image_bytes = file.read()
    output_folder = "get_images"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, file.filename)
    with open(output_path, "wb") as file1:
        file1.write(image_bytes)

@app.post("/receive_images/")
def receive_images(file: UploadFile = File(...)):
    try:
        work_with_img(file)
        return f"Изображение {file.filename} принято"
    except Exception as e:
        return {"message": f"Error receiving and processing images: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8089)
