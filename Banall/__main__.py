import asyncio
import importlib
from config import START_IMG,OWNER_ID
from pyrogram import idle
from config import *

from Banall import LOGGER, app
from Banall.modules import ALL_MODULES


async def Banall_start():
    try:
        await Mukesh.start()
    except Exception as ex:
        LOGGER.error(ex)
        quit(1)

    for all_module in ALL_MODULES:
        importlib.import_module("Banall.modules." + all_module)

    LOGGER.info(f"@{app.username} Started.")
    await Mukesh.send_photo(OWNER_ID,START_IMG,"I am Alive")
    await idle()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(Banall_start())
    LOGGER.info("Stopping Banall bot")
