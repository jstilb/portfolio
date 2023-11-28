import pytest
import json
from fastapi.testclient import TestClient

from askwiki import __version__
from askwiki.main import app

client = TestClient(app)


GPT3_T5_EXAMPLE = {
    'pipeline': 'gpt3_t5',
    'question': 'What are the most common types of liver infection?'
}


def test_ask():
    response = client.post("/ask/", data=json.dumps(GPT3_T5_EXAMPLE))
    assert response.status_code == 200
    print(response.json())
    assert 'summary' in response.json()
                           
