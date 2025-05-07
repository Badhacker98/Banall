import sys
import asyncio
import importlib
from flask import Flask
import threading
from pyrogram import idle
from pyrogram.types import BotCommand
from config import OWNER_ID
from Banall import LOGGER, app
from Banall.modules import ALL_MODULES


async def anony_boot():
    try:
        await app.start()
    except Exception as ex:
        LOGGER.error(ex)
        sys.exit(1)

    for all_module in ALL_MODULES:
        importlib.import_module("Banall.modules." + all_module)
        LOGGER.info(f"ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ɪᴍᴘᴏʀᴛᴇᴅ: {all_module}")

    # Set bot commands
    try:
        await app.set_bot_commands(
            commands=[
                BotCommand("start", "✧ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ✧"),
                BotCommand("help", "✧ ɢᴇᴛ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇɴᴜ ✧"),
            ]
        )
        LOGGER.info("ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ ꜱᴇᴛ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ.")
    except Exception as ex:
        LOGGER.error(f"ꜰᴀɪʟᴇᴅ ᴛᴏ ꜱᴇᴛ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ: {ex}")

    LOGGER.info(f"@{app.username} Started.")
    try:
        await app.send_message(int(OWNER_ID), f"{app.mention} has started")
    except Exception as ex:
        LOGGER.info(f"@{app.username} ꜱᴛᴀʀᴛᴇᴅ, ᴘʟᴇᴀꜱᴇ ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ꜰʀᴏᴍ ᴏᴡɴᴇʀ ɪᴅ.")
    
    await idle()


# Flask Server Code for Health Check
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Start Flask server in a new thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Start the bot asynchronously
    asyncio.get_event_loop().run_until_complete(anony_boot())
    LOGGER.info("ꜱᴛᴏᴘᴘɪɴɢ ʙᴀɴᴀʟʟ ʙᴏᴛ...")
    
