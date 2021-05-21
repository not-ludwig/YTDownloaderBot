# from typing import Text
from pytube import YouTube
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
import logging
# from telegram import Bot
import os

token = os.environ['TOKEN']

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
LINK = 0

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "I'm a bot, say something")

def get_link(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Send me the link you wish to download! ")
    return LINK

def download(update, context):
    video = YouTube(update.message.text)
    audio = video.streams.filter(only_audio=True).first()
    title = video.title

    pre = audio.download()
    
    post = os.path.splitext(pre)[0]

    
    os.rename(pre, post + '.mp3')

    context.bot.send_message(chat_id = update.effective_chat.id, text = 'Wait...') 
    context.bot.send_audio(chat_id = update.effective_chat.id, audio = open(title.replace(".", "") + '.mp3', 'rb'))
    
    
    # context.bot.send_photo(chat_id = update.effective_chat.id, photo = video.thumbnail_url) -- Video Thumbnail
    # print(video.title) -- Video Title
    
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