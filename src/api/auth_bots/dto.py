from pydantic import BaseModel


class CodeSubmit(BaseModel):
    code: str


class PasswordSubmit(BaseModel):
    password: str
