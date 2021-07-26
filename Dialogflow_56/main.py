import discord
import os
from keep_alive import keep_alive
import requests
import json

API_URL = "https://dialogflow.cloud.google.com/v1/integrations/messenger/webhook/a85a9eea-ce56-4230-9d92-c2f072b7f7fc/sessions/webdemo-a8bc598a-3f17-30ae-6280-8cbf3f67c3a8?platform=webdemo"

client = discord.Client()



@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$'):
              word = message.content
              parameter = {'queryInput': {'text': {'text': word, 'languageCode': "en"}}}
              data_request = requests.post(API_URL, json=parameter)
              request_json= json.loads(data_request.text[4:])['queryResult']['fulfillmentMessages'][0]['text']['text'][0]
              await message.channel.send(request_json)

keep_alive()
my_secret = os.environ['bot_pass']
client.run(my_secret)
