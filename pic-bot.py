import os
import time
import asyncio
from glob import glob
from telegram import Bot
from telegram.error import RetryAfter

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '52xxx295:AAGWCrQKxxguS1pN4rMBMLxxxktLvw'
channel_id = -1002100060  # Use the negative channel ID for public channels

# Adjust these values as needed
DELAY_BETWEEN_REQUESTS = 30  # Delay in seconds between each request

bot = Bot(token=bot_token)
sent_pictures_file = 'sent_pictures.txt'

def save_sent_pictures(sent_pictures):
    with open(sent_pictures_file, 'w') as file:
        for picture_path in sent_pictures:
            file.write(f"{picture_path}\n")

def load_sent_pictures():
    sent_pictures = set()
    if os.path.exists(sent_pictures_file):
        with open(sent_pictures_file, 'r') as file:
            for line in file:
                sent_pictures.add(line.strip())
    return sent_pictures

async def send_picture(file_path, caption):
    try:
        with open(file_path, 'rb') as photo:
            await bot.send_photo(chat_id=channel_id, photo=photo, caption=caption)
            sent_pictures.add(file_path)
            save_sent_pictures(sent_pictures)
        print(f"Success: {caption}")
    except RetryAfter as e:
        print(f"Retry after {e.retry_after} seconds. Waiting...")
        await asyncio.sleep(e.retry_after)
        await send_picture(file_path, caption)
    except Exception as e:
        print(f"Error: {e}")

async def main():
    global sent_pictures
    sent_pictures = load_sent_pictures()

    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    picture_dir = script_dir  # Use the script's directory for pictures
    picture_files = sorted(glob(os.path.join(picture_dir, '*.jpg')) +
                           glob(os.path.join(picture_dir, '*.png')) +
                           glob(os.path.join(picture_dir, '*.gif')))

    for i, picture_file in enumerate(picture_files, start=1):
        if picture_file not in sent_pictures:
            caption = f"Picture {i}"
            await send_picture(picture_file, caption)
            await asyncio.sleep(DELAY_BETWEEN_REQUESTS)

if __name__ == "__main__":
    asyncio.run(main())
