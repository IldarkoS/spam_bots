import asyncio
import logging
from os import login_tty

from telethon import TelegramClient, events
from telethon.errors import RPCError, UserNotParticipantError
from telethon.tl.types import PeerChannel, Message, Channel

from src.config import settings
from src.domain.bot import Bot
from src.domain.bot_worker import BotWorkerUseCaseProtocol
from src.domain.comment_generator import CommentGeneratorProtocol
from src.domain.task import (
    TaskUseCaseProtocol,
    Task,
    TaskRepositoryProtocol,
    TaskStatus,
)
from src.service.comment_generator import CommentGeneratorImpl


class BotWorkerUseCaseImpl(BotWorkerUseCaseProtocol):
    def __init__(
        self,
        bot: Bot,
        client: TelegramClient,
        task_repository: TaskRepositoryProtocol,
        comment_generator: CommentGeneratorProtocol,
    ):
        self.bot = bot
        self.client = client
        self.task_repository = task_repository
        self.comment_generator = comment_generator
        self._is_running = True
        self._active_channels = set()

        self.client.add_event_handler(
            self._message_handler,
            event=events.NewMessage()
        )

    async def run(self):
        self._is_running = True
        logging.info(f"Bot worker ({self.bot.name}:{self.bot.phone}) starting...")
        await self._connect()
        asyncio.create_task(self._subscribe_loop())

        try:
            await self.client.run_until_disconnected()
        finally:
            logging.info(f"Bot worker ({self.bot.name}:{self.bot.phone}) stopped.")
            self._is_running = False

    async def _connect(self):
        if not self.client.is_connected():
            await self.client.connect()
        if not await self.client.is_user_authorized():
            raise RuntimeError(
                f"Bot worker ({self.bot.name}:{self.bot.phone}) is not authorized"
            )
        logging.info(
            f"Bot worker ({self.bot.name}:{self.bot.phone}) connected to Telegram API"
        )

    async def _subscribe_loop(self):
        while self._is_running:
            try:
                await self._poll_and_update_channels()
            except Exception as e:
                logging.error(
                    f"Bot worker ({self.bot.name}:{self.bot.phone}) error during polling tasks: {e}"
                )
            await asyncio.sleep(60)

    async def _poll_and_update_channels(self):
        tasks: list[Task] = await self.task_repository.get_all_tasks()
        relevant = [t for t in tasks if t.scope == "GLOBAL" or t.bot_id == self.bot.id]

        for task in relevant:
            task.status = TaskStatus.IN_PROGRESS
            await self.task_repository.update(task=task)

        channel_ids = {int(t.channel) for t in relevant}
        self._active_channels = channel_ids

        # logging.info(
        #     f"Bot worker ({self.bot.name}:{self.bot.phone}) now listening to channels: {channel_ids}"
        # )

    async def _message_handler(self, event: events.NewMessage.Event):
        chat = event.chat
        message: Message = event.message

        if not isinstance(chat, Channel):
            return

        if chat.id not in self._active_channels:
            return

        if message.is_reply or message.reply_to:
            return

        try:
            participant = await event.client.get_permissions(chat, 'me')
            if not participant.post_messages:
                logging.warning(
                    f"Bot worker ({self.bot.name}:{self.bot.phone}) has no rights to post messages in {chat.title} ({chat.id})"
                )
                return
        except UserNotParticipantError:
            logging.warning(
                f"Bot worker ({self.bot.name}:{self.bot.phone}) is not a participant of {chat.title} ({chat.id})"
            )
            return
        except RPCError as e:
            logging.error(
                f"Bot worker ({self.bot.name}:{self.bot.phone}) failed to check permissions in {chat.title} ({chat.id}): {e}"
            )
            return

        try:
            reply = await self.comment_generator.generate_comment(post_text=message.message)
            await event.reply(reply)
            logging.info(
                f"Bot worker ({self.bot.name}:{self.bot.phone}) replied in channel {chat.title} ({chat.id}): {reply[:30]}"
            )
        except RPCError as e:
            logging.error(
                f"Bot worker ({self.bot.name}:{self.bot.phone}) failed to reply in {chat.title} ({chat.id}): {e}"
            )

    def stop(self):
        self._is_running = False
        self._active_channels.clear()
        logging.info(f"Bot worker ({self.bot.name}:{self.bot.phone}) shutdown initiated.")