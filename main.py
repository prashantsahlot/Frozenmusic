
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from pytube import YouTube
from pydub import AudioSegment
from pydub.playback import play

# Telegram Bot Token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

def start(update, context):
    update.message.reply_text('Welcome to the VC Music Bot!')

def play_song(update, context):
    # Download and play the song
    song_url = context.args[0]
    update.message.reply_text(f'Playing song from {song_url}')
    
    # Download song using pytube
    yt = YouTube(song_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(filename='song.mp3')

    # Convert to WAV format
    audio = AudioSegment.from_mp3('song.mp3')
    audio.export('song.wav', format='wav')

    # Play the song
    play(audio)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("play", play_song))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
