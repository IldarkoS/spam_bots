from fastapi import APIRouter, status

from src.api.bots.dto import BotCreateResponse, BotCreateRequest, BotUpdateRequest
from src.depends import BotUseCase

router = APIRouter(tags=["Bots"], prefix="")


@router.post("/bot/", response_model=BotCreateResponse)
async def create_bot(bot_in: BotCreateRequest, bot_use_case: BotUseCase):
    entity = await bot_use_case.create(bot_in.to_entity())
    return BotCreateResponse.from_entity(entity)


@router.get("/", response_model=list[BotCreateResponse])
async def get_bots(bot_use_case: BotUseCase):
    bots = await bot_use_case.get_all()
    return [BotCreateResponse.from_entity(bot) for bot in bots]


@router.get("/bot/{bot_id}/", response_model=BotCreateResponse)
async def get_bot(bot_id: int, bot_use_case: BotUseCase):
    entity = await bot_use_case.get_by_id(bot_id)
    return BotCreateResponse.from_entity(entity)


@router.delete("/bot/{bot_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bot(bot_id: int, bot_use_case: BotUseCase):
    await bot_use_case.delete(bot_id)


@router.patch("/bot/{bot_id}/", status_code=status.HTTP_200_OK)
async def patch_bot(bot_id: int, bot_in: BotUpdateRequest, bot_use_case: BotUseCase):
    entity = bot_in.to_entity(bot_id)
    entity = await bot_use_case.update(entity)
    return BotCreateResponse.from_entity(entity)
