from fastapi import HTTPException, status


class BotError(HTTPException):
    ...


class BotNotFoundError(BotError):
    def __init__(self, bot_id=None):
        message = "Bot not found" if bot_id is None else f"Bot with ID: {bot_id} not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)

