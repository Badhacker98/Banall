import asyncio
import importlib
from config import OWNER_ID
from pyrogram import idle
from config import *

from Banall import LOGGER, app, bot
from Banall.modules import ALL_MODULES

START_IMG = [
    "https://files.catbox.moe/tpo7zr.jpg",    
]


async def Banall_start():
    try:
        # Start Pyrogram Bot
        await app.start()
        LOGGER.info(f"Pyrogram Bot Started")
        
        # Start Telethon Bot
        await bot.start(bot_token=BOT_TOKEN)
        me = await bot.get_me()
        LOGGER.info(f"Telethon Bot Started ")
    except Exception as ex:
        LOGGER.error(ex)
        quit(1)

    # Automatically load all modules
    for all_module in ALL_MODULES:
        importlib.import_module("Banall.modules." + all_module)

    # Send Alive Message
    await app.send_photo(OWNER_ID, START_IMG, "I am Alive (Pyrogram Bot)")
    LOGGER.info("Both Pyrogram and Telethon clients started successfully.")
    await idle()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(Banall_start())
    LOGGER.info("Stopping Banall bot")
