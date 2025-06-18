import asyncio
import logging
from collections import defaultdict

from src.domain.bot import Bot, BotRepositoryProtocol
from src.domain.bot_manager import BotManagerUseCaseProtocol
from src.domain.comment_generator import CommentGeneratorProtocol
from src.domain.task import TaskRepositoryProtocol
from src.service.bot_worker import BotWorkerUseCaseImpl
from src.service.comment_generator import CommentGeneratorImpl
from src.telegram.telegram_client import get_telegram_client


class BotManagerUseCaseImpl(BotManagerUseCaseProtocol):
    def __init__(
        self,
        bot_repository: BotRepositoryProtocol,
        task_repository: TaskRepositoryProtocol,
        comment_generator: CommentGeneratorProtocol,
    ):
        self.bot_repository = bot_repository
        self.task_repository = task_repository
        self.comment_generator = comment_generator
        self._workers: dict[int, asyncio.Task] = {}
        self._errors: dict[int, str] = defaultdict(str)

    def _is_running(self, bot_id: int) -> bool:
        task = self._workers.get(bot_id, None)
        return task is not None and not task.done()

    async def _run_worker(self, bot_id: int, worker: BotWorkerUseCaseImpl):
        try:
            await worker.run()
        except Exception as e:
            self._errors[bot_id] = str(e)
            logging.error(
                f"Bot ({worker.bot.name}:{worker.bot.phone}) crashed with error: {e}"
            )
        finally:
            worker.bot.is_active = False
            await self.bot_repository.update(bot=worker.bot)
            self._workers.pop(bot_id, None)

    async def start_bot(self, bot: Bot):
        if self._is_running(bot.id):
            logging.info(f"Bot ({bot.name}:{bot.phone}) already running")
            return

        bot.is_active = True
        await self.bot_repository.update(bot=bot)

        client = get_telegram_client(bot)
        worker = BotWorkerUseCaseImpl(
            bot=bot,
            client=client,
            comment_generator=self.comment_generator,
            task_repository=self.task_repository,
        )

        task = asyncio.create_task(self._run_worker(bot_id=bot.id, worker=worker))
        self._workers[bot.id] = task

    async def stop_bot(self, bot: Bot):
        task = self._workers.get(bot.id)
        if task and not task.done():
            task.cancel()
            logging.info(f"Bot ({bot.name}:{bot.phone}) stopped")
        bot.is_active = False
        await self.bot_repository.update(bot=bot)
        self._workers.pop(bot.id, None)

    async def restart_bot(self, bot: Bot):
        await self.stop_bot(bot=bot)
        await self.start_bot(bot=bot)

    async def get_status(self) -> list[dict]: ...
