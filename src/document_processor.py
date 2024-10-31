# src/document_processor.py

from abc import ABC, abstractmethod

class DocumentProcessor(ABC):
    def __init__(self, file_path, output_path, openai_api, prompt):
        self.file_path = file_path
        self.output_path = output_path
        self.openai_api = openai_api
        self.prompt = prompt

    @abstractmethod
    def process(self):
        pass