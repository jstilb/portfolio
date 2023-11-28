import pytest
import json
from fastapi.testclient import TestClient

from askwiki import __version__
from askwiki.main import app

client = TestClient(app)


GPT3_T5_EXAMPLE = {
    'pipeline': 'langchain_t5',
    'question': 'What is the Basketball-Reference.com NBA player ID of Hakeem Olajuwon?'
}


def test_ask():
    response = client.post("/ask/", data=json.dumps(GPT3_T5_EXAMPLE))
    assert response.status_code == 200
    print(response.json())
    assert 'summary' in response.json()
                           
