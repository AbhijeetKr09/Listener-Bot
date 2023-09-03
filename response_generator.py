import spacy
import json
from collections import defaultdict, deque
import os
import openai
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, SentimentOptions
from dotenv import load_dotenv

load_dotenv('data.env')
class ResponseGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlu_api = os.getenv('NLU_API')
        self.nlu_url = os.getenv('NLU_URL')
        self.version = os.getenv('NLU_version')
        openai.api_key = os.getenv('OPENAI_API')

        authenticator = IAMAuthenticator(self.nlu_api)
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            version=self.version,
            authenticator=authenticator
        )

        self.natural_language_understanding.set_service_url(self.nlu_url)
        self.save_data_for_training()

    def create_prompt(self, user_text):
        doc = self.nlp(user_text)
        entities = [ent.text for ent in doc.ents]

        response = self.natural_language_understanding.analyze(
            text=user_text,
            features=Features(entities=EntitiesOptions(), sentiment=SentimentOptions())).get_result()
        sentiment = response['sentiment']['document']['label']
        if not response['entities']:
            intent = 'Unknown'
        else:
            intent = response['entities'][0]['type']

        prompt = f"The user is feeling {sentiment} and their intent is {intent} and entities in text: {entities}. Provide a response that addresses their needs. \n this is user text: {user_text}."
        return prompt

    def generate_response(self, prompt, conversation_history, model='text-davinci-002'):
        if not conversation_history:
            conversation_history_str = ''
        else:
            conversation_history_str = '\n'.join(
                f"{message['text']}\n {message['response']}"
                for message in conversation_history
            )

        prompt = f"last conversation History:{conversation_history_str} \n New prompt from user: {prompt}"
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=1.0,
            top_p=0.9
        )
        return response['choices'][0]['text']

    def store_data(self, username, user_text, response_text, filename='history.json', max_history=5):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if username not in data:
            data[username] = []

        conversation_history_list = list(data[username])

        message = {'text': user_text, 'response': response_text}
        conversation_history_list.append(message)

        conversation_history_list = conversation_history_list[-max_history:]

        data[username] = conversation_history_list

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_conversation_history(self, username, filename='history.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        conversation_history = list(data.get(username, []))

        return conversation_history

    def store_complete_data(self, username, user_text, response_text, filename='complete_history.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = defaultdict(list)

        message = {'text': user_text, 'response': response_text}
        data[username].append(message)

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_complete_conversation_history(self, username, filename='complete_history.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        conversation_history = data.get(username, [])

        return conversation_history
    
    def save_data_for_training(self, input_file='complete_history.json', output_file='training_data.txt'):
        try:
            with open(input_file, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"File '{input_file}' not found.")
            return

        with open(output_file, 'a') as output:
            for conversation in data.values():
                for message in conversation:
                    user_text = message['text'].strip()
                    response = message['response'].strip()

                    output.write(f"User: {user_text}\n")
                    output.write(f"AI: {response}\n\n")