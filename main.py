# -- Imports -- #

from pytube import YouTube
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
import logging
import os
import time
from dotenv import load_dotenv

# -- The correct way to import a token stored in .env file -- #
# -- It configures your local enviromental variable and merge to the enviromental variable tree -- #
load_dotenv() 
token = os.getenv('token')

# -- Basic Setup -- #
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher
LINK = 0
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# -- Main Commands -- #
def start(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "I'm a bot, say something")

def get_link(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Send me the link you wish to download! ")
    # -- Hold value to use in Conversation Handler -- #
    return LINK 

def download(update, context):
    # -- Get video info -- #
    video = YouTube(update.message.text)
    audio = video.streams.filter(only_audio=True).first()
    title = video.title.translate(str.maketrans('','',".,'"))
    
    # -- Download audio stream and change its extension --  #
    pre = audio.download()
    post = os.path.splitext(pre)[0]
    os.rename(pre, post + '.mp3')

    context.bot.send_message(chat_id = update.effective_chat.id, text = 'Wait...') 
    context.bot.send_audio(chat_id = update.effective_chat.id, audio = open(title + '.mp3', 'rb'))
    
    # -- Wait 5 seconds then delete the video file -- #
    time.sleep(5)
    os.remove(title + '.mp3')
    # -- End the conversation handler since input is not expected or alredy given -- #
    return ConversationHandler.END

start_handler = CommandHandler('start', start)

dispatcher.add_handler(start_handler)

dispatcher.add_handler(ConversationHandler(
    entry_points=[
        CommandHandler('download', get_link)
    ],

    states={
        LINK: [MessageHandler(Filters.text, download)]
    },

    fallbacks=[],
))

updater.start_polling()
