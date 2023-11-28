import openai
import configparser


def run_prompt(prompt="", model=None, temperature=0.6, stop=None):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=100,
        stop=stop
    )
    return response

class Gpt3SparqlGenerator:
    MODEL_NAME = 'davinci:ft-askwiki-2023-03-13-01-21-40'
    def __init__(self, model=MODEL_NAME):
        config = configparser.ConfigParser()
        config.read('secrets.ini')
        openai.api_key = config['OPENAI']['OPENAI_API_KEY']
        self.model = model

    def generate_sparql(self, question):
        response = run_prompt(f"{question} ->",
                              model=self.model, stop=[" \n"])
        translation = response['choices'][0]['text']
        if translation is None or len(translation) == 0:
            return None
        return translation
