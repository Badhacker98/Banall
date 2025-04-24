from telethon import errors
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
import asyncio
import logging
from Banall import OWNER_ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BANNED_RIGHTS = ChatBannedRights(
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

async def ban_users(bot, event, cmd_name):
    chat = await event.get_chat()
    bot_me = await bot.get_me()

    if not chat.admin_rights or not chat.admin_rights.ban_users:
        await event.reply("I need `Ban Users` permission to run this command.")
        return

    total, success, failed = 0, 0, 0
    failed_users = []

    try:
        async for user in bot.iter_participants(chat):
            total += 1
            if user.id in [event.sender_id, bot_me.id]:
                continue

            try:
                await bot(EditBannedRequest(
                    channel=chat,
                    participant=user.id,
                    banned_rights=BANNED_RIGHTS
                ))
                success += 1
            except errors.UserAdminInvalidError:
                failed += 1
                failed_users.append(f"{user.id}: is admin")
            except errors.FloodWaitError as e:
                await asyncio.sleep(e.seconds)
                return await ban_users(bot, event, cmd_name)
            except Exception as e:
                failed += 1
                failed_users.append(f"{user.id}: {str(e)}")

            await asyncio.sleep(0.5)

    except Exception as e:
        logger.error(f"Error: {e}")
        await event.reply(f"Error occurred: `{e}`")
        return

    msg = (
        f"**Banall Report** for `{cmd_name}`\n"
        f"Total: `{total}`\n"
        f"Successful: `{success}`\n"
        f"Failed: `{failed}`"
    )
    await event.reply(msg)
