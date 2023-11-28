import logging

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from .gpt3_sparql import Gpt3SparqlGenerator
from .langchain_sparql import LangchainSparqlGenerator
from .t5_summarizer import T5Summarizer
from .wikibase_sparql_runner import WikibaseSparqlRunner
from .gpt3_summarizer import Gpt3Summarizer
from .langchain_agent import LangchainWikibaseAgent

log = logging.getLogger("askwiki")
log.setLevel(logging.INFO)

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "healthy"}


class PipelineName(BaseModel):
    pipeline_name: str


class Question(BaseModel):
    pipeline: str
    question: str


class Answer(BaseModel):
    pipeline: str
    question: str
    sparql: str
    rawresults: dict
    summary: str


class SimplePipeline():

    def run(self, question):
        # generate sparql
        sparql = self.generate_sparql(question)
        log.info(f'sparql {sparql}')

        # run the sparql query
        df_results = self.run_sparql(sparql)
        log.info(f'df_results {df_results}')
        rawresults = {c: list(df_results[c]) for c in df_results.columns}
        log.info(f'rawresults {df_results}')

        # generate a summary
        summary = self.generate_summary(question, df_results)
        log.info(f'summary {summary}')

        return sparql, rawresults, summary


class DummyPipeline(SimplePipeline):

    def generate_sparql(self, question):
        return "this is supposed to be a sparql query"

    def run_sparql(self, query):
        df = pd.DataFrame({"sbj": ["wd:Q351363", "wd:Q331835", "wd:Q11533909"],
                           "sbj_label": ["seamanship", "suction", "Senshoku ginōshi"]})
        return df

    def generate_summary(self, question, df):
        return "this is supposed to be a summary"


class Gpt3T5Pipeline(SimplePipeline):
    def __init__(self):
        self.sparql_generator = Gpt3SparqlGenerator()
        self.sparql_runner = WikibaseSparqlRunner()
        self.summarizer = T5Summarizer()

    def generate_sparql(self, question):
        sparql = self.sparql_generator.generate_sparql(question)
        return sparql

    def run_sparql(self, query):
        df = self.sparql_runner.run_sparql_to_df(query)
        return df

    def generate_summary(self, question, df):
        # find the objects in the result
        wikiobjects = []
        for index, row in df.iterrows():
            for col in df.columns:
                v = row[col]
                if v.find('http://www.wikidata.org/entity/') >= 0:
                    wikiobjects.append(col_.replace('http://www.wikidata.org/entity/', ''))
        assertions = self.summarizer.get_wiki_prop(wikiobjects)
        wikibase_input = f"AskWiki NLG: {'&&'.join(assertions)}  </s>"
        summary = self.summarizer.generate_summary(wikibase_input)
        return summary


class LangchainT5Pipeline(SimplePipeline):
    def __init__(self):
        self.sparql_generator = LangchainSparqlGenerator()
        self.sparql_runner = WikibaseSparqlRunner()
        self.summarizer = T5Summarizer()

    def generate_sparql(self, question):
        sparql = self.sparql_generator.generate_sparql(question)
        return sparql

    def run_sparql(self, query):
        df = self.sparql_runner.run_sparql_to_df(query)
        return df

    def generate_summary(self, question, df):
        # find the objects in the result
        wikiobjects = []
        for index, row in df.iterrows():
            for col in df.columns:
                v = row[col]
                if v.find('http://www.wikidata.org/entity/') >= 0:
                    wikiobjects.append(col_.replace('http://www.wikidata.org/entity/', ''))
        assertions = self.summarizer.get_wiki_prop(wikiobjects)
        wikibase_input = f"AskWiki NLG: {'&&'.join(assertions)}  </s>"
        summary = self.summarizer.generate_summary(wikibase_input)
        return summary


class LangchainDummyPipeline(SimplePipeline):
    def __init__(self):
        self.sparql_generator = LangchainSparqlGenerator()
        self.sparql_runner = WikibaseSparqlRunner()

    def generate_sparql(self, question):
        sparql = self.sparql_generator.generate_sparql(question)
        return sparql

    def run_sparql(self, query):
        df = self.sparql_runner.run_sparql_to_df(query)
        return df

    def generate_summary(self, question, df):
        summary = 'this is supposed to be the summary'
        return summary

class LangchainGpt3SummarizerPipeline():

    def __init__(self):
        self.sparql_generator = LangchainSparqlGenerator()
        self.summarizer = Gpt3Summarizer()

    def run(self, question):
        # generate sparql
        sparql = self.sparql_generator.generate_sparql(question)
        print(f'sparql {sparql}')
        rawresults, summary = self.summarizer.run_sparql_and_summarize(sparql)
        return sparql, rawresults, summary


class LangchainAgentPipeline():

    def __init__(self):
        self.agent = LangchainWikibaseAgent()

    def run(self, question):
        # generate sparql
        summary = self.agent.generate_sparql_run_and_summarize(question)
        return "this is supposed to be a sparql query", \
            { "sbj": [ "wd:Q351363", "wd:Q331835", "wd:Q11533909" ], "sbj_label": [ "seamanship", "suction", "Senshoku ginōshi" ] }, \
            summary



pipeline_cache = {
    'default': {'class': DummyPipeline, 'instance': DummyPipeline()},
    'gpt3_t5': {'class': Gpt3T5Pipeline, 'instance': None},
    'langchain_t5': {'class': LangchainT5Pipeline, 'instance': None},
    'langchain_gpt3': {'class': LangchainGpt3SummarizerPipeline, 'instance': None},
    'agent': {'class': LangchainAgentPipeline, 'instance': None}
}


def getPipeline(pipeline):
    if pipeline not in pipeline_cache:
        print(f"can't find pipeline {pipeline}, using default")
        pipeline = 'default'
    else:
        print(f'found pipeline {pipeline}')
    pipeline_dict = pipeline_cache[pipeline]
    if pipeline_dict['instance'] is None:
        print(f'instantiating pipeline {pipeline}')
        pipeline_dict['instance'] = pipeline_dict['class']()
    return pipeline_dict['instance']


@app.get("/pipelines/")
async def pipelines():
    pipeline_names = [PipelineName(pipeline_name=n) for n in pipeline_cache]
    return pipeline_names


@app.post("/ask/")
async def ask(p: Question):
    # choose the pipeline
    pipeline = getPipeline(p.pipeline)

    sparql, rawresults, summary = pipeline.run(p.question)

    answer = Answer(pipeline=p.pipeline,
                    question=p.question,
                    sparql=sparql,
                    rawresults=rawresults,
                    summary=summary)

    return answer
