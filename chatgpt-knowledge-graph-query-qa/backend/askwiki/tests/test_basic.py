from fastapi.testclient import TestClient

from askwiki import __version__
from askwiki.main import app

client = TestClient(app)

def test_version():
    assert __version__ == "0.1.0"

def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200

def test_pipelines():
    response = client.get("/pipelines/")
    assert response.status_code == 200
    names = [v['pipeline_name'] for v in response.json()]
    assert 'default' in names

