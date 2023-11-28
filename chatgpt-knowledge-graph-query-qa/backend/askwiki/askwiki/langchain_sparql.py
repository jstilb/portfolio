import logging
from typing import Any, Dict, List, Optional

import openai
import configparser
import requests

from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain

log = logging.getLogger("askwiki")
log.setLevel(logging.INFO)

def get_nested_value(nested_dict: Dict[str, Any], path: List[str]) -> Optional[Any]:
    current = nested_dict
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def vocab_lookup(search: str, entity_type: str = "item",
                 item_tag: str = None,
                 srqiprofile: str = "classic") -> Optional[str]:
    if item_tag is not None:
        if item_tag.startswith("q-"):
            entity_type = "item"
        elif item_tag.startswith("p-"):
            entity_type = "property"

    if entity_type == "item":
        srnamespace = 0
    elif entity_type == "property":
        srnamespace = 120
    else:
        raise ValueError("entity_type must be either 'property' or 'item'")

    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search,
        "srnamespace": srnamespace,
        "srlimit": 5,
        "srqiprofile": srqiprofile,
        "srwhat": 'text',
        "format": "json"
    }
    headers = {'Accept': 'application/json'}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        results = get_nested_value(response.json(), ['query', 'search'])
        if results and len(results) > 0:
            return results[0]['title'].split(':')[-1]
        else:
            return None
    else:
        return None

def vocab_lookup_with_alternatives(search_terms, item_tag=None):
    for s in search_terms:
        term = vocab_lookup(s, item_tag=item_tag)
        if term is not None:
            return term
    return ""

def resolve_query_template(t):
    vocab_items = [(v["item_tag"], v["item_label_quesses"]) for v in t["vocabulary"]]
    # since this is not a proper template, we use "replace" below
    # so we need to be careful that some tags may be prefixes of others
    # sorting them by tag length avoids that
    vocab_items = sorted(vocab_items, key=lambda x: x[0], reverse=True)
    resolved_vocabulary = {item_tag: vocab_lookup_with_alternatives(item_label_quesses, item_tag=item_tag) for item_tag, item_label_quesses in vocab_items}
    query = t['query_template']
    for item_tag, item_id in resolved_vocabulary.items():
        query = query.replace(item_tag, item_id)
    result = query
    return result

class LangchainSparqlGenerator:
    MODEL_NAME = 'gpt3.5-turbo'

    def __init__(self, model=MODEL_NAME):
        config = configparser.ConfigParser()
        config.read('secrets.ini')
        self.openai_api_key = config['OPENAI']['OPENAI_API_KEY']

        system_prompt_template = """
You are an expert on sparql and wikibase. I have a private wikibase where the p and q items are completely unknown to you. 

If you are asked to provide a "query template json" for a user question, you should respond with a json object with these keys and values:
* 'query_template': a python-style template string. the query template should not use 'rdfs:label' to help you find items. Instead, just use a placeholder tag for each p and q item you need. Each tag should begin with "p-" or "q-" depending on whether you think you need a p or a q item
* 'vocabulary': a list of objects, one for each p or q item you need for a sparql query, each item should have these components:
** 'item_tag': a placeholder string that you make up
** 'item_label_quesses': a list of up to three different strings that you think might be used as the label for that p or q item
Remember: you do not know the actual q or p items in my wikibase, so make sure to list ALL p and q items in the 'vocabulary' section of the json.

You may assume the following prefixes:
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

Respond only with the json. Do not include any comments or explanations.
        """

        example1_human = """
        generate a query template json for the question "Does malin 1 have a right ascension lower than 15.1398?"
        """

        example1_ai = """
        {{
          "query_template": "SELECT ?result WHERE {{ wd:q-Malin1 wdt:p-RightAscension ?right_ascension . FILTER(?right_ascension < 15.1398) BIND(xsd:boolean(?right_ascension < 15.1398) as ?result) }}",
          "vocabulary": [
            {{
              "item_tag": "q-Malin1",
              "item_label_quesses": ["Malin 1", "Malin-1", "Malin1"]
            }},
            {{
              "item_tag": "p-RightAscension",
              "item_label_quesses": ["Right ascension", "right_ascension", "RA"]
            }}
          ]
        }}
        """

        example2_human = """
        generate a query template json for the question "How many children did J.S. Bach have?"
        """

        example2_ai = """
        {{
          "query_template": "SELECT (COUNT(?children) as ?count) WHERE {{ wd:q-JSBach wdt:p-Child ?children . }}",
          "vocabulary": [
            {{
              "item_tag": "q-JSBach",
              "item_label_quesses": ["J.S. Bach", "Johann Sebastian Bach", "Bach, Johann Sebastian"]
            }},
            {{
              "item_tag": "p-Child",
              "item_label_quesses": ["Child", "Offspring", "Progeny"]
            }}
          ]
        }}
        """

        example3_human = """
        generate a query template json for the question "What is the capital of France?"
        """

        example3_ai = """
        {{
          "query_template": "SELECT ?capital WHERE {{ wd:q-France wdt:p-Capital ?capital . }}",
          "vocabulary": [
            {{
              "item_tag": "q-France",
              "item_label_quesses": ["France"]
            }},
            {{
              "item_tag": "p-Capital",
              "item_label_quesses": ["Capital", "Capital city"]
            }}
          ]
        }}
        """

        template = system_prompt_template
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)

        example_human_1 = HumanMessagePromptTemplate.from_template(example1_human)
        example_ai_1 = AIMessagePromptTemplate.from_template(example1_ai)
        example_human_2 = HumanMessagePromptTemplate.from_template(example3_human)
        example_ai_2 = AIMessagePromptTemplate.from_template(example3_ai)

        human_template = "Please generate query template json for this question: {text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        self.chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, example_human_1, example_ai_1, example_human_2, example_ai_2,
             human_message_prompt])

    def generate_sparql(self, question):
        chat = ChatOpenAI(temperature=0, openai_api_key=self.openai_api_key)
        self.chain = LLMChain(llm=chat, prompt=self.chat_prompt)
        template = self.chain.run(f'generate a query template json for the question {question}')

        start_index = template.find('{')
        end_index = template.rfind('}')
        if start_index != -1 and end_index != -1 and start_index < end_index:
            template = template[start_index:end_index + 1]
        else:
            return None

        log.info(f"template: {template}")
        print(template)

        query = resolve_query_template(eval(template))
        return query
