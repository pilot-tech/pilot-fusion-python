from .commonllm import CodeGenerator
from .config import  get_openai_api_key
import google.generativeai as genai
import openai


class OpenaiCodeGenerator(CodeGenerator):
    def __init__(self, model_name='gpt-3.5-turbo'):
        super().__init__('openai')
        self.model_name = model_name
        self.configure_api_key()

    def configure_api_key(self):
        api_key = get_openai_api_key()
        openai.api_key = api_key

    def get_model_response(self, full_prompt: str):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": full_prompt}]
        )
        return {"text": response.choices[0].message['content'].strip()}