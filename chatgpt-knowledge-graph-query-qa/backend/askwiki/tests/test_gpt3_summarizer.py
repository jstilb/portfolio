from askwiki.gpt3_summarizer import Gpt3Summarizer

def test_getwikiprop_3_A():
    summarizer = Gpt3Summarizer()
    endpoint_url = "https://query.wikidata.org/sparql"
    query3 = """SELECT ?operating_income WHERE { wd:Q32491 wdt:P3362 ?operating_income . }"""
    wd_df3, wikiobjects_3 = summarizer.sparql_to_df(endpoint_url, query3)
    askwiki_openai_input, _ = summarizer.getwikiprop_3(wd_df3, wikiobjects_3)
    assert askwiki_openai_input == "Answer | operating_income | 1370000000"

def test_getwikiprop_3_B():
    summarizer = Gpt3Summarizer()
    endpoint_url = "https://query.wikidata.org/sparql"
    query3 = """SELECT ?athlete_id WHERE { wd:Q235975 wdt:P3171 ?athlete_id . }"""
    wd_df3, wikiobjects_3 = summarizer.sparql_to_df(endpoint_url, query3)
    askwiki_openai_input, _ = summarizer.getwikiprop_3(wd_df3, wikiobjects_3)
    assert askwiki_openai_input == "Answer | athlete_id | mary-lou-retton"

def test_getwikiprop_3_no_match():
    summarizer = Gpt3Summarizer()
    endpoint_url = "https://query.wikidata.org/sparql"
    nomatch = """SELECT ?answer WHERE { wd:Q675176 wdt:P515 ?X . ?X wdt:P156 ?answer}"""
    wd_nomatch, wikiobjects_nomatch = summarizer.sparql_to_df(endpoint_url, nomatch)
    askwiki_openai_input, askwiki_nlg_input = summarizer.getwikiprop_3(wd_nomatch, wikiobjects_nomatch)
    assert askwiki_openai_input == 'Wikidata | Answer | No matching records found'

def test_generate_response():
    summarizer = Gpt3Summarizer()
    summary = summarizer.generate_response('hepatitis A| BNCF Thesaurus |42006 && hepatitis A| MedlinePlus ID |000278 && hepatitis A| DiseasesDB |5757 & hepatitis A| ICD-9 |070.0 && hepatitis A| ICD-10 |B15 && hepatitis A| eMedicine |177484 && hepatitis A| Freebase ID |/m/01yjzm && hepatitis A| Patientplus ID |hepatitis-a-pro ->',
                                           stop=[" \n"])
    assert summary is not None
    assert 'Hepatitis A' in summary

def test_run_sparql_and_summarize():
    summarizer = Gpt3Summarizer()
    query3 = """SELECT ?athlete_id WHERE { wd:Q235975 wdt:P3171 ?athlete_id . }"""
    rawresults, summary = summarizer.run_sparql_and_summarize(query3)
    assert rawresults is not None
    assert summary is not None

