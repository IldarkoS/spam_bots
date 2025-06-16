from src.domain.bot_entity import BotUseCaseProtocol, BotRepositoryProtocol, Bot
from src.exceptions import BotNotFoundError


class BotUseCaseImpl(BotUseCaseProtocol):

    def __init__(self, repository: BotRepositoryProtocol):
        self.repository = repository

    async def create(self, bot: Bot) -> Bot:
        return await self.repository.add(bot)

    async def delete(self, id: int) -> None:
        await self.repository.delete(id)

    async def get_by_id(self, id: int) -> Bot:
        bot = await self.repository.get_by_id(id)
        if not bot:
            raise BotNotFoundError(bot_id=id)
        return bot

    async def update(self, bot: Bot) -> Bot:
        exist = await self.get_by_id(bot.id)
        return await self.repository.update(bot)

    async def get_all(self) -> list[Bot]:
        return await self.repository.get_all()
