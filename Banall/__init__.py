import logging
import time
from Abg import patch
from pyrogram import Client
from telethon import TelegramClient
from pyrogram.enums import ParseMode
import config
import uvloop
from config import API_ID, API_HASH, BOT_TOKEN

uvloop.install()

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)
boot = time.time()
OWNER = config.OWNER_ID

if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise ValueError("API_ID, API_HASH, and BOT_TOKEN must be set in config.py")

app = Client(
    "BOT",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Banall.modules")
)

bot = TelegramClient(
    "TelethonBOT",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def start(self):
    await super().start()
    self.id = self.me.id
    self.name = self.me.first_name + " " + (self.me.last_name or "")
    self.username = self.me.username
    self.mention = self.me.mention

async def stop(self):
    await super().stop()

LOG.info("Starting the bots...")
