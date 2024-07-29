# -*- coding: utf-8 -*-
from pytubefix import YouTube, exceptions
from telegram.ext import ConversationHandler
import os, time

SONG = 0
wait = "*Wait\.\.\.*"
working = "*Working on it\.\.\.*"
done = "*Done* ✅ *Sending ✉*"

def get_song(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Send me the link you wish to download!")
    # -- Hold value to use in Conversation Handler -- #
    return SONG

def download(update, context):
    # -- Get video info -- #
    try:
        video = YouTube(update.message.text)
        audio = video.streams.filter(only_audio=True).first()
        # title = video.title.translate(str.maketrans('','',".,'?#|;"))
        title = video.title.translate(str.maketrans('','',f"'#$%*.,\/:;<>?^|~\""))

        # -- Check if video reaches 20 minutes (1200 sec == 20 min) -- #
        if(video.length < 1200):
        # -- Download audio stream and change its extension --  #
            pre = audio.download()
            post = os.path.splitext(pre)[0]
            os.rename(pre, post + '.mp3')

            context.bot.send_message(chat_id = update.effective_chat.id, text = wait, parse_mode='MarkdownV2')
            time.sleep(2)
            context.bot.send_message(chat_id = update.effective_chat.id, text = working, parse_mode='MarkdownV2')
            time.sleep(2)
            context.bot.send_message(chat_id = update.effective_chat.id, text = done, parse_mode='MarkdownV2') 
            time.sleep(2)
            context.bot.send_audio(chat_id = update.effective_chat.id, audio = open(title + '.mp3', 'rb'))
            
            # -- Wait 1 seconds then delete the video file -- #
            time.sleep(1)
            os.remove(title + '.mp3')
            
            # -- End the conversation handler since input is not expected or alredy given -- #
            return ConversationHandler.END
            # -- Check if a valid link has been received -- #
        else:
            context.bot.send_message(chat_id = update.effective_chat.id, text = 'Video limit is 20 Minutes (storage), give me another link') 

    except exceptions.RegexMatchError as e:
        print(e)
        context.bot.send_message(chat_id = update.effective_chat.id, text = "Send me a valid link, please run /download again")
        return ConversationHandler.END
    except exceptions.VideoRegionBlocked as e:
        context.bot.send_message(chat_id = update.effective_chat.id, text = "This video is region locked, please run /download again with another video")
        return ConversationHandler.END