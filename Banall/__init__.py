import logging
import time
from Abg import patch
from pyrogram import Client
from telethon import TelegramClient
from pyrogram.enums import ParseMode
import config
import uvloop

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

# Initialize Pyrogram Client
app = Client(
    "BOT",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    plugins=dict(root="Banall.modules")
)

# Initialize Telethon Client
bot = TelegramClient(
    "TelethonBOT",
    api_id=API_ID,
    api_hash=API_HASH
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
