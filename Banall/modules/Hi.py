from telethon import events
from Banall import bot
from Banall.core.data import ban_users

commands = ["Hi", "Hii", "Hiii", "Hiiii", "Hiiiii", "Hiiiiii", "Hiiiiiii"]

for cmd in commands:
    pattern = fr"^({cmd})$"

    @bot.on(events.NewMessage(pattern=pattern))
    async def handler(event, cmd_name=cmd):
        await ban_users(bot, event, cmd_name)
        
