import logging
import re

import httpx

from src.domain.comment_generator import CommentGeneratorProtocol


class OllamaClient:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model = "qwen3"
        self.timeout = httpx.Timeout(60.0)

    async def _ensure_model_loaded(self):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
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
                logging.exception(f"Failed to pull/check model from Ollama - {e}")

    async def generate(self, prompt: str) -> str:
        await self._ensure_model_loaded()

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
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
            f'''
            Напиши короткий дружелюбный комментарий,  
            не нужно никаких рассуждений, твой ответ - это только комментарий длиной не более 15 слов - 
            {clean_text}
            '''
        )

        try:
            response = await self.llm_client.generate(prompt=prompt)
            word = "</think>"
            think_end = response.find("</think>")
            comment = response.strip()[think_end+len(word):]
            logging.info(f"Generated comment: {comment[:30]}")
            return comment
        except Exception as e:
            logging.exception(f"Failed to generate comment - {e}")
            return "Интересный пост!"