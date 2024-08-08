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
pip install llm-integrator
```

## Getting Started

### 1. Configure API Keys

Before using the LLMs, you need to set the API keys. The package provides utility functions in `config.py` to set and retrieve these keys.

**Example:**

```python
from llm_integrator.config import set_openai_api_key, set_google_api_key, set_mistral_api_key

# Set the OpenAI API key
set_openai_api_key('your-openai-api-key')

# Set the Google API key for Gemini
set_google_api_key('your-google-api-key')

# Set the Mistral API key
set_mistral_api_key('your-mistral-api-key')
