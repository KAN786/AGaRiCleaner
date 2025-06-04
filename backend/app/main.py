from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.api.v1.endpoints import message, user, server
from gradio_client import Client




@asynccontextmanager
async def on_startup(app: FastAPI):
    init_db()
    app.state.client = Client("CLOUDYUL/AGaRiCleaner_Detector")

    yield

app = FastAPI(lifespan = on_startup) 


@app.get("/")
def read_root():
    return {"message": "SQLite + FastAPI connected!"}

app.include_router(message.router, prefix="/messages", tags=["Messages"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(server.router, prefix="/servers", tags=["Servers"])