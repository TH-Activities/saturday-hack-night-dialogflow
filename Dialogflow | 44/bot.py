
import logging
import random
import hashlib

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from google.cloud import dialogflow

SESSION_COUNTER=random.randint(0,200)
PROJECT_ID="newagent-ufao"
def gen_session_id(counter):
    h = hashlib.new('sha512_256')
    h.update(b"feelmememe"+str(counter))
    h.digest_size(36)
    return h.hexdigest()

def detect_intent_with_sentiment_analysis(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs and analyzes the
    sentiment of the query text.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session_path = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session_path))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

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

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
        # Score between -1.0 (negative sentiment) and 1.0 (positive sentiment).
        print(
            "Query Text Sentiment Score: {}\n".format(
                response.query_result.sentiment_analysis_result.query_text_sentiment.score
            )
        )
        print(
            "Query Text Sentiment Magnitude: {}\n".format(
                response.query_result.sentiment_analysis_result.query_text_sentiment.magnitude
            )
        )
        return response.query_result.sentiment_analysis_result.query_text_sentiment.score



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


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
    global SESSION_COUNTER
    session_id=gen_session_id(SESSION_COUNTER)
    SESSION_COUNTER+=1
    val= detect_intent_with_sentiment_analysis(PROJECT_ID,session_id,update.message.text, "en")
    update.message.reply_text(val)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1940340851:AAHMSeaV1YjRIhUlAHAG9NetMdYeZfP7N64", use_context=True)

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