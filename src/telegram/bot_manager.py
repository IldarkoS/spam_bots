import asyncio
import logging
from collections import defaultdict

from src.telegram.bot_worker import BotWorker


class BotManager:
    def __init__(self):
        self._workers: dict[int, asyncio.Task] = {}
        self._errors: dict[int, str] = defaultdict(str)

    def is_running(self, bot_id) -> bool:
        task = self._workers.get(bot_id)
        return task is not None and not task.done()

    async def start_bot(self, bot_id: int):
        if self.is_running(bot_id):
            logging.info(f"Bot {bot_id} already running")
            return

        logging.info(f"Starting bot {bot_id}...")
        worker = BotWorker(bot_id)
        task = asyncio.create_task(self._run_worker(bot_id, worker))
        self._workers[bot_id] = task


    async def _run_worker(self, bot_id: int, worker: BotWorker):
        try:
            await worker.run()
        except Exception as e:
            logging.error(f"Bot {bot_id} crashed: {e}")
            self._errors[bot_id] = str(e)
            self._workers.pop(bot_id)

    async def stop_bot(self, bot_id: int):
        task = self._workers.get(bot_id)
        if task and not task.done():
            task.cancel()
            logging.info(f"Stopping bot {bot_id}...")
            self._workers.pop(bot_id)

    async def restart_bot(self, bot_id: int):
        await self.stop_bot(bot_id)
        await self.start_bot(bot_id)

    async def start_all(self):
        ...

    async def get_status(self) -> list[dict]:
        return [
            {
                "bot_id": bot_id,
                "running": self.is_running(bot_id),
                "error": self._errors.get(bot_id)
            }
            for bot_id in self._workers.keys()
        ]


manager = BotManager()