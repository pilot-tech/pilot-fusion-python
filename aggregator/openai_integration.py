from .commonllm import CodeGenerator
from .config import get_google_api_key
import google.generativeai as genai
import openai


class OpenaiCodeGenerator(CodeGenerator):
    def __init__(self):
        super().__init__('gemini')
        self.configure_api_key()

    def configure_api_key(self):
        api_key = get_google_api_key()
        genai.configure(api_key=api_key)

    def get_model_response(self, full_prompt: str):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_prompt}]
        )
        return response