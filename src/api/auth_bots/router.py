from fastapi import APIRouter

from src.api.auth_bots.dto import CodeSubmit, PasswordSubmit
from src.config import settings
from src.depends import AuthBotUseCase, BotUseCase
from src.service.auth_bot import AuthBotUseCaseImpl

router = APIRouter(prefix="/bot", tags=["Auth Bots"])


@router.post("/auth/request_code/{bot_id}/")
async def request_code(
    bot_id: int,
    auth_bot_use_case: AuthBotUseCase,
    bot_use_case: BotUseCase,
):
    bot = await bot_use_case.get_bot_by_id(id=bot_id)
    await auth_bot_use_case.request_code(bot=bot)
    return {"Status": "Code sent"}


@router.post("/auth/submit_code/{bot_id}/")
async def submit_code(
    bot_id: int,
    code_in: CodeSubmit,
    auth_bot_use_case: AuthBotUseCase,
    bot_use_case: BotUseCase,
):
    bot = await bot_use_case.get_bot_by_id(id=bot_id)
    result = await auth_bot_use_case.submit_code(bot=bot, code=code_in.code)
    return {"Status": result}


@router.post("/auth/submit_password/{bot_id}/")
async def submit_password(
    bot_id: int,
    password_in: PasswordSubmit,
    auth_bot_use_case: AuthBotUseCase,
    bot_use_case: BotUseCase,
):
    bot = await bot_use_case.get_bot_by_id(id=bot_id)
    result = await auth_bot_use_case.submit_password(
        bot=bot, password=password_in.password
    )
    return {"Status": result}
