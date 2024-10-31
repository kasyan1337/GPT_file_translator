# src/openai_api.py

import os
import openai
from dotenv import load_dotenv
import time
import logging

# Configure logging
logging.basicConfig(filename="api_usage.log", level=logging.INFO)


class OpenAIAPI:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4-turbo"  # Use the desired model
        self.last_usage = {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}

    def translate_text(self, prompt, text):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text},
                ],
            )
            # Log usage
            usage = response["usage"]
            self.last_usage = usage  # Store last usage
            logging.info(
                f"Prompt tokens: {usage['prompt_tokens']}, "
                f"Completion tokens: {usage['completion_tokens']}, "
                f"Total tokens: {usage['total_tokens']}"
            )
            return response["choices"][0]["message"]["content"]

        except openai.error.OpenAIError as e:
            if 'rate limit' in str(e).lower():
                print("Rate limit exceeded. Waiting for 20 seconds.")
                time.sleep(20)
                return self.translate_text(prompt, text)
            print(f"OpenAI API error: {e}")
            return None

        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def calculate_cost(self, usage):
        # Pricing as per OpenAI's rates for GPT-4 (update if rates change)
        prompt_tokens = usage['prompt_tokens']
        completion_tokens = usage['completion_tokens']
        total_tokens = usage['total_tokens']
        cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000  # USD
        return cost