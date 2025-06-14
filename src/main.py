from fastapi import FastAPI

from src.api.bots.router import router as bot_router
from src.api.tasks.router import router as task_router
from src.api.bot_auth.router import router as bot_auth_router
from src.logging import configure_logging, LogLevel

configure_logging(LogLevel.DEBUG)
app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello World"}


app.include_router(bot_router)
app.include_router(task_router)
app.include_router(bot_auth_router)
