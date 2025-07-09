# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import logging
from info import ADMINS
from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.connections_mdb import add_connection, all_connections, if_active, delete_connection

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@Client.on_message((filters.private | filters.group) & filters.command('connect'))
async def addconnection(client, message):
    """Handle connection requests between users and groups"""
    try:
        userid = message.from_user.id if message.from_user else None
        if not userid:
            return await message.reply(
                "You are anonymous admin. Use /connect {message.chat.id} in PM",
                quote=True
            )

        chat_type = message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            try:
                cmd, group_id = message.text.split(" ", 1)
                group_id = group_id.strip()
                if not group_id.isdigit():
                    raise ValueError("Group ID must be numeric")
            except Exception as e:
                logger.error(f"Invalid connect command format: {e}")
                return await message.reply_text(
                    "<b>Enter in correct format!</b>\n\n"
                    "<code>/connect groupid</code>\n\n"
                    "<i>Get your Group id by adding this bot to your group and use <code>/id</code></i>",
                    quote=True
                )

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            group_id = message.chat.id
        else:
            return await message.reply_text(
                "This command can only be used in private chats or groups",
                quote=True
            )

        # Verify user is admin in the group
        try:
            st = await client.get_chat_member(group_id, userid)
            if (
                st.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
                and userid not in ADMINS
            ):
                return await message.reply_text(
                    "You must be an admin in the group to connect it!",
                    quote=True
                )
        except Exception as e:
            logger.error(f"Error checking admin status: {e}")
            return await message.reply_text(
                "Invalid Group ID or I'm not in that group!\n\n"
                "If correct, make sure I'm added to your group with admin rights.",
                quote=True
            )

        # Verify bot is admin in the group
        try:
            st = await client.get_chat_member(group_id, "me")
            if st.status != enums.ChatMemberStatus.ADMINISTRATOR:
                return await message.reply_text(
                    "Please make me admin in the group first!",
                    quote=True
                )

            # Add connection to database
            chat = await client.get_chat(group_id)
            addcon = await add_connection(str(group_id), str(userid))
            
            if addcon:
                success_msg = f"✅ Successfully connected to **{chat.title}**\nNow manage your group from my PM!"
                await message.reply_text(
                    success_msg,
                    quote=True,
                    parse_mode=enums.ParseMode.MARKDOWN
                )
                
                if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    await client.send_message(
                        userid,
                        f"Connected to **{chat.title}**!",
                        parse_mode=enums.ParseMode.MARKDOWN
                    )
            else:
                await message.reply_text(
                    "⚠️ You're already connected to this group!",
                    quote=True
                )

        except Exception as e:
            logger.error(f"Connection error: {e}")
            await message.reply_text(
                "Some error occurred! Try again later.",
                quote=True
            )

    except Exception as e:
        logger.exception(f"Unexpected error in addconnection: {e}")
        await message.reply_text(
            "An unexpected error occurred. Please try again later.",
            quote=True
        )

@Client.on_message((filters.private | filters.group) & filters.command('disconnect'))
async def deleteconnection(client, message):
    """Handle disconnection requests"""
    try:
        userid = message.from_user.id if message.from_user else None
        if not userid:
            return await message.reply(
                "You are anonymous admin. Use /connect {message.chat.id} in PM",
                quote=True
            )

        chat_type = message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            return await message.reply_text(
                "Run /connections to view or disconnect from groups!",
                quote=True
            )

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            group_id = message.chat.id

            # Verify user has permission to disconnect
            try:
                st = await client.get_chat_member(group_id, userid)
                if (
                    st.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
                    and str(userid) not in ADMINS
                ):
                    return await message.reply_text(
                        "You must be an admin to disconnect this group!",
                        quote=True
                    )
            except Exception as e:
                logger.error(f"Error checking admin status for disconnect: {e}")
                return await message.reply_text(
                    "Error verifying your admin status. Please try again.",
                    quote=True
                )

            # Delete connection
            delcon = await delete_connection(str(userid), str(group_id))
            if delcon:
                await message.reply_text(
                    "✅ Successfully disconnected from this group",
                    quote=True
                )
            else:
                await message.reply_text(
                    "⚠️ This group isn't connected to me!\nUse /connect to connect it.",
                    quote=True
                )

    except Exception as e:
        logger.exception(f"Unexpected error in deleteconnection: {e}")
        await message.reply_text(
            "An unexpected error occurred. Please try again later.",
            quote=True
        )

@Client.on_message(filters.private & filters.command(["connections"]))
async def connections(client, message):
    """List all connected groups for a user"""
    try:
        userid = message.from_user.id
        groupids = await all_connections(str(userid))

        if not groupids:
            return await message.reply_text(
                "There are no active connections! Connect to some groups first.",
                quote=True
            )

        buttons = []
        valid_connections = 0

        for groupid in groupids:
            try:
                chat = await client.get_chat(int(groupid))
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{chat.title}{act}",
                            callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
                valid_connections += 1
            except Exception as e:
                logger.warning(f"Couldn't fetch chat {groupid}: {e}")
                # Optionally remove invalid connections from DB
                await delete_connection(str(userid), str(groupid))

        if valid_connections > 0:
            await message.reply_text(
                "🔗 Your connected groups:\n\n",
                reply_markup=InlineKeyboardMarkup(buttons),
                quote=True
            )
        else:
            await message.reply_text(
                "All your connections appear to be invalid. Please connect to groups again.",
                quote=True
            )

    except Exception as e:
        logger.exception(f"Unexpected error in connections: {e}")
        await message.reply_text(
            "Failed to fetch your connections. Please try again later.",
            quote=True
                )
