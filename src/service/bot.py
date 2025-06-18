from typing import Any

from src.domain.bot import BotUseCaseProtocol, BotRepositoryProtocol, Bot, QueryParams
from src.exceptions import BotNotFoundError, BotAlreadyExistsError


class BotUseCaseImpl(BotUseCaseProtocol):

    def __init__(self, repository: BotRepositoryProtocol):
        self.repository = repository

    async def create_bot(self, bot: Bot) -> Bot:
        exist = await self.get_bot_by_field(
            {
                "name": bot.name,
                "phone": bot.phone,
            }
        )
        if exist:
            raise BotAlreadyExistsError()
        return await self.repository.create(bot=bot)

    async def delete_bot(self, id: int) -> None:
        exist = await self.get_bot_by_field(
            {
                "id": id,
            }
        )
        if not exist:
            raise BotNotFoundError(bot_id=id)
        await self.repository.delete(id=id)

    async def get_bot_by_field(self, filters: dict[str, Any]) -> Bot | None:
        bot = await self.repository.get_by_fields(filters)
        return bot

    async def update_bot(self, bot: Bot) -> Bot:
        exist = await self.get_bot_by_field(
            {
                "id": bot.id,
            }
        )
        if not exist:
            raise BotNotFoundError(bot_id=id)
        return await self.repository.update(bot=bot)

    async def get_bots_list(self, params: QueryParams) -> list[Bot]:
        return await self.repository.get_all_bots(params=params)

    async def get_bot_by_id(self, id: int) -> Bot:
        bot = await self.repository.get_by_fields({"id": id})
        if not bot:
            raise BotNotFoundError(bot_id=id)
        return bot
