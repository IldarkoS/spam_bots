from fastapi import APIRouter, status, Depends

from src.api.bots.dto import BotRead, BotCreate, BotUpdate, FilterParams
from src.depends import BotUseCase

router = APIRouter(tags=["Bots"], prefix="")


@router.post("/bot/", response_model=BotRead)
async def create_bot(bot_in: BotCreate, bot_use_case: BotUseCase):
    entity = await bot_use_case.create_bot(bot_in.to_entity())
    return BotRead.from_entity(entity)


@router.get("/bots/", response_model=list[BotRead])
async def get_bots(bot_use_case: BotUseCase, query_params: FilterParams = Depends()):
    bots = await bot_use_case.get_bots_list(params=query_params)
    return [BotRead.from_entity(bot) for bot in bots]


@router.get("/bot/{bot_id}/", response_model=BotRead)
async def get_bot(bot_id: int, bot_use_case: BotUseCase):
    entity = await bot_use_case.get_bot_by_id(id=bot_id)
    return BotRead.from_entity(entity)


@router.delete("/bot/{bot_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bot(bot_id: int, bot_use_case: BotUseCase):
    await bot_use_case.delete_bot(id=bot_id)


@router.patch("/bot/{bot_id}/", response_model=BotRead, status_code=status.HTTP_200_OK)
async def patch_bot(bot_id: int, bot_in: BotUpdate, bot_use_case: BotUseCase):
    entity = bot_in.to_entity(bot_id)
    entity = await bot_use_case.update_bot(bot=entity)
    return BotRead.from_entity(entity)
