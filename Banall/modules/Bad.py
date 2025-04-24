from pyrogram import filters
from pyrogram.types import Message
from Banall import app
from Banall.core.data3 import perform_mass_ban

# Multiple command aliases
commands = ["Bad", "Bad1", "Bad2", "Bad3", "Bad4", "Bad5"]

for cmd in commands:
    @app.on_message(filters.command(cmd) & filters.group)
    async def ban_all_handler(client, message: Message, cmd_name=cmd):
        await perform_mass_ban(client, message)
