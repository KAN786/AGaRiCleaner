from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.api.v1.endpoints import message, user, server

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code here runs at startup
    init_db()
    yield # Code below here runs at shutdown (if needed)

app = FastAPI(lifespan = lifespan)



@asynccontextmanager
async def on_startup(app: FastAPI):
    init_db()

    
@app.get("/")
def read_root():
    return {"message": "SQLite + FastAPI connected!"}

app.include_router(message.router, prefix="/messages", tags=["Messages"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(server.router, prefix="/servers", tags=["Servers"])