# run with command line: python -m pytest tests/test_llm.py

from llm import get_llm
from unittest.mock import patch
import os
import pytest

def test_get_llm_config():
    with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_key"}):
        llm = get_llm()
        
        # Verify it's a ChatOpenAI (Chatbot) instance
        # Note: langchain_openai.ChatOpenAI inherits from BaseChatModel
        assert llm.openai_api_key.get_secret_value() == "test_key"
        assert llm.openai_api_base == "https://openrouter.ai/api/v1"
        assert llm.model_name == "openai/gpt-4o-mini"

def test_get_llm_raises_error_without_key():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="OPENROUTER_API_KEY not found"):
            get_llm()
