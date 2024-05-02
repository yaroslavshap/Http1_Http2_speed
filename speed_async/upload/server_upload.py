from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse
import os
import uvicorn

import config

app = FastAPI()

async def work_with_image(file_data):
    data = await file_data.read()
    output_folder = "get_images"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, file_data.filename)
    with open(output_path, "wb") as file1:
        file1.write(data)


@app.post("/receive_images/")
async def receive_images(file_data: UploadFile):
    try:
        await work_with_image(file_data)
        print(f"{file_data.filename}")

        return JSONResponse("ок", status_code=200)
    except Exception as e:
        return JSONResponse({str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=config.port)

