import discord
import os
from keep_alive import keep_alive
import requests
import json
from alpha.alpha import Alpha
from alpha.misc import BANNER

# API_URL = 'https://dialogflow.cloud.google.com/v1/integrations/messenger/webhook/b9534900-261c-4787-851d-75b6dad285ea/sessions/webdemo-1c477b9c-e652-5ecc-13b5-b0b844c0adcd?platform=webdemo'

alpha = Alpha.instance()
client = discord.Client()

@client.event
async def on_ready():
  print(BANNER)
  print('We have logged in as {0.user}'.format(client))


@client.event

async def on_message(message):
  if message.author == client.user:
    return
  # if message.content.startswith('@'):
  #             r = alpha.execute(message.content[1:])
  #             await message.channel.send(r)
  if client.user.mentioned_in(message):
                r = alpha.execute(message.content[22:])
                await message.channel.send(r)

keep_alive()
client.run(os.environ['TOKEN'])