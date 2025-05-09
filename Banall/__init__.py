import os
import logging
from pyrogram import Client
from telethon import TelegramClient
from config import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOG = logging.getLogger(__name__)

# Initialize Pyrogram Client
app = Client(
    "BOT",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Banall.modules")
)

# Initialize Telethon Client
bot = TelegramClient(
    "TelethonBOT",
    api_id=API_ID,
    api_hash=API_HASH
)

# Pyrogram Client methods
@app.on_connect
async def on_connect(client):
    client.id = client.me.id
    client.name = client.me.first_name + " " + (client.me.last_name or "")
    client.username = client.me.username
    client.mention = client.me.mention

async def start():
    await app.start()
    await bot.start(bot_token=BOT_TOKEN)
    LOG.info("Bots started successfully!")

async def stop():
    await app.stop()
    await bot.stop()
    LOG.info("Bots stopped.")

LOG.info("Starting the bots...")
