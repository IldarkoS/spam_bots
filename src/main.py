from fastapi import FastAPI

from src.api.bots.router import router as bot_router
from src.api.tasks.router import router as task_router
from src.api.auth_bots.router import router as bot_auth_router
from src.api.bot_runner.bot_runner import router as bot_runner_router
from src.logging import configure_logging, LogLevel

configure_logging(LogLevel.DEBUG)
app = FastAPI()

app.include_router(bot_router)
app.include_router(task_router)
app.include_router(bot_auth_router)
app.include_router(bot_runner_router)
