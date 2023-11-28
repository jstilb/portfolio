import pytest
import json
from fastapi.testclient import TestClient

from askwiki import __version__
from askwiki.main import app
from askwiki.langchain_sparql import LangchainSparqlGenerator

client = TestClient(app)


def test_liver_infection():
    ssg = LangchainSparqlGenerator()
    question = "What are the most common types of liver infection?"
    sparql = ssg.generate_sparql(question)
    assert sparql is not None
    assert isinstance(sparql, str)
    assert len(sparql) > 0
    print(sparql)


def test_delta():
    ssg = LangchainSparqlGenerator()
    question = "What is Delta Air Line's periodical literature mouthpiece?"
    sparql = ssg.generate_sparql(question)
    assert sparql is not None
    assert isinstance(sparql, str)
    assert len(sparql) > 0
    print(sparql)

def test_bach():
    ssg = LangchainSparqlGenerator()
    question = "How many children did J.S. Bach have?"
    sparql = ssg.generate_sparql(question)
    assert sparql is not None
    assert isinstance(sparql, str)
    assert len(sparql) > 0
    print(sparql)

def test_ravanalova():
    ssg = LangchainSparqlGenerator()
    question = "Who is the child of the husband of Ravanalova I?"
    sparql = ssg.generate_sparql(question)
    assert sparql is not None
    assert isinstance(sparql, str)
    assert len(sparql) > 0
    print(sparql)

