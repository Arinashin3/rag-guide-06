"""실습 콘솔 서버 (내 PC 전용). app/main.py 와 별개이며 EKS 에는 올리지 않습니다."""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.dev import router

app = FastAPI(title="rag-guide 실습 콘솔")
app.include_router(router)
app.mount("/ui", StaticFiles(directory="app/static", html=True), name="ui")


@app.get("/")
def home():
    return RedirectResponse("/ui/")
