# #Team Id: 22.

## Mood Meme Generator

Generates meme based on user's input mood (using DialogFlow api to find mood)

Working:
- DialogFlow API used, trained a set of 4 moods using example phrases
- Express server hosted on glitch.com to interact with dialogflow
- Frontend hosted on firebase
- Frontend accepts user input, sends to dialogflow to get mood.
- The mood is then mapped to a set of meme templates, after which user input text is imprinted over the meme using imgflip api

Dialogflow api to get the mood - https://defiant-tabby-climb.glitch.me/meme/{query}

Live demo: https://moodmemeth.web.app/