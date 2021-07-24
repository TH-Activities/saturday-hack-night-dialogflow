require('dotenv').config()
const Discord = require('discord.js');
const fs = require('fs');
const dialogflow = require('@google-cloud/dialogflow');
const uuid = require('uuid')

const projectId = process.env.PROJECT_ID;
const serviceAccount = process.env.SERVICE_ACCOUNT;
const privateKey = process.env.PRIVATE_KEY;
const client = new Discord.Client()

const sessionClient = new dialogflow.SessionsClient({
  credentials:{
    private_key:privateKey,
    client_email:serviceAccount
  }
})
client.on('message', async message => {
  if (message.author.bot) return;
    if(message.guild === null){
        const { content , author } = message;
        const sessionId = uuid.v4();
        const sessionPath = sessionClient.projectAgentSessionPath(
          projectId,
          sessionId
        );
        const request = {
          session: sessionPath,
          queryInput: {
            text: {
              text: content,
              languageCode: 'en-US',
            },
          },
        };
        console.log(request);
        const responses = await sessionClient.detectIntent(request);
        const result = responses[0].queryResult.fulfillmentText;
        message.reply(result);
    }
})

//Login 
client.login(process.env.BOT_TOKEN).then(() => {
  console.log(`Discowin: Logged in`)
})