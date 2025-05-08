import asyncio
from telethon import events, functions
from telethon.errors import FloodWaitError
from telethon.tl.types import ChatBannedRights, ChannelParticipantsKicked

from Banall import bot 
from config import OWNER_ID

@bot.on(events.NewMessage(pattern=r"^\.unbanall$"))
async def unban_all_handler(event):
    if not event.is_group:
        return await event.reply("This command only works in groups.")

    if event.sender_id != OWNER_ID:
        return await event.reply("Only the owner can use this command.")

    msg = await event.reply("Searching banned users...")

    count = 0
    chat_id = event.chat_id

    async for user in bot.iter_participants(chat_id, filter=ChannelParticipantsKicked, aggressive=True):
        try:
            await bot(functions.channels.EditBannedRequest(
                chat_id,
                user.id,
                ChatBannedRights(until_date=0, view_messages=False)
            ))
            count += 1
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds + 3)
        except Exception as e:
            continue

    await msg.edit(f"✅ Unban Complete\nTotal Unbanned: {count}")
