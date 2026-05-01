"""Shared pytest fixtures for ml-automation-nlp."""

import json
from pathlib import Path
from typing import Any, Dict

import pytest


@pytest.fixture
def mock_llm_response() -> Dict[str, Any]:
    """Mock LLM response for testing agent integration."""
    return {
        "status": "success",
        "message": "Test response",
        "data": {"text": "Sample NLP output"},
    }


@pytest.fixture
def sample_dataset() -> Dict[str, Any]:
    """Sample dataset for testing text analysis."""
    return {
        "documents": [
            "This is a sample document about NLP.",
            "Natural language processing is powerful.",
            "Machine learning models require training data.",
        ],
        "labels": ["topic_a", "topic_b", "topic_c"],
        "metadata": {
            "source": "test_data",
            "language": "en",
            "count": 3,
        },
    }


@pytest.fixture
def temp_workspace(tmp_path: Path) -> Path:
    """Create a temporary workspace directory for file operations."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace
