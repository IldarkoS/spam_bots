class CommentGenerator:
    async def generate_comment(self, post_text: str) -> str:
        ...


class DummyGenerator(CommentGenerator):
    async def generate_comment(self, post_text: str) -> str:
        return f"Автоматический ответ на пост : {post_text[:30]}"

