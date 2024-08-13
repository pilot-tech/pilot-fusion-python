import pytest
import os
from pilot_fusion.config import (
    set_google_api_key,
    get_google_api_key,
    set_openai_api_key,
    get_openai_api_key,
    set_mistral_api_key,
    get_mistral_api_key
)

def test_set_google_api_key():
    test_api_key = "test-google-api-key"
    set_google_api_key(test_api_key)
    assert os.getenv("GOOGLE_API_KEY") == test_api_key

def test_get_google_api_key(monkeypatch):
    test_api_key = "test-google-api-key"
    monkeypatch.setenv("GOOGLE_API_KEY", test_api_key)
    assert get_google_api_key() == test_api_key

def test_get_google_api_key_not_set(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    with pytest.raises(ValueError, match="GOOGLE_API_KEY environment variable not set. Use `set_google_api_key` to configure it."):
        get_google_api_key()

def test_set_openai_api_key():
    test_api_key = "test-openai-api-key"
    set_openai_api_key(test_api_key)
    assert os.getenv("OPENAI_API_KEY") == test_api_key

def test_get_openai_api_key(monkeypatch):
    test_api_key = "test-openai-api-key"
    monkeypatch.setenv("OPENAI_API_KEY", test_api_key)
    assert get_openai_api_key() == test_api_key

def test_get_openai_api_key_not_set(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable not set. Use `set_openai_api_key` to configure it."):
        get_openai_api_key()

def test_set_mistral_api_key():
    test_api_key = "test-mistral-api-key"
    set_mistral_api_key(test_api_key)
    assert os.getenv("MISTRAL_API_KEY") == test_api_key

def test_get_mistral_api_key(monkeypatch):
    test_api_key = "test-mistral-api-key"
    monkeypatch.setenv("MISTRAL_API_KEY", test_api_key)
    assert get_mistral_api_key() == test_api_key

def test_get_mistral_api_key_not_set(monkeypatch):
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
    with pytest.raises(ValueError, match="MISTRAL_API_KEY environment variable not set. Use `set_mistral_api_key` to configure it."):
        get_mistral_api_key()
