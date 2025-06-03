from fastapi import FastAPI

from backend.app.api.v1.endpoints import endpoints
app = FastAPI()

app.include_router(endpoints.router, prefix="/users", tags=["Users"])
app.include_router(endpoints.router, prefix="/messages", tags=["Messages"])