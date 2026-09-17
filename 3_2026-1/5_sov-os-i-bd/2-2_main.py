import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Учебный HTTP-сервис работает", "pid": os.getpid()}

@app.get("/health")
def health():
    return {"status": "ok", "pid": os.getpid()}
