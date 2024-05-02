from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import uvicorn

import config

app = FastAPI()


async def work_with_img(file_data, file_name):

    output_folder = config.received_images_folder
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, file_name.decode('utf-8'))
    with open(output_path, "wb") as file1:
        file1.write(file_data)


@app.post("/receive_images/")
async def receive_images(request: Request):
    try:
        data = await request.body()
        file_name, file_data = data.split(b'\0', 1)
        await work_with_img(file_data, file_name)
        return JSONResponse("1000", status_code=200)
    except Exception as e:
        return JSONResponse("!", status_code=500)



if __name__=="__main__":
    uvicorn.run(app, host=config.host, port=config.port)