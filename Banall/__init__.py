from pyrogram import Client
from telethon import TelegramClient
from telethon.sessions import StringSession
from telegram.ext import Application
import config

# Pyrogram Bot Client (With Bot Token)
app = Client(
    name="app", 
    api_id=config.APP_ID, 
    api_hash=config.HASH_ID, 
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="Banall.modules")
)


# Telethon Bot Client (With Bot Token)
bot = TelegramClient(
             session="Bad",  # Add a session name here
             api_id=config.APP_ID, 
             api_hash=config.HASH_ID
             ).start(bot_token=config.BOT_TOKEN)

