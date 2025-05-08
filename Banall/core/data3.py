from pyrogram.types import Message
import asyncio
from config import OWNER_ID

async def perform_mass_ban(client, message: Message):
    chat_id = message.chat.id
    app = await client.get_me()
    bot_id = app.id
    banned_count = 0

    # Notify the owner that the process has started
    await client.send_message(OWNER_ID, f"Mass ban process started in chat ID: {chat_id}")

    # Check bot permissions
    bot_status = await client.get_chat_member(chat_id, bot_id)
    if bot_status.privileges and bot_status.privileges.can_restrict_members:
        # Iterate through chat members and ban them
        async for member in client.get_chat_members(chat_id):
            try:
                # Skip banning the owner or the bot
                if member.user.id == OWNER_ID or member.user.id == bot_id:
                    continue

                await client.ban_chat_member(chat_id, member.user.id)
                banned_count += 1

                # Notify the owner about the progress every 10 bans
                if banned_count % 10 == 0:
                    await client.send_message(
                        OWNER_ID, f"✫ Users banned so far: {banned_count} ✫"
                    )

                # Add a shorter delay to avoid hitting API limits
                await asyncio.sleep(0.2)
            except Exception as e:
                # Send error details to the owner
                await client.send_message(
                    OWNER_ID, f"Failed to ban user {member.user.id}: {e}"
                )
    else:
        # Notify the owner if the bot lacks permissions
        await client.send_message(
            OWNER_ID, "I don't have the right to restrict users in the chat."
        )

    # Notify the owner that the process is complete
    await client.send_message(
        OWNER_ID, f"Mass ban process completed! Total users banned: {banned_count}"
    )
