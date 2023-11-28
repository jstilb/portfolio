import configparser

import pandas as pd

from wikibaseintegrator import wbi_helpers
from wikibaseintegrator.wbi_config import config as wbi_config

from requests.exceptions import HTTPError


class WikibaseSparqlRunner:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('secrets.ini')
        wbi_config['USER_AGENT'] = config['WIKIDATA']['USER_AGENT']
        wbi_config['BACKOFF_MAX_TRIES'] = 1

    def run_sparql_to_df(self, query):
        try:
            results = wbi_helpers.execute_sparql_query(query)
        except HTTPError as he:
            print(f"failed query {query}")
            return None
        if 'boolean' in results:
            return pd.DataFrame([{'Boolean': results['boolean']}])
        jsonResult = [dict([(k, b[k]['value']) for k in b]) for b in results['results']['bindings']]
        df = pd.DataFrame.from_dict(jsonResult)
        return df
