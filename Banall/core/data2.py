import asyncio
from telethon import functions
from telethon.errors import FloodWaitError
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins
from config import OWNER_ID

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True
)

async def ban_users(bot, event, cmd_name):
    if not event.is_group:
        return await event.reply("This command only works in groups.")

    me = await bot.get_me()
    perms = await bot.get_permissions(event.chat_id, me.id)
    if not perms.ban_users:
        return await event.reply("I need ban rights to do this.")

    admins = await bot.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
    admins_ids = [admin.id for admin in admins]

    total = 0
    success = 0

    async for user in bot.iter_participants(event.chat_id):
        total += 1
        # Skip admins and bots
        if user.id in admins_ids or user.bot:
            continue
        try:
            await bot(functions.channels.EditBannedRequest(
                event.chat_id,
                user.id,
                BANNED_RIGHTS
            ))
            success += 1
        except FloodWaitError as e:
            # Wait for FloodWaitError duration + 2 seconds
            await asyncio.sleep(e.seconds + 2)
        except Exception:
            # Generic exception handling
            await asyncio.sleep(0.5)

        # Reduce delay for faster execution
        await asyncio.sleep(0.1)

    # Send summary to OWNER_ID only
    await bot.send_message(
        OWNER_ID,
        f"**#BANALL**\n\n**Command:** `{cmd_name}`\n**Group:** `{event.chat.title}`\n**Successfully Banned:** `{success}` out of `{total}` members"
    )
