from fastapi import APIRouter

from src.depends import BotUseCase, BotManagerUseCase

router = APIRouter(tags=["Bot runner"], prefix="/bot")


@router.post("/run/{bot_id}/")
async def run_bot(
    bot_id: int, bot_use_case: BotUseCase, bot_manager_use_case: BotManagerUseCase
):
    bot = await bot_use_case.get_bot_by_id(id=bot_id)
    await bot_manager_use_case.start_bot(bot=bot)
    return {"Status": f"Bot ({bot.name}:{bot.phone}) started"}


@router.post("/stop/{bot_id}/")
async def stop_bot(
    bot_id: int, bot_use_case: BotUseCase, bot_manager_use_case: BotManagerUseCase
):
    bot = await bot_use_case.get_bot_by_id(id=bot_id)
    await bot_manager_use_case.stop_bot(bot=bot)
    return {"Status": f"Bot ({bot.name}:{bot.phone}) stopped"}


@router.post("/restart/{bot_id}/")
async def restart_bot(bot_id: int): ...


@router.get("/status/")
async def status(): ...
