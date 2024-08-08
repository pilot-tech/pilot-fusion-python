from .commonllm import CodeGenerator
from .config import get_google_api_key
import google.generativeai as genai

class GeminiCodeGenerator(CodeGenerator):
    def __init__(self):
        super().__init__('gemini')
        self.configure_api_key()

    def configure_api_key(self):
        api_key = get_google_api_key()
        genai.configure(api_key=api_key)

    def get_model_response(self, full_prompt: str):
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(full_prompt)
        return {"text": response.text.strip()}
    

    
    

