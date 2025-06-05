from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.api.v1.endpoints import user_endpoints, gpt_endpoints
from gradio_client import Client
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    agaricleaner_url: str
    openai_api_key: str
    assistant_id: str

    class Config:
        env_file = ".env"


@asynccontextmanager
async def on_startup(app: FastAPI):
    init_db()
    app.state.settings = Settings()
    app.state.client = Client(app.state.settings.agaricleaner_url)


    yield

app = FastAPI(lifespan = on_startup) 


@app.get("/")
def read_root():
    return {"message": "SQLite + FastAPI connected!"}

app.include_router(user_endpoints.router, prefix="/users", tags=["Users"])
app.include_router(gpt_endpoints.router, prefix="/gpt", tags=["GPT"])