import asyncio
import importlib
from pyrogram import idle
from pyrogram.errors import FloodWait
from telethon.errors import FloodError
from telethon.sync import TelegramClient

from config import OWNER_ID, BOT_USERNAME
from Banall import app, bot
from Banall.logging import LOGGER as LOG
from Banall.modules import ALL_MODULES 


async def start_pyrogram():
    global app
    try:
        LOG.info("Starting Pyrogram Client...")
        app = app or await app.start()  # Ensure app is started only once
        LOG.info("Pyrogram Client started successfully.")
    except Exception as ex:
        LOG.error(f"Error starting Pyrogram Client: {ex}")
        raise ex


async def start_telethon():
    try:
        LOG.info("Starting Telethon Client...")
        # Directly start the session without requiring BOT_TOKEN
        await bot.start()  # Session starts directly
        LOG.info("Telethon Client started successfully.")
    except Exception as ex:
        LOG.error(f"Error starting Telethon Client: {ex}")
        raise ex


async def anony_boot():
    pyrogram_started = False
    telethon_started = False

    # Attempt to start Pyrogram Client
    try:
        await start_pyrogram()
        pyrogram_started = True
    except Exception as ex:
        LOG.warning(f"Pyrogram failed to start: {ex}. Continuing with Telethon only...")

    # Attempt to start Telethon Client
    try:
        await start_telethon()
        telethon_started = True
    except Exception as ex:
        LOG.warning(f"Telethon failed to start: {ex}. Continuing with Pyrogram only...")

    # Ensure at least one client is running
    if not pyrogram_started and not telethon_started:
        LOG.critical("Both Pyrogram and Telethon failed to start. Exiting...")
        quit(1)

    # Load all modules
    for all_module in ALL_MODULES:
        importlib.import_module("Banall.modules." + all_module)

    LOG.info(f"@{BOT_USERNAME} Started with fallback mechanism.")
    
    try:
        await idle()
    except (FloodWait, FloodError) as flood_ex:
        LOG.warning(f"Flood detected: {flood_ex}. Fallback mechanism will be activated.")
        if pyrogram_started:
            LOG.info("Stopping Pyrogram due to flood...")
            await app.stop()
            pyrogram_started = False
        elif telethon_started:
            LOG.info("Stopping Telethon due to flood...")
            await bot.disconnect()
            telethon_started = False

        # Attempt to restart the other client
        if not pyrogram_started:
            await start_pyrogram()
        if not telethon_started:
            await start_telethon()

    LOG.info("Stopping Banall Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(anony_boot())
