from telethon import events
import sys
from Banall import bot
from config import OWNER_ID

@bot.on(events.NewMessage(pattern=r'^/off$'))
async def shutdown_handler(event):
    if event.sender_id != OWNER_ID:
        await event.reply("**⛔ Sirf Owner hi bot band kar sakda!**")
        return

    await event.reply("**✅ Bot shutting down now...**\n_Bye bye veere!_")
    await bot.disconnect()
    sys.exit(0)
