
import pytest
from unittest.mock import patch, MagicMock
from pilot_fusion.gemini_integration import GeminiCodeGenerator
from pilot_fusion.config import get_google_api_key , set_google_api_key


set_google_api_key("mock-key")


@pytest.fixture
def mock_genai():
    with patch('google.generativeai') as mock_genai:
        yield mock_genai

@pytest.fixture
def code_generator(mock_genai):
    return GeminiCodeGenerator()

def test_initialize_code_generator(code_generator):
    assert isinstance(code_generator, GeminiCodeGenerator)
    assert code_generator.model_name == 'gemini'


@patch('google.generativeai.GenerativeModel')
def test_get_model_response(mock_GenerativeModel, mock_genai, code_generator):

    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = 'test response text'
    mock_GenerativeModel.return_value = mock_model
    
    full_prompt = 'Generate some content'
    expected_response = {"text": "test response text"}
    

    response = code_generator.get_model_response(full_prompt)
    

    mock_GenerativeModel.assert_called_once_with('gemini-1.5-pro')
    mock_model.generate_content.assert_called_once_with(full_prompt)
    assert response == expected_response
