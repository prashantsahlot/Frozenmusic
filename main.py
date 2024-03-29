from pyrogram import Client, filters
from pytgcalls import GroupCallManager
from googleapiclient.discovery import build
import logging

# Import configuration from config.py
from .config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    YOUTUBE_API_KEY,
)

app = Client("your_bot_name", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_manager = GroupCallManager(app)
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

logging.basicConfig(level=logging.DEBUG)  # Enable debug logging (optional)

@app.on_message(filters.command(["join", "start"]))
async def join_chat(client, message):
    chat_id = message.chat.id
    await call_manager.join_group_call(chat_id)

@app.on_message(filters.command("play"))
async def play_music(client, message):
    query = message.text.split()[1]

    # Search for the video using YouTube Data API v3 (replace with your desired search logic)
    search_response = youtube.search().list(
        part='snippet',
        q=query,
        type='video'
    ).execute()

    try:
        video_id = search_response['items'][0]['id']['videoId']
        # You might need to handle potential errors here, e.g., no results found
        await call_manager.stream_video(chat_id=message.chat.id, video_id=video_id)
    except Exception as e:
        logging.error(f"Error playing video: {e}")
        await message.reply_text(f"An error occurred while playing the video.")

@app.on_message(filters.command("stop"))
async def stop_playing(client, message):
    await call_manager.leave_current_group_call()

if __name__ == "__main__":
    app.run()
