import pytest
import json
from fastapi.testclient import TestClient

from askwiki import __version__
from askwiki.main import app

client = TestClient(app)


def test_ask_hakeem():
    example = {
        'pipeline': 'langchain_gpt3',
        'question': 'What is the Basketball-Reference.com NBA player ID of Hakeem Olajuwon??'
    }
    response = client.post("/ask/", data=json.dumps(example))
    assert response.status_code == 200
    print(response.json())
    assert 'summary' in response.json()


def test_ask_bach():
    example = {
        'pipeline': 'langchain_gpt3',
        'question': 'How many children did J.S. Bach have?'
    }
    response = client.post("/ask/", data=json.dumps(example))
    assert response.status_code == 200
    print(response.json())
    assert 'summary' in response.json()

