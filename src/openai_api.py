# src/openai_api.py

import os
import openai
from dotenv import load_dotenv
import asyncio
from openai.error import RateLimitError, OpenAIError, APIError, Timeout
import logging

# Configure logging
logging.basicConfig(filename="api_usage.log", level=logging.INFO)


class OpenAIAPI:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4"

    async def translate_text(self, prompt, text):
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text},
                ],
            )
            # Log usage
            usage = response["usage"]
            logging.info(
                f"Prompt tokens: {usage['prompt_tokens']}, Completion tokens: {usage['completion_tokens']}, Total tokens: {usage['total_tokens']}"
            )
            return response["choices"][0]["message"]["content"]
        except RateLimitError:
            print("Rate limit exceeded. Waiting for 20 seconds.")
            await asyncio.sleep(20)
            return await self.translate_text(prompt, text)
        except (OpenAIError, APIError, Timeout) as e:
            print(f"OpenAI API error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
