from os import getcwd

from fastapi import FastAPI, UploadFile, File, HTTPException
from starlette.responses import StreamingResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/video/{video_name}")
async def get_video(video_name: str):
    def iterfile():
        with open(getcwd() + '\\videos\\' + video_name + '.mp4', mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="video/mp4")


@app.post("/video/")
async def upload(file: UploadFile = File(...)):
    contents = file.file.read()
    print(file.filename.split('.')[-1])
    if file.filename.split('.')[-1] != 'mp4':
        file.file.close()
        raise HTTPException(status_code=422, detail="The file format must be MP4 only")
    with open(getcwd() + '\\videos\\' + file.filename, 'wb') as f:
        f.write(contents)
    file.file.close()
    return {"message": f"Successfully uploaded {file.filename}"}
