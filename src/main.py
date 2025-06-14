from fastapi import FastAPI

from src.api.router import router as bot_router
from src.logging import configure_logging, LogLevel

configure_logging(LogLevel.DEBUG)
app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello World"}


app.include_router(bot_router)
