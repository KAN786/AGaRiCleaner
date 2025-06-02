from fastapi import FastAPI

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])