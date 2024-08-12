# PilotHub
Pilot Aggregator is a Python package designed to streamline the aggregation of data from multiple sources. Built with efficiency and flexibility in mind, this package allows developers to easily collect, process, and manage data in a unified manner.

## Features

- **Unified API Configuration:** Easily configure API keys for different LLMs.
- **LLM Integration:** Seamlessly switch between different LLMs (e.g., OpenAI, Gemini, Mistral) for text and code generation.
- **Code Generation:** Generate Python code based on prompts using the specified LLM.
- **Text Generation:** Generate detailed text responses based on prompts using the specified LLM.
- **Extensible Design:** Easily add support for more LLMs in the future.

## Installation

You can install the package using pip:

```bash
pip install pilot-fusion
```

## Getting Started

### 1. Configure API Keys

Before using the LLMs, you need to set the API keys. The package provides utility functions in `config.py` to set and retrieve these keys.

**Example:**

```python
from aggregator.config import set_openai_api_key, set_google_api_key, set_mistral_api_key

# Set the OpenAI API key
set_openai_api_key('your-openai-api-key')

# Set the Google API key for Gemini
set_google_api_key('your-google-api-key')

# Set the Mistral API key
set_mistral_api_key('your-mistral-api-key')
```

### 2. Using LLMs for Code Generation

You can generate code using different LLMs by creating an instance of the corresponding generator class.

```python
from aggregator.gemini_integration import GeminiCodeGenerator

# Initialize the Gemini code generator
gemini_generator = GeminiCodeGenerator()

# Generate code based on a prompt
prompt = "Create a diagram for a microservices architecture."
code = gemini_generator.generate_code(prompt)

print(code)
```

### 3. Using LLMs for Text Generation


Similar to code generation, you can also generate text responses using different LLMs.

Example:

```python
# Generate a text response based on a prompt
text = gemini_generator.generate_text("Explain the benefits of using microservices.")

print(text)
```

## Adding Support for New LLMs

The package is designed to be extensible. To add a new LLM:

1. Create a new class that inherits from `CodeGenerator`.
2. Implement the `get_model_response` method to interact with the new LLM's API.
3. Add configuration functions for the new LLM's API key in `config.py`.

### Example Skeleton for Adding a New LLM

```python
from aggregator.commonllm import CodeGenerator
from aggregator.config import get_newllm_api_key
import newllm

class NewLLMCodeGenerator(CodeGenerator):
    def __init__(self):
        super().__init__('newllm')
        self.configure_api_key()

    def configure_api_key(self):
        api_key = get_newllm_api_key()
        newllm.configure(api_key=api_key)

    def get_model_response(self, full_prompt: str):
        model = newllm.GenerativeModel('newllm-model')
        response = model.generate_content(full_prompt)
        return {"text": response.text.strip()}
```

# Code Generators Using Different AI Models

### 1. Gemini Code Generator

This generator uses Google's Gemini model.

```python
from aggregator.gemini_integration import GeminiCodeGenerator

generator = GeminiCodeGenerator(model_name="gemini-1.5-pro")
code = generator.generate_diagram("Create a system diagram for a web application using React, Node.js, and MongoDB.")
print(code)
```
### 2. OpenAI Code Generator

This generator uses OpenAI's models like GPT-3.5-turbo.

```python
from aggregator.openai_integration import OpenaiCodeGenerator

generator = OpenaiCodeGenerator(model_name="gpt-3.5-turbo")
code = generator.generate_code("Create a Python function that sorts a list of numbers.")
print(code)

```

### 3. Mistral Code Generator

This generator uses the Mistral model.


```python
from aggregator.mistral_integration import MistralCodeGenerator

generator = MistralCodeGenerator(model_name="codestral-mamba-latest")
code = generator.generate_diagram("Create a flowchart for an e-commerce application.")
print(code)


```
### 4. Claude Code Generator

This generator uses Anthropic's Claude model.


```python
from aggregator.claude_integration import ClaudeCodeGenerator

generator = ClaudeCodeGenerator(model_name="claude-3-5-sonnet-20240620")
code = generator.generate_diagram("Generate a UML diagram for a microservices architecture.")
print(code)



```

## Contribution

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

## Contact

If you have any questions, feel free to open an issue or contact the repository maintainers.



