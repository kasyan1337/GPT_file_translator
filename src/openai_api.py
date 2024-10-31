# src/openai_api.py

import os
import openai
from dotenv import load_dotenv
import time
import logging

# Configure logging
logging.basicConfig(filename="api_usage.log", level=logging.INFO)

class OpenAIAPI:
    def __init__(self, model="gpt-4o"):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.last_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

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
            if "rate limit" in str(e).lower():
                print("Rate limit exceeded. Waiting for 20 seconds.")
                time.sleep(20)
                return self.translate_text(prompt, text)
            print(f"OpenAI API error: {e}")
            return None

        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def calculate_cost(self, usage):
        # Pricing as per OpenAI's latest rates (update if rates change)
        model_pricing = {
            "gpt-4o": {"prompt": 0.00250, "completion": 0.01000},
            "gpt-4o-2024-08-06": {"prompt": 0.00250, "completion": 0.01000},
            "gpt-4o-mini": {"prompt": 0.000150, "completion": 0.000600},
            "gpt-4o-mini-2024-07-18": {"prompt": 0.000150, "completion": 0.000600},
            "o1-preview": {"prompt": 0.015, "completion": 0.060},
            "o1-mini": {"prompt": 0.003, "completion": 0.012},
        }
        rates = model_pricing.get(self.model, None)
        if rates is None:
            print(f"Model {self.model} not found in pricing list.")
            return 0.0
        cost = (
            (usage["prompt_tokens"] * rates["prompt"])
            + (usage["completion_tokens"] * rates["completion"])
        ) / 1000
        return cost