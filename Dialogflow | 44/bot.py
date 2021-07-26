from __future__ import unicode_literals
import logging
import random
import hashlib
import math
import html
import sys
import os
import json
import nltk
from nltk.corpus import wordnet
import operator
from collections import OrderedDict

from praw.reddit import Subreddit
from time import sleep
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters 
from telegram import Bot
from datetime import datetime
from google.cloud import dialogflow
import praw
log = logging.getLogger(__name__)
channel="feelmememebot"

TTOKEN=os.environ['TELEGRAM_BOT_TOKEN']
bot = Bot(token=TTOKEN)
PROJECT_ID="newagent-ufao"

reddit = praw.Reddit(client_id = os.environ['REDDIT_CID'], 
                        client_secret = os.environ['REDDIT_CSC'], 
                        user_agent = os.environ['USER_AGENT'])
subreddit= reddit.subreddit("Memes+Dankmemes")
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def prev_submissions():
    try:
        with open('prev_submissions.id', 'r') as f:
            return f.read().strip()
    except:
        return None
def write_submissions(sub_id):
    try:
        with open('prev_submissions.id', 'w') as f:
            f.write(sub_id)
    except:
        log.expection("Error writing sub ID!")

post = False
last_sub_id = prev_submissions()
if not last_sub_id:
    log.info("Latest submission not found, starting all submissions!")
    post = True
else:
    log.info("Last posted submission is {}".format(last_sub_id))
start_time = datetime.utcnow().timestamp()
def fetch_reddit(words):    
    seo={}
    global post,last_sub_id      
    try:
        for submission in subreddit.hot():
            try:

                title = html.escape(submission.title or '')
                link = "https://redd.it/{id}".format(id=submission.id)

                for word in words:
                    if title.find(word) != -1:
                        if submission.id in seo:
                            seo[submission.id]=seo[submission.id]+1
                        else:
                            seo[submission.id]=1

            except Exception as e:
                log.exception("Error parsing {}".format(link))
    except Exception as e:
        log.exception("Error fetching new submissions, restarting in 10 secs")
        sleep(10)
    if len(seo) <=0:
        bot.send_message(chat_id=816449476,text="No new memes related to your mood in hot feed :(, sadness intensifies...")
        return
    keyMax = max(seo.items(), key = operator.itemgetter(1))[0]
    if keyMax==last_sub_id:
        seo[keyMax]=-1
        max(seo.iteritems(), key=operator.itemgetter(1))[0]
        keyMax = max(seo.items(), key = operator.itemgetter(1))[0]
    else:
        for submission in subreddit.hot():
            if keyMax==submission.id:
                link = "https://redd.it/{id}".format(id=submission.id)
                image = html.escape(submission.url or '')
                title = html.escape(submission.title or '')
                user = html.escape(submission.author.name or '')

                template = "{title}\n{link}\nby {user}"
                message = template.format(title=title, link=link, user=user)


                bot.sendPhoto(chat_id=816449476, photo=submission.url, caption=message)
                # bot.sendMessage(chat_id=channel, parse_mode=telegram.ParseMode.HTML, text=message)
                write_submissions(submission.id)
                return
        else:
            bot.send_message(chat_id=816449476,text="No new memes related to your mood in hot feed :(, sadness intensifies...")
            return

                        

def detect_intent_with_sentiment_analysis(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs and analyzes the
    sentiment of the query text.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session_path = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session_path))
    i=0
    score=0
 
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    # Enable sentiment analysis
    sentiment_config = dialogflow.SentimentAnalysisRequestConfig(
        analyze_query_text_sentiment=True
    )

    # Set the query parameters with sentiment analysis
    query_params = dialogflow.QueryParameters(
        sentiment_analysis_request_config=sentiment_config
    )

    response = session_client.detect_intent(
        request={
            "session": session_path,
            "query_input": query_input,
            "query_params": query_params,
        }
    )
    score= response.query_result.sentiment_analysis_result.query_text_sentiment.score
    texts=texts.split(' ')
    mx=-1
    word=[]
    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)
        sentiment_config = dialogflow.SentimentAnalysisRequestConfig(
            analyze_query_text_sentiment=True
        )

    # Set the query parameters with sentiment analysis
        query_params = dialogflow.QueryParameters(
            sentiment_analysis_request_config=sentiment_config
        )
        response = session_client.detect_intent(
        request={
            "session": session_path,
            "query_input": query_input,
            "query_params": query_params,
        }
        )
        s=response.query_result.sentiment_analysis_result.query_text_sentiment.score
        if s > 0.1 or s < -0.1:
            word.append(response.query_result.query_text)
    words=[]
    for w in word:
        for synset in wordnet.synsets(w):
            for lemma in synset.lemmas():
                if len(lemma.name()) > 3:
                    words.append(lemma.name())    #add the synonyms
    return (score,words)  

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def reply(update, context):
    """Echo the user message."""
    print(update.update_id)
    res= detect_intent_with_sentiment_analysis(PROJECT_ID,update.update_id,update.message.text, "en")
    
    update.message.reply_text(str(res[0]))
    print(res[1])
    fetch_reddit(res[1])

def error(update, context):
    """Log Errors caused by Updates."""
    log.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TTOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, reply))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()