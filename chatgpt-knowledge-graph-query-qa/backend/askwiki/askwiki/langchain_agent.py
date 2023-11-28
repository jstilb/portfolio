import logging
from typing import Any, Dict, List, Optional
import configparser
import os
import json

from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
import re

log = logging.getLogger("askwiki")
log.setLevel(logging.INFO)


def get_nested_value(o: dict, path: list) -> any:
    current = o
    for key in path:
        try:
            current = current[key]
        except:
            return None
    return current


import requests

from typing import Optional


def vocab_lookup(search: str, entity_type: str = "item",
                 url: str = "https://www.wikidata.org/w/api.php",
                 wikidata_user_agent_header: str = None,
                 srqiprofile: str = None,
                 ) -> Optional[str]:
    headers = {
        'Accept': 'application/json'
    }
    if wikidata_user_agent_header is not None:
        headers['User-Agent'] = wikidata_user_agent_header

    if entity_type == "item":
        srnamespace = 0
        srqiprofile = "classic_noboostlinks" if srqiprofile is None else srqiprofile
    elif entity_type == "property":
        srnamespace = 120
        srqiprofile = "classic" if srqiprofile is None else srqiprofile
    else:
        raise ValueError("entity_type must be either 'property' or 'item'")

    params = {
        "action": "query",
        "list": "search",
        "srsearch": search,
        "srnamespace": srnamespace,
        "srlimit": 1,
        "srqiprofile": srqiprofile,
        "srwhat": 'text',
        "format": "json"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        title = get_nested_value(response.json(), ['query', 'search', 0, 'title'])
        if title is None:
            return f"I couldn't find any {entity_type} for '{search}'. Please rephrase your request and try again"
        # if there is a prefix, strip it off
        return title.split(':')[-1]
    else:
        return "Sorry, I got an error. Please try again."


def run_sparql(query: str, url='https://query.wikidata.org/sparql',
               wikidata_user_agent_header: str = None) -> List[Dict[str, Any]]:
    headers = {
        'Accept': 'application/json'
    }
    if wikidata_user_agent_header is not None:
        headers['User-Agent'] = wikidata_user_agent_header

    response = requests.get(url, headers=headers, params={'query': query, 'format': 'json'})

    if response.status_code != 200:
        return "That query failed. Perhaps you could try a different one?"
    results = get_nested_value(response.json(), ['results', 'bindings'])
    return json.dumps(results)


template = """
Answer the following questions by generating a sparql query against a wikibase where the p and q items are 
completely unknown to you. You will need to discover the p and q items before you can generate the sparql.
Do not assume you know the p and q items for any concepts. Always use tools to find all p and q items.

When generating sparql:
* Try to avoid "count" and "filter" queries if possible
* Never enclose the sparql in back-quotes
* If you think the query might produce one or more q items, always ask for their labels also

After you generate the sparql, you should run it. The results will be returned in json. You should then
summarize the json results in natural language. Do not include any facts that are not in the json response.
If the json is empty, generate a summary based on that.

You may assume the following prefixes:
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>

You have access to the following tools:

{tools}

Use the following format:

Question: the input question for which you must provide either a natural language answer or a sparql query
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
{agent_scratchpad}"""


class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)


class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action: (.*?)[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)


class LangchainWikibaseAgent:
    MODEL_NAME = 'gpt-4'

    def __init__(self, model=MODEL_NAME):
        config = configparser.ConfigParser()
        config.read('secrets.ini')
        openai_api_key = config['OPENAI']['OPENAI_API_KEY']
        os.environ.update({'OPENAI_API_KEY': openai_api_key})
        wikidata_user_agent_header = None if not config.has_section('WIKIDATA') else config['WIKIDATA'][
            'USER_AGENT']

        # Define which tools the agent can use to answer user queries
        tools = [
            Tool(
                name="ItemLookup",
                func=(lambda x: vocab_lookup(x, entity_type="item")),
                description="useful for when you need to know the q-number for an item"
            ),
            Tool(
                name="PropertyLookup",
                func=(lambda x: vocab_lookup(x, entity_type="property")),
                description="useful for when you need to know the p-number for a property"
            ),
            Tool(
                name="SparqlQueryRunner",
                func=run_sparql,
                description="useful for getting results from a wikibase"
            )
        ]

        prompt = CustomPromptTemplate(
            template=template,
            tools=tools,
            # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
            # This includes the `intermediate_steps` variable because that is needed
            input_variables=["input", "intermediate_steps"]
        )

        output_parser = CustomOutputParser()

        llm = ChatOpenAI(model=model, temperature=0)

        # LLM chain consisting of the LLM and a prompt
        llm_chain = LLMChain(llm=llm, prompt=prompt)

        tool_names = [tool.name for tool in tools]
        agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names
        )

        self.agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

    def generate_sparql_run_and_summarize(self, question):
        result = self.agent_executor.run(question)
        return result
