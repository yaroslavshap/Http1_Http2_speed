from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
import os
import uvicorn

app = FastAPI()





async def work_with_img(file, filename):
    output_folder = "transferred_file"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, filename.decode('utf-8'))
    with open(output_path, "wb") as file1:
        file1.write(file)

@app.post("/receive_images/")
async def receive_images(request: Request):
    try:
        data = await request.body()
        file_name, file_data = data.split(b'\0', 1)
        await work_with_img(file_data, file_name)
        return JSONResponse("200", status_code=200)
    except Exception as e:
        return JSONResponse("!", status_code=500)






#
# async def work_with_img(file):
#     image_bytes = await file.read()
#     output_folder = "transferred_file"
#     os.makedirs(output_folder, exist_ok=True)
#     output_path = os.path.join(output_folder, file.filename)
#     with open(output_path, "wb") as file1:
#         file1.write(image_bytes)
#
# @app.post("/receive_images/")
# async def receive_images(file: UploadFile = File()):
#     try:
#         await work_with_img(file)
#         return f"Файл {file.filename} принят"
#     except Exception as e:
#         return {"message": f"Ошибка: {str(e)}"}






#
# def work_with_img(file):
#     image_bytes = file.file.read()  # синхронное чтение файла
#     output_folder = "transferred_file"
#     os.makedirs(output_folder, exist_ok=True)
#     output_path = os.path.join(output_folder, file.filename)
#     with open(output_path, "wb") as file1:
#         file1.write(image_bytes)
#
# @app.post("/receive_images/")
# def receive_images(file: UploadFile = File(...)):
#     try:
#         work_with_img(file)
#         return f"Файл {file.filename} принят"
#     except Exception as e:
#         return {"message": f"Ошибка: {str(e)}"}




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8099)


