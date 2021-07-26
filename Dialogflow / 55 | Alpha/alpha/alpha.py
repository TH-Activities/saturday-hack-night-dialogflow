from json import load, dumps 
from time import sleep
from misc import BANNER
from helpers import *
from datetime import datetime

class Alpha:
    _instance = None
    _user_info = None
    _prompt = '>'
    _intro = 'Hii, i\'m Alpha.'

    # Debug Handler
    class Debug:
        state = False
        @classmethod
        def check_log(cls, data, type='log'):
            if cls.state:
                with open('data/log.txt', 'a+') as log:
                    if type == 'log':
                        log.write(f'{datetime.now()} LOG -> {data}\n')
                    elif type == 'warning':
                        log.write(f'{datetime.now()} WARNING -> {data}\n')
                    elif type == 'error':
                        log.write(f'{datetime.now()} ERROR -> {data}\n')

        
    # Singleton DP
    def __init__(self):
        raise RuntimeError('call instance() instead')

    # loads user info from user_info.json file
    def load_user_info(self):
        with open('data/user_info.json', 'r') as user_info_file:
            self._user_info = load(user_info_file)
            self.Debug.check_log('Loaded user_info.json')

    # saves user info to user_info.json file
    def save_user_info(self):
        with open('data/user_info.json', 'w') as user_info_file:
            user_info_file.write(dumps(self._user_info))
            self.Debug.check_log('Saved to user_info.json')


    # singleton implementation
    @classmethod
    def instance(cls, debug=False):
        """
        Creates a new ``Alpha`` instance.
        The ``debug`` parameter can be set to True to enable debug messages.
        """
        cls.Debug.state = debug
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls.load_user_info(cls._instance)
            cls.Debug.check_log('Created new instance')
        return cls._instance

    # read user name if doesn't exist else load from file
    def check_get_user_name(self):
        name = self._user_info['name']
        if name == '':
            name = input('Enter your name : ')
            self.Debug.check_log(f'Created new user {name}')
        self._user_info['name'] = name
        self._intro = f'Welcome back {name}'
        self.save_user_info()

    # reads a user input
    def get_input(self):
        return input(f'{ColourPrint.Yellow(self._user_info["name"])} {self._prompt} ')

    # gives output to console, waits .5 seconds for improved experience
    def say(self, text=''):
        print(f'{ColourPrint.Green("Alpha")} {self._prompt} {text} ')
        print()
        sleep(0.5)

    # gives default intro message
    def give_intro(self):
        print(BANNER)
        self.say(self._intro)

    #gives default actions message
    def give_actions(self):
        self.say('I can do simple calculations, create stories from emojies or just talk!!!')

    # connects to dialogflow API and returns the response as dict
    def connect_agent(self, expression):
        response = load_from_agent(expression)
        self.Debug.check_log(f'Got response : {response}')
        response = clean_response(response.text)
        return json_to_dict(response)

    # detects intent from response of dialogflow
    def detect_intent(self, response_dict):
        try:
            intent =  response_dict['queryResult']['intent']['displayName']
            self.Debug.check_log(f'Got Intent : {intent}')
            return intent
        except KeyError:
            self.Debug.check_log(f'Got invalid intent from : {response_dict}', type='error')
            return None

    # do action according to given intent
    def do_actions(self, response_dict):
        intent = self.detect_intent(response_dict)
        if intent == 'jokes.get':
            self.say_joke(response_dict)
        elif intent == 'calculate-simple-expressions':
            self.do_simple_calculations(response_dict)

        elif intent == 'Default Welcome Intent':
            self.say(response_dict['queryResult']['fulfillmentText'])

        elif intent == 'Default Fallback Intent':
            if is_emoji(response_dict['queryResult']['queryText'][0]):
                self.emoji_to_story(response_dict) 
            else:
                self.say(response_dict['queryResult']['fulfillmentText'])
        else:
            if 'smalltalk' in response_dict['queryResult']['action']:
                self.say(response_dict['queryResult']['fulfillmentText'])
            else:
                self.say(ColourPrint.Red('Something is really really wrong!!'))

    # to do simple math calculations
    def do_simple_calculations(self, response_dict):
        self.Debug.check_log(f'Got Math: {response_dict["queryResult"]["parameters"]}')
        result = calculate_expression(response_dict['queryResult']['parameters'])
        self.Debug.check_log(f'Got Result: {result}')
        if result != None:
            self.say(f"{response_dict['queryResult']['queryText']} is {result}")
        else:
            print(f'It\'s too hard for me!!')

    # prints the joke got in response
    def say_joke(self, response_dict):
        self.say(f"Here is a joke: {response_dict['queryResult']['fulfillmentText']}")

    # tries to convert given emojies to a story
    def emoji_to_story(self, response_dict):
        emoji_string = response_dict['queryResult']['queryText']
        self.Debug.check_log(f'Got Emoji: {emoji_string}')
        story = generate_story_from_emoji(emoji_string)
        self.Debug.check_log(f'Got Story: {story}')
        self.say(story)

    # for CLI, runs the alpha untill user closes/KI
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
            self.Debug.check_log(f'Keyboard Interrupt')
            print()
            print()
            self.say('see ya later')
        
# example execution
if __name__ == '__main__':
    alpha = Alpha.instance(debug=True)
    alpha.run()