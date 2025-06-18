from typing import Protocol


class CommentGeneratorProtocol(Protocol):
    async def generate_comment(self, post_text: str) -> str: ...
