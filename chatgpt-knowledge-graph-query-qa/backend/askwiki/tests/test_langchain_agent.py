from askwiki.langchain_agent import LangchainWikibaseAgent

def test_generate_sparql_run_and_summarize_bach():
    agent = LangchainWikibaseAgent()
    question = "How many children did J.S. Bach have?"
    answer = agent.generate_sparql_run_and_summarize(question)
    assert answer is not None
    assert isinstance(answer, str)
    assert len(answer) > 0
    print(answer)

