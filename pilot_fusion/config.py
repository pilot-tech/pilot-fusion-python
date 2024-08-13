import os

def set_google_api_key(api_key: str):
    os.environ["GOOGLE_API_KEY"] = api_key

def get_google_api_key():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set. Use `set_google_api_key` to configure it.")
    return api_key


def set_openai_api_key(api_key: str):
    os.environ["OPENAI_API_KEY"]=api_key

def get_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set. Use `set_openai_api_key` to configure it.")
    return api_key

def set_mistral_api_key(api_key: str):
    os.environ["MISTRAL_API_KEY"]=api_key


def get_mistral_api_key():
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set. Use `set_mistral_api_key` to configure it.")
    return api_key


def set_claude_api_key(api_key: str):
    os.environ["ANTHROPIC_API_KEY"]=api_key


def get_claude_api_key():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set. Use `set_claude_api_key` to configure it.")
    return api_key    


