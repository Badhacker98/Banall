from config import *
import logging

from pyrogram import Client
from telethon import TelegramClient

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

LOGGER = logging.getLogger(__name__)

# Pyrogram Bot Initialization
app = Client(
    "BOT",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Banall.modules"),
)

# Telethon Bot Initialization
bot = TelegramClient(
    "TelethonBOT",
    api_id=API_ID,
    api_hash=API_HASH,
)
