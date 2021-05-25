# -- Imports -- #

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from dotenv import load_dotenv
import logging
import os
import playlist
import download

# -- The correct way to import a token stored in .env file -- #
# -- It configures your local enviromental variable and merge to the enviromental variable tree -- #
load_dotenv() 
token = os.getenv('token')

# -- Basic Setup -- #
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot_greeting = "*Hi, I'm the Youtube Downloader bot\nRun */download *to start downloading your favorite music\nIf I somehow misbehave contact my maker from the profile info*"
saving = "*To save a song*\nOn mobile📱: Long press the audio and press the download button up top\. \nOn PC💻: Right Click on the audio and choose 'Save audio file As\.\.\.'"

# -- Main Commands -- #
def start(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = bot_greeting, parse_mode='MarkdownV2')

def save(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = saving, parse_mode='MarkdownV2')

start_handler = CommandHandler('start', start)
save_handler = CommandHandler('how', save)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(save_handler)

dispatcher.add_handler(ConversationHandler(
    entry_points=[
        CommandHandler('download', download.get_song)
    ],

    states={
        download.SONG: [MessageHandler(Filters.text, download.download)]
    },

    fallbacks=[],
))

dispatcher.add_handler(ConversationHandler(
     entry_points=[
        CommandHandler('playlist', playlist.get_playlist)
    ],

    states={
        playlist.PLAYLIST: [MessageHandler(Filters.text, playlist.playlist)]
    },

    fallbacks=[],
))

updater.start_polling()
