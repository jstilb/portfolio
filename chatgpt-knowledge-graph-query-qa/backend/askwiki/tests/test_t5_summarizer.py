from askwiki.t5_summarizer import T5Summarizer

def test_get_wiki_prop():
    summarizer = T5Summarizer()
    res = summarizer.get_wiki_prop(['Q6853', 'Q154869', 'Q157661'])
    assert res is not None

def test_t5_summarizer_sj():
    summarizer = T5Summarizer()
    wikibase_input = "AskWiki NLG: shrinivas | description | student && shrinivas | surname | joshi && shrinivas | student | UC Berkeley  && shrinivas | hair color | salt&pepper && shrinivas | age | 42  </s>"
    summary = summarizer.generate_summary(wikibase_input)
    print(summary)
    assert summary is not None

HEP_ASSERTIONS = ['hepatitis B|Description|human viral infection', 'hepatitis B|Commons category|Hepatitis B',
                  'hepatitis B|BNCF Thesaurus|22624', 'hepatitis B|MedlinePlus ID|000279',
                  'hepatitis B|DiseasesDB|5765',
                  'hepatitis B|ICD-9|070.2', 'hepatitis B|ICD-10|B16', 'hepatitis B|eMedicine|177632',
                  'hepatitis B|NDL ID|00986940',
                  'hepatitis B|Patientplus ID|hepatitis-b-pro', 'hepatitis B|Disease Ontology ID|DOID:2043',
                  'hepatitis B|NCI Thesaurus ID|C3097',
                  'hepatitis B|Encyclopædia Britannica Online ID|science/hepatitis-B',
                  'hepatitis B|number of deaths|wikidata.quantity.Quantity(887000.0, None, None, None)',
                  'hepatitis B|number of cases|wikidata.quantity.Quantity(257000000.0, None, None, None)',
                  'hepatitis B|MeSH ID|D006509',
                  'hepatitis B|ICD-9-CM|070.30', 'hepatitis B|MeSH Code|C02.256.430.400',
                  'hepatitis B|OmegaWiki Defined Meaning|1291115', 'hepatitis B|OMIM ID|610424',
                  'hepatitis B|BNE ID|XX548510',
                  'hepatitis B|KEGG ID|H00412', 'hepatitis B|BnF ID|11938386s', 'hepatitis B|LCAuth ID|sh85060295',
                  'hepatitis B|GND ID|4159548-8', 'hepatitis B|NKCR AUT ID|ph118024',
                  'hepatitis C|Description|human viral infection',
                  'hepatitis C|BNCF Thesaurus|44499', 'hepatitis C|MedlinePlus ID|000284',
                  'hepatitis C|DiseasesDB|5783',
                  'hepatitis C|eMedicine|177792', 'hepatitis C|NDL ID|00986947', 'hepatitis C|Freebase ID|/m/0jdvt',
                  'hepatitis C|GND ID|4262007-7', 'hepatitis C|Commons category|Hepatitis C',
                  'hepatitis C|Patientplus ID|hepatitis-c-pro', 'hepatitis C|Disease Ontology ID|DOID:1883',
                  'hepatitis C|NCI Thesaurus ID|C3098',
                  'hepatitis C|Encyclopædia Britannica Online ID|science/hepatitis-C',
                  'hepatitis C|prevalence|wikidata.quantity.Quantity(0.22, None, None, None)',
                  'hepatitis C|number of deaths|wikidata.quantity.Quantity(399000.0, None, None, None)',
                  'hepatitis C|number of cases|wikidata.quantity.Quantity(71000000.0, None, None, None)',
                  'hepatitis C|MeSH ID|D006526',
                  'hepatitis C|ICD-9-CM|070.7', 'hepatitis C|MeSH Code|C01.925.440.440',
                  'hepatitis C|MalaCards ID|hepatitis_c',
                  'hepatitis C|OMIM ID|609532', 'hepatitis C|KEGG ID|H00413', 'hepatitis C|LCAuth ID|sh85060290',
                  'hepatitis C|BnF ID|12175477z', 'hepatitis C|NKCR AUT ID|ph120673',
                  'hepatitis A|Description|acute infectious disease of the liver',
                  'hepatitis A|BNCF Thesaurus|42006',
                  'hepatitis A|MedlinePlus ID|000278', 'hepatitis A|DiseasesDB|5757', 'hepatitis A|ICD-9|070.0',
                  'hepatitis A|ICD-10|B15', 'hepatitis A|eMedicine|177484', 'hepatitis A|Freebase ID|/m/01yjzm',
                  'hepatitis A|Patientplus ID|hepatitis-a-pro', 'hepatitis A|Disease Ontology ID|DOID:12549',
                  'hepatitis A|NCI Thesaurus ID|C3096', 'hepatitis A|Commons category|Hepatitis A',
                  'hepatitis A|Encyclopædia Britannica Online ID|science/hepatitis-A',
                  'hepatitis A|BabelNet id|00043755n',
                  'hepatitis A|MeSH ID|D006506', 'hepatitis A|MeSH Code|C01.925.440.420',
                  'hepatitis A|KEGG ID|H00411',
                  'hepatitis A|LCAuth ID|sh85060293', 'hepatitis A|NALT ID|82551',
                  'hepatitis A|NKCR AUT ID|ph1036491']

def test_t5_summarizer_hep_a():
    summarizer = T5Summarizer()
    assertions = [a for a in HEP_ASSERTIONS if a.startswith('hepatitis A')]
    wikibase_input = f"AskWiki NLG: {'&&'.join(assertions)}  </s>"
    summary = summarizer.generate_summary(wikibase_input)
    print(summary)
    assert summary is not None

def test_t5_summarizer_hep():
    summarizer = T5Summarizer()
    assertions = HEP_ASSERTIONS
    wikibase_input = f"AskWiki NLG: {'&&'.join(assertions)}  </s>"
    summary = summarizer.generate_summary(wikibase_input)
    assert summary is not None



