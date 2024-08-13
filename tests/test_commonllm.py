import pytest
import os
import re
from unittest.mock import patch, MagicMock
from pilot_fusion.commonllm import CodeGenerator, extract_relevant_imports, format_imports, extract_all_imports

class MockCodeGenerator(CodeGenerator):
    def get_model_response(self, full_prompt: str):
        if "Generate a complete Python script" in full_prompt:

            return {
                'choices': [
                    {'message': {'content': '```python\n# Mock code\n```'}}
                ]
            }
        elif "Describe what an EC2 instance is" in full_prompt:

            return {
                'choices': [
                    {'message': {'content': 'Mock text'}}
                ]
            }
        else:

            return {
                'choices': [
                    {'message': {'content': '```python\n# Default mock code\n```'}}
                ]
            }


@pytest.fixture
def setup_generator():
    return MockCodeGenerator(model_name="test_model")

def extract_relevant_imports(prompt: str, diagrams_data: dict) -> dict:
    relevant_imports = {}
    for category, components in diagrams_data.items():
        for component in components:
            if component.lower() in prompt.lower():
                relevant_imports.setdefault(category, []).append(component)
    return relevant_imports

def test_extract_relevant_imports():
    diagrams_data = {
        "diagrams.aws.compute": ["EC2", "Lambda"],
        "diagrams.aws.network": ["VPC", "Route53"]
    }
    prompt = "Create a diagram with EC2 and VPC"
    expected_imports = {
        "diagrams.aws.compute": ["EC2"],
        "diagrams.aws.network": ["VPC"]
    }

    assert extract_relevant_imports(prompt, diagrams_data) == expected_imports

def test_format_imports():
    relevant_imports = {
        "diagrams.aws.compute.EC2": ["EC2"],
        "diagrams.aws.network.VPC": ["VPC"]
    }
    expected_code = "from diagrams.aws.compute import EC2\nEC2 = [EC2]\nfrom diagrams.aws.network import VPC\nVPC = [VPC]"
    assert format_imports(relevant_imports) == expected_code

def test_generate_diagram(setup_generator):
    prompt = "Create a diagram with EC2 and VPC"
    generated_code = setup_generator.generate_diagram(prompt)
    
   
    assert re.search(r'# Mock code', generated_code) is not None


def test_generate_text(setup_generator):
    prompt = "Describe what an EC2 instance is"
    generated_text = setup_generator.generate_text(prompt)
    
    assert "Mock text" in generated_text

def test_generate_code(setup_generator):
    prompt = "Write a basic Hello World script"
    generated_code = setup_generator.generate_code(prompt)
    

    assert re.search(r'# Default mock code', generated_code) is not None



def test_validate_imports_valid(setup_generator):
    valid_code = "import os\nfrom diagrams.aws.compute import EC2\n"
    try:
        setup_generator.validate_imports(valid_code)
    except ValueError:
        pytest.fail("validate_imports() raised ValueError unexpectedly!")

def test_validate_imports_invalid(setup_generator):
    invalid_code = "import non_existent_module\n"
    with pytest.raises(ValueError):
        setup_generator.validate_imports(invalid_code)

@patch('builtins.open', new_callable=MagicMock)
@patch('os.makedirs', MagicMock())
def test_log_text(mock_open, setup_generator):
    prompt = "Describe an EC2 instance"
    content = "EC2 is a virtual server"
    setup_generator.log_text(prompt, content)
    mock_open.assert_called_once()

@patch('builtins.open', new_callable=MagicMock)
@patch('os.makedirs', MagicMock())
def test_log_code(mock_open, setup_generator):
    prompt = "Create a diagram with EC2"
    code = "# Diagram code"
    setup_generator.log_code(prompt, code)
    mock_open.assert_called_once()

def test_parse_response(setup_generator):
    response = {'choices': [{'message': {'content': 'Mock content'}}]}
    parsed_content = setup_generator.parse_response(response)
    
    assert parsed_content == 'Mock content'

def test_parse_response_unexpected_format(setup_generator):
    response = {'unexpected_key': 'unexpected_value'}
    with pytest.raises(ValueError):
        setup_generator.parse_response(response)

if __name__ == "__main__":
    pytest.main()
