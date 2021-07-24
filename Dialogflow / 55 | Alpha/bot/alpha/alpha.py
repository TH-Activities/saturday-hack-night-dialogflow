from json import load, dumps 
from time import sleep
from misc import BANNER
from helpers import *


class AvailableIntents:
  SayJoke = 'jokes.get'
  Calculate = 'calculate-simple-expressions'
  Welcome = 'Default Welcome Intent'
  FallBack = 'Default Fallback Intent'
  Emoji = 'detect-emoji'
  Help = 'help-user'

class Alpha:
    _instance = None
    _user_info = None
    _prompt = '>'
    _intro = 'Hii, i\'m Alpha.'

    
    def __init__(self):
        raise RuntimeError('call instance() instead')


    def load_user_info(self):
        with open('data/user_info.json', 'r') as user_info_file:
            self._user_info = load(user_info_file)

    def save_user_info(self):
        with open('data/user_info.json', 'w') as user_info_file:
            user_info_file.write(dumps(self._user_info))


    @classmethod
    def instance(cls, debug=False):
        """
        Creates a new ``Alpha`` instance.
        The ``debug`` parameter can be set to True to enable debug messages.
        """
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls.load_user_info(cls._instance)

        cls.DEBUG = debug

        return cls._instance

    def check_get_user_name(self):
        name = self._user_info['name']
        if name == '':
            name = input('Enter your name : ')
        self._user_info['name'] = name
        self._intro = f'Welcome back {name}'
        self.save_user_info()

    # for CLI
    def get_input(self):
        return input(f'{ColourPrint.Yellow(self._user_info["name"])} {self._prompt} ')


    def say(self, text=''):
        return text


    def give_intro(self):
        return self.say(self._intro)

    def give_actions(self):
        return self.say('I can do simple calculations, create stories from emojies or just talk!!!')

    def connect_agent(self, expression):
        response = load_from_agent(expression)
        response = clean_response(response.text)
        return json_to_dict(response)

    def detect_intent(self, response_dict):
        # return if intent is present
        try:
            intent =  response_dict['queryResult']['intent']['displayName']
            return intent
        # else intent detection failed at dialpgflow side
        except KeyError:
            return None

    def do_actions(self, response_dict):
        intent = self.detect_intent(response_dict)
        if intent == AvailableIntents.SayJoke:
            return self.say_joke(response_dict)

        elif intent == AvailableIntents.Calculate:
          try:
              return self.do_simple_calculations(response_dict)
          except ZeroDivisionError:
            return 'It\'s too hard for me'

        elif intent == AvailableIntents.Welcome:
            return self.say(response_dict['queryResult']['fulfillmentText'])

        elif intent == AvailableIntents.Emoji:
          return self.emoji_to_story(response_dict)

        elif intent == AvailableIntents.FallBack:
                return self.say(response_dict['queryResult']['fulfillmentText'])
        
        elif intent == AvailableIntents.Help:
                return self.say(response_dict['queryResult']['fulfillmentText'])
        else:
            try:
              if 'smalltalk' in response_dict['queryResult']['action']:
                  return self.say(response_dict['queryResult']['fulfillmentText'])
            except KeyError:
              print('Invalid Action Occured')
            else:
                return self.say('Something is really really wrong!!')

    def do_simple_calculations(self, response_dict):
        result = calculate_expression(response_dict['queryResult']['parameters'])
        if result != None:
            return self.say(f"{response_dict['queryResult']['queryText']} is {result}")
        else:
            return f'It\'s too hard for me!!'

    def say_joke(self, response_dict):
        return self.say(f"Here is a joke: {response_dict['queryResult']['fulfillmentText']}")

    def emoji_to_story(self, response_dict):
        emoji_string = response_dict['queryResult']['queryText']
        story = generate_story_from_emoji(emoji_string)
        return self.say(story)

    def execute(self, command):
      response_dict = self.connect_agent(command)
      return self.do_actions(response_dict)

    def run(self):
        self.check_get_user_name()
        self.give_intro()
        self.give_actions()
        self.say('so what do you wanna do?')
        try:
            while True:
                expression = self.get_input()
                print()
                response_dict = self.connect_agent(expression)
                self.do_actions(response_dict)


        except KeyboardInterrupt:
            print()
            print()
            self.say('see ya later')
        