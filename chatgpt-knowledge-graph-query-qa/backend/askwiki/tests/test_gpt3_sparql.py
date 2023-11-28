import pytest
import json
from fastapi.testclient import TestClient

from askwiki import __version__
from askwiki.main import app
from askwiki.gpt3_sparql import Gpt3SparqlGenerator

client = TestClient(app)


def test_liver_infection():
    ssg = Gpt3SparqlGenerator()
    question = "What are the most common types of liver infection?"
    sparql = ssg.generate_sparql(question)
    assert sparql is not None
    assert isinstance(sparql, str)
    assert len(sparql) > 0
    print(sparql)


def test_delta():
    ssg = Gpt3SparqlGenerator()
    question = "What is Delta Air Line's periodical literature mouthpiece?"
    sparql = ssg.generate_sparql(question)
    assert sparql is not None
    assert isinstance(sparql, str)
    assert len(sparql) > 0
    print(sparql)


