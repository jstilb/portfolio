from fastapi.testclient import TestClient

from askwiki.main import app
from askwiki.wikibase_sparql_runner import WikibaseSparqlRunner

client = TestClient(app)


def test_wikibase_sparql_runner():
    runner = WikibaseSparqlRunner()
    query = "select distinct ?obj where { wd:Q188920 wdt:P2813 ?obj . ?obj wdt:P31 wd:Q1002697 }"
    df = runner.run_sparql_to_df(query)
    assert df is not None
    

def test_bad_syntax():
    runner = WikibaseSparqlRunner()
    # the open { is missing
    query = "select distinct ?obj where  wd:Q188920 wdt:P2813 ?obj . ?obj wdt:P31 wd:Q1002697 }"
    df = runner.run_sparql_to_df(query)
    assert df is None
    

