from fastapi import APIRouter

from src.telegram.bot_manager import manager

router = APIRouter(tags=["Bot runner"], prefix="")

@router.post("/run/{bot_id}/")
async def run_bot(bot_id: int):
    await manager.start_bot(bot_id)
    return {"status": f"bot {bot_id} started"}

@router.post("/stop/{bot_id}/")
async def stop_bot(bot_id: int):
    await manager.stop_bot(bot_id)
    return {"status": f"bot {bot_id} stopped"}


@router.get("/status/")
async def status():
    return await manager.get_status()