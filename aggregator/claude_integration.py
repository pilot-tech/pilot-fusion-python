import anthropic

from .commonllm import CodeGenerator

class ClaudeCodeGenerator(CodeGenerator):
    def __init__(self, model_name: str = "claude"):
        super().__init__(model_name)
        self.anthropic_client = anthropic.Anthropic()

    def get_model_response(self, full_prompt: str):
        message = self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20240620",
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
        content = message.content.strip()

        return content
    

