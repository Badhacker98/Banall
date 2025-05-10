from pyrogram.errors import FloodWait

MAX_CONCURRENT_BANS = 100000  # Limit to avoid hitting Telegram rate limits

async def ban_one_member(client, chat_id, member, user_id, banned_info, sem):
    async with sem:
        try:
            if member.user.id != user_id and member.user.id not in SUDOERS:
                await client.ban_chat_member(chat_id, member.user.id)
                banned_info["banned"] += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception:
            banned_info["failed"] += 1

async def ban_members(client, chat_id, user_id, total_members, msg):
    banned_info = {"banned": 0, "failed": 0}
    sem = asyncio.Semaphore(MAX_CONCURRENT_BANS)

    ok = await msg.reply_text(
        f"Total members found: {total_members}\n**Started Banning Quickly...**"
    )

    tasks = []
    async for member in client.get_chat_members(chat_id):
        task = asyncio.create_task(ban_one_member(client, chat_id, member, user_id, banned_info, sem))
        tasks.append(task)

    await asyncio.gather(*tasks)

    await ok.edit_text(
        f"Total banned: {banned_info['banned']}\nFailed: {banned_info['failed']}"
    )

@Client.on_message(filters.command("banall") & filters.user(OWNER_ID))
async def ban_all(client, msg):
    chat_id = msg.chat.id
    user_id = msg.from_user.id
    BOT_ID = client.me.id
    bot = await client.get_chat_member(chat_id, BOT_ID)
    
    if bot.privileges.can_restrict_members:
        total_members = 0
        async for _ in client.get_chat_members(chat_id):
            total_members += 1

        await ban_members(client, chat_id, user_id, total_members, msg)
    else:
        await msg.reply_text(
            "I don't have the right to restrict users or you are not authorized."
        )
