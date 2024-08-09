import anthropic

from .commonllm import CodeGenerator

class ClaudeCodeGenerator(CodeGenerator):
    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620"):
        super().__init__('claude')
        self.model_name = model_name
        self.anthropic_client = anthropic.Anthropic()

    def get_model_response(self, full_prompt: str):
        message = self.anthropic_client.messages.create(
            model=self.model_name,
            max_tokens=1000,
            temperature=0,
            system="You are an expert in creating diagrams. Respond only with the complete code wrapped in triple backticks.",
            messages=[
                {
                    "role": "user",
                    "content": full_prompt
                }
            ]
        )
        content = message['completion'].strip()

        return {"text": content}
    

