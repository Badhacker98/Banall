from pyrogram import Client
from telethon import TelegramClient
from telethon.sessions import StringSession
import config

# Pyrogram Bot Client (With Bot Token)
app = Client(
    name="app", 
    api_id=config.API_ID, 
    api_hash=config.API_HASH, 
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="Banall.modules")
)


# Telethon Bot Client (With Bot Token)
bot = TelegramClient(
             session="Bad",  # Add a session name here
             api_id=config.API_ID, 
             api_hash=config.API_HASH
             ).start(bot_token=config.BOT_TOKEN)

