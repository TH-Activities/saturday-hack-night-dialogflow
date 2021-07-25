from requests import post, get
from json import loads 
from config import API_URL
from emoji import UNICODE_EMOJI_ENGLISH, demojize


find_unicode = lambda s : '{:X}'.format(ord(s))

input_as_json = lambda data : {'queryInput': {'text': {'text': data, 'languageCode': "en"}}}

load_from_agent = lambda expression : post(API_URL, json=input_as_json(expression))

clean_response = lambda response : response[4:]

json_to_dict = lambda json : loads(json)

extract_data = lambda response_dict : response_dict['queryResult']['parameters']

is_emoji = lambda char : char in UNICODE_EMOJI_ENGLISH.keys()

def calculate_expression(expression_dict):
    try:
        if expression_dict['operator'] == '+':
            return float(expression_dict['number_1']) + float(expression_dict['number_2']) 

        elif expression_dict['operator'] == '-':
            return float(expression_dict['number_1']) - float(expression_dict['number_2']) 

        elif expression_dict['operator'] == '*':
            return float(expression_dict['number_1']) * float(expression_dict['number_2']) 

        elif expression_dict['operator'] == '/':
            return float(expression_dict['number_1']) / float(expression_dict['number_2']) 

    except KeyError:
        return None

def generate_story_from_emoji(emoji_string):
    words = []
    for e in emoji_string:
        words.append(demojize(e).replace(':', '').replace('_', ' '))
    try:
        subject, verb, object = words[0], words[1], words[2]
    except IndexError:
        return 'Sorry i need minimum three emojis(subject, verb and object)'
    r = loads(get(f'https://lt-nlgservice.herokuapp.com/rest/english/realise?subject={subject}&verb={verb}&object={object}').text)
    if r['result'] == 'OK':
        return r['sentence']
    return 'sorry i didn\'t get it'


class ColourPrint:
    @staticmethod
    def Red(text): return "\033[91m {}\033[00m" .format(text)

    @staticmethod
    def Green(text): return "\033[92m {}\033[00m" .format(text)

    @staticmethod
    def Yellow(text): return "\033[93m {}\033[00m" .format(text)

    @staticmethod
    def LightPurple(text): return "\033[94m {}\033[00m" .format(text)

    @staticmethod
    def Purple(text): return "\033[95m {}\033[00m" .format(text)

    @staticmethod
    def Cyan(text): return "\033[96m {}\033[00m" .format(text)

    @staticmethod
    def prLightGray(text): return "\033[97m {}\033[00m" .format(text)

    @staticmethod
    def Black(text): return "\033[98m {}\033[00m" .format(text)
    