import os
from mistralai.client import MistralClient

from .commonllm import CodeGenerator

class MistralCodeGenerator(CodeGenerator):
    def __init__(self, model_name: str = "codestral-mamba-latest"):
        super().__init__('mistral')
        self.model_name = model_name
        self.api_key = self.get_api_key()
        self.client = MistralClient(api_key=self.api_key)


    def get_api_key(self):
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY environment variable not set.")
        return api_key


    def get_model_response(self, full_prompt: str):
        messages = [
            {
                "content": full_prompt,
                "role": "user"
            }
        ]
        chat_response = self.client.chat(
            model=self.model_name,
            messages=messages
        )
        return chat_response 