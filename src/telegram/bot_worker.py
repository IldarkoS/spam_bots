import asyncio
import logging
from asyncio import Task

from telethon import TelegramClient, events
from telethon.errors import ChatAdminRequiredError, RPCError
from telethon.tl.types import PeerChannel

from src.adapters.bot_repository import BotRepositoryImpl
from src.adapters.task_repository import TaskRepositoryImpl
from src.config import settings
from src.core.db import db_helper
from src.core.models.task import TaskStatus, TaskScope, TaskType

import logging

from src.telegram.comment_generator import DummyGenerator

logging.basicConfig(level=logging.DEBUG)
# For instance, show only warnings and above
logging.getLogger('telethon').setLevel(level=logging.WARNING)

class BotWorker:
    def __init__(self, bot_id: int):
        self.bot_id = bot_id
        self.bot = None
        self.client: TelegramClient | None = None
        self.tasks: list[Task] = []
        self.comment_generator = DummyGenerator()

    async def _init_bot(self):
        async with db_helper.session_factory() as session:
            repo = BotRepositoryImpl(session)
            self.bot = await repo.get_by_id(self.bot_id)
            if not self.bot:
                raise RuntimeError(f"Bot with ID {self.bot_id} not found")

        session_path = f"{settings.SESSIONS_DIR}/{self.bot.phone}"
        self.client = TelegramClient(session=session_path, api_id=self.bot.api_id, api_hash=self.bot.api_hash)
        await self.client.connect()
        if not await self.client.is_user_authorized():
            raise RuntimeError(f"Bot {self.bot.phone} not authorized")

        logging.info(f"Bot {self.bot.phone} ({self.bot.id}) connected")

    async def _load_tasks(self):
        async with db_helper.session_factory() as session:
            repo = TaskRepositoryImpl(session)
            all_tasks = await repo.get_all_tasks()

        self.tasks = [
            task
            for task in all_tasks
            if task.status == "NEW"
               and (task.scope == "GLOBAL" or task.bot_id == self.bot_id)
        ]
        logging.info(f"Loaded {len(self.tasks)} tasks for bot {self.bot_id}")

    async def _handle_tasks(self):
        for task in self.tasks:
            if task.type == "SINGLE":
                await self._handle_single(task)
            elif task.type == "SUBSCRIBE":
                await self._handle_subscribe(task)

    async def _handle_single(self, task: Task):
        if not task.channel or not task.post_id:
            logging.warning(f"Skipping invalid SINGLE task {task.id}")
            return

        try:
            comment = f"[{self.bot.name}] Привет! Это автоматический комментарий."
            entity = await self.client.get_entity(PeerChannel(int(task.channel)))
            await self.client.send_message(entity=entity, message=comment, reply_to=task.post_id)
            logging.debug(f"Sending message to {task.channel}, post_id={task.post_id}")

            logging.info(f"SINGLE task #{task.id} done by bot {self.bot_id}")
        except RPCError as e:
            logging.error(f"Failed to perform SINGLE task {task.id}: {e}")
            await self._mark_task_error(task, str(e))

    async def _handle_subscribe(self, task: Task):
        if not task.channel:
            logging.warning(f"Skipping invalid SUBSCRIBE task {task.id}")
            return

        entity = await self.client.get_entity(PeerChannel(int(task.channel)))

        @self.client.on(events.NewMessage(chats=entity))
        async def handler(event):
            try:
                if event.message.is_reply or event.message.reply_to:
                    logging.debug(f"Bot {self.bot_id} ignored comment in {task.channel}")
                    return

                text = event.message.message
                reply = await self.comment_generator.generate_comment(text)
                await event.reply(reply)
                await event.reply(reply)
                logging.info(f"Bot {self.bot_id} commented in {task.channel}")
            except RPCError as e:
                logging.error(f"Bot {self.bot_id} failed to comment: {e}")

        logging.info(f"Bot {self.bot_id} subscribed to {task.channel} for task {task.id}")

    async def _mark_task_error(self, task: Task, error: str):
        async with db_helper.session_factory() as session:
            repo = TaskRepositoryImpl(session)
            task.status = "ERROR"

    async def run(self):
        try:
            await self._init_bot()
            await self._load_tasks()
            await self._handle_tasks()
            logging.info(f"Bot {self.bot_id} is now running")
            await self.client.run_until_disconnected()
        except Exception as e:
            logging.exception(f"Bot {self.bot_id} crashed: {e}")