# src/openai_api.py

import os
import openai
from dotenv import load_dotenv

class OpenAIAPI:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4"

    def translate_text(self, prompt, text):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]
        )
        return response['choices'][0]['message']['content']