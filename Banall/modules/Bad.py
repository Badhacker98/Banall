from telethon import events
from Banall import bot
from Banall.core.data import ban_users

commands = ["bad", "bad1", "bad2", "bad3", "bad4", "bad5", "bad6"]

for cmd in commands:
    pattern = fr"^({cmd})$"

    @bot.on(events.NewMessage(pattern=pattern))
    async def handler(event, cmd_name=cmd):
        await ban_users(bot, event, cmd_name)
