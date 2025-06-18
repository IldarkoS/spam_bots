from fastapi import HTTPException, status


class BotError(HTTPException): ...


class BotNotFoundError(BotError):
    def __init__(self, bot_id=None):
        message = (
            "Bot not found" if bot_id is None else f"Bot with ID: {bot_id} not found"
        )
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class BotAlreadyExistsError(BotError):
    def __init__(self):
        message = "Bot already exists"
        super().__init__(status_code=status.HTTP_201_CREATED, detail=message)


class TaskError(HTTPException): ...


class TaskAlreadyExistsError(TaskError):
    def __init__(self):
        message = "Task already exists"
        super().__init__(status_code=status.HTTP_201_CREATED, detail=message)


class TaskNotFoundError(TaskError):
    def __init__(self, task_id=None):
        message = (
            "Task not found"
            if task_id is None
            else f"Task with ID: {task_id} not found"
        )
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class InvalidFilterFieldException(Exception):
    def __init__(self, field: str):
        super().__init__(f"Invalid filter field: '{field}' does not exist")


class AuthBotError(HTTPException): ...


class InvalidPhoneError(AuthBotError):
    def __init__(self):
        message = "Invalid phone number"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class InvalidCodeError(AuthBotError):
    def __init__(self):
        message = "Invalid code"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class CodeExpiredError(AuthBotError):
    def __init__(self):
        message = "Code expired"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class TooManyRequestsError(AuthBotError):
    def __init__(self):
        message = "Too many requests, try again later"
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=message)


class InvalidPasswordError(AuthBotError):
    def __init__(self):
        message = "Invalid password"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class CodeNotRequestedError(AuthBotError):
    def __init__(self):
        message = "Code was not requested"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
