import os
from mistralai.client import MistralClient

from .commonllm import CodeGenerator

class MistralCodeGenerator(CodeGenerator):
    def __init__(self, model_name: str = "codestral-mamba-latest"):
        super().__init__(model_name)
        self.api_key = os.environ.get("MISTRAL_API_KEY")
        self.client = MistralClient(api_key=self.api_key)

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