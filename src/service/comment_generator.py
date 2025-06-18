import logging
import re

import httpx

from src.domain.comment_generator import CommentGeneratorProtocol


class OllamaClient:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model = "mistral"

    async def _ensure_model_loaded(self):
        """Проверка, загружена ли модель. Если нет — подтянуть."""
        async with httpx.AsyncClient() as client:
            try:
                res = await client.get(f"{self.base_url}/api/tags")
                res.raise_for_status()

                models = [m["name"] for m in res.json().get("models", [])]
                if self.model not in models:
                    logging.info(f"Pulling model {self.model} from Ollama...")
                    pull = await client.post(f"{self.base_url}/api/pull", json={"name": self.model})
                    pull.raise_for_status()
                    logging.info(f"Model {self.model} pulled successfully.")
                else:
                    logging.debug(f"Model {self.model} already loaded.")
            except Exception as e:
                logging.exception("Failed to pull/check model from Ollama")

    async def generate(self, prompt: str) -> str:
        await self._ensure_model_loaded()

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/api/chat", json=payload)

        if response.status_code != 200:
            logging.error("Ollama API error: %s", response.text)
            raise Exception("Ollama generation failed")

        result = response.json()
        return result.get("message", {}).get("content", "").strip()


class CommentGeneratorImpl(CommentGeneratorProtocol):
    def __init__(self):
        self.llm_client = OllamaClient(
        )

    @staticmethod
    def _clean_text(text: str) -> str:
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"
                                   u"\U0001F300-\U0001F5FF"
                                   u"\U0001F680-\U0001F6FF"
                                   u"\U0001F1E0-\U0001F1FF"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE
                                   )
        text = emoji_pattern.sub('', text)

        text = re.sub(r'\s+', ' ', text).strip()

        return text

    async def generate_comment(self, post_text: str) -> str:
        clean_text = self._clean_text(post_text)
        logging.info(f"Generating comment for post: {clean_text[:30]}")

        prompt = (
            f"Напиши короткий дружелюбный комментарий к следующему посту - {clean_text}"
        )

        try:
            response = await self.llm_client.generate(prompt=prompt)
            comment = response.strip()
            logging.info(f"Generated comment: {comment[:30]}")
            return comment
        except Exception as e:
            logging.exception("Failed to generate comment")
            return "Интересный пост!"
