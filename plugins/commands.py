# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os, string, logging, random, asyncio, time, datetime, re, sys, json, base64
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait, MessageNotModified, PeerIdInvalid
from pyrogram.types import *
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id, get_bad_files
from database.users_chats_db import db, delete_all_referal_users, get_referal_users_count, get_referal_all_users, referal_add_user
from database.join_reqs import JoinReqs
from info import CLONE_MODE, CHANNELS, REQUEST_TO_JOIN_MODE, TRY_AGAIN_BTN, ADMINS, SHORTLINK_MODE, PREMIUM_AND_REFERAL_MODE, STREAM_MODE, AUTH_CHANNEL, OWNER_USERNAME, REFERAL_PREMEIUM_TIME, REFERAL_COUNT, PAYMENT_TEXT, PAYMENT_QR, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, CHNL_LNK, GRP_LNK, REQST_CHANNEL, SUPPORT_CHAT_ID, SUPPORT_CHAT, MAX_B_TN, VERIFY, SHORTLINK_API, SHORTLINK_URL, TUTORIAL, VERIFY_TUTORIAL, IS_TUTORIAL, URL
from utils import get_settings, pub_is_subscribed, get_size, is_subscribed, save_group_settings, temp, verify_user, check_token, check_verification, get_token, get_shortlink, get_tutorial, get_seconds
from database.connections_mdb import active_connection
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size

logger = logging.getLogger(__name__)
BATCH_FILES = {}
join_db = JoinReqs

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    try:
        await message.react(emoji="❤️‍🔥")
        
        if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            buttons = [
                [
                    InlineKeyboardButton('ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴏᴜʀ ɢʀᴏᴜᴘ', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                ],
                [
                    InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url="https://t.me/KeralaLeechHelp"),
                    InlineKeyboardButton('ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘ', url='https://t.me/CJMovieSearch')
                ],
                [
                    InlineKeyboardButton('ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ', url='https://t.me/KeralaLeechHelp')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(
                script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME),
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
            
            await asyncio.sleep(2)
            if not await db.get_chat(message.chat.id):
                total = await client.get_chat_members_count(message.chat.id)
                await client.send_message(
                    LOG_CHANNEL,
                    script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown")
                )
                await db.add_chat(message.chat.id, message.chat.title)
            return

        # Add new user to database
        if not await db.is_user_exist(message.from_user.id):
            await db.add_user(message.from_user.id, message.from_user.first_name)
            await client.send_message(
                LOG_CHANNEL,
                script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention)
            )

        # Handle deep linking
        if len(message.command) != 2:
            buttons = await get_start_buttons()
            m = await message.reply_sticker("CAACAgUAAxkBAAEKVaxlCWGs1Ri6ti45xliLiUeweCnu4AACBAADwSQxMYnlHW4Ls8gQMAQ")
            await asyncio.sleep(1)
            await m.delete()
            
            await message.reply_photo(
                photo=random.choice(PICS),
                caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )
            return

        # Handle auth channel subscription
        if AUTH_CHANNEL and not await is_subscribed(client, message):
            try:
                invite_link = await client.create_chat_invite_link(
                    int(AUTH_CHANNEL),
                    creates_join_request=REQUEST_TO_JOIN_MODE
                )
            except ChatAdminRequired:
                logger.error("Make sure Bot is admin in Forcesub channel")
                return
            
            btn = [[InlineKeyboardButton("ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url=invite_link.invite_link)]]
            
            if message.command[1] != "subscribe":
                try:
                    kk, file_id = message.command[1].split("_", 1)
                    btn.append([InlineKeyboardButton("Tʀʏ Aɢᴀɪɴ", callback_data=f"checksub#{kk}#{file_id}")])
                except (IndexError, ValueError):
                    btn.append([InlineKeyboardButton("Tʀʏ Aɢᴀɪɴ", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
            
            text = (
                "**ᴊᴏɪɴ ᴛʜᴇ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ɢᴇᴛ ᴍᴏᴠɪᴇ ғɪʟᴇ**\n\n"
                "ғɪʀsᴛ ᴄʟɪᴄᴋ ᴏɴ ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ"
            )
            
            await client.send_message(
                chat_id=message.from_user.id,
                text=text,
                reply_markup=InlineKeyboardMarkup(btn),
                parse_mode=enums.ParseMode.MARKDOWN
            )
            return

        # Handle referral links
        if data.split("-", 1)[0] == "Tom":
            await handle_referral(client, message)
            return

        # Handle file sending
        await handle_file_sending(client, message)

    except Exception as e:
        logger.error(f"Error in start command: {str(e)}", exc_info=True)
        await message.reply("An error occurred. Please try again later.")

async def get_start_buttons():
    if PREMIUM_AND_REFERAL_MODE:
        buttons = [
            [
                InlineKeyboardButton('ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],
            [
                InlineKeyboardButton('ᴇᴀʀɴ ᴍᴏɴᴇʏ', callback_data="shortlink_info"),
                InlineKeyboardButton('ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘ', url=GRP_LNK)
            ],
            [
                InlineKeyboardButton('ʜᴇʟᴘ', callback_data='help'),
                InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about')
            ],
            [
                InlineKeyboardButton('💳 Gᴇᴛ Fʀᴇᴇ Oʀ Pᴀɪᴅ Sᴜʙsᴄʀɪᴘᴛɪᴏɴ 💳', callback_data='subscription')
            ],
            [
                InlineKeyboardButton('Jᴏɪɴ ᴋᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ', url=CHNL_LNK)
            ]
        ]
    else:
        buttons = [
            [
                InlineKeyboardButton('ᴀᴅᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],
            [
                InlineKeyboardButton('ᴇᴀʀɴ ᴍᴏɴᴇʏ', callback_data="shortlink_info"),
                InlineKeyboardButton('ᴍᴏᴠɪᴇ ɢʀᴏᴜᴘ', url=GRP_LNK)
            ],
            [
                InlineKeyboardButton('ʜᴇʟᴘ', callback_data='help'),
                InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about')
            ],
            [
                InlineKeyboardButton('ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ', url=CHNL_LNK)
            ]
        ]
    
    if CLONE_MODE:
        buttons.append([InlineKeyboardButton('🤖 Cʀᴇᴀᴛᴇ Yᴏᴜʀ Oᴡɴ Cʟᴏɴᴇ Bᴏᴛ 🤖', callback_data='clone')])
    
    return buttons

async def handle_referral(client, message):
    data = message.command[1]
    user_id = int(data.split("-", 1)[1])
    vj = await referal_add_user(user_id, message.from_user.id)
    
    if vj and PREMIUM_AND_REFERAL_MODE:
        await message.reply(
            f"<b>You have joined using the referral link of user with ID {user_id}\n\n"
            "Send /start again to use the bot</b>"
        )
        num_referrals = await get_referal_users_count(user_id)
        await client.send_message(
            chat_id=user_id,
            text=f"<b>{message.from_user.mention} started the bot with your referral link\n\n"
            f"Total Referrals - {num_referrals}</b>"
        )
        
        if num_referrals == REFERAL_COUNT:
            time = REFERAL_PREMEIUM_TIME
            seconds = await get_seconds(time)
            if seconds > 0:
                expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
                user_data = {"id": user_id, "expiry_time": expiry_time}
                await db.update_user(user_data)
                await delete_all_referal_users(user_id)
                await client.send_message(
                    chat_id=user_id,
                    text=f"<b>You Have Successfully Completed Total Referral.\n\n"
                    f"You Added In Premium For {REFERAL_PREMEIUM_TIME}</b>"
                )
        return
    
    buttons = await get_start_buttons()
    m = await message.reply_sticker("CAACAgUAAxkBAAEKVaxlCWGs1Ri6ti45xliLiUeweCnu4AACBAADwSQxMYnlHW4Ls8gQMAQ")
    await asyncio.sleep(1)
    await m.delete()
    
    await message.reply_photo(
        photo=random.choice(PICS),
        caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

async def handle_file_sending(client, message):
    data = message.command[1]
    
    if data.split("-", 1)[0] == "BATCH":
        await handle_batch_files(client, message)
        return
    
    elif data.split("-", 1)[0] == "DSTORE":
        await handle_dstore_files(client, message)
        return
    
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""
    
    files = await get_file_details(file_id)
    if not files:
        await message.reply("File not found in database. It may have been deleted.")
        return
    
    for file in files:
        f_caption = file.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(
                    file_name=file.file_name,
                    file_size=get_size(file.file_size),
                    file_caption=file.caption
                )
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        
        if f_caption is None:
            f_caption = f"{file.file_name}"
        
        try:
            if STREAM_MODE:
                log_msg = await client.send_cached_media(
                    chat_id=LOG_CHANNEL,
                    file_id=file.file_id
                )
                fileName = quote_plus(get_name(log_msg))
                stream = f"{URL}watch/{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}"
                download = f"{URL}{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}"
                
                await log_msg.reply_text(
                    text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{message.from_user.id}\n"
                    f"•• ᴜꜱᴇʀɴᴀᴍᴇ : {message.from_user.mention}\n\n"
                    f"•• ᖴᎥᒪᗴ Nᗩᗰᗴ : {fileName}",
                    quote=True,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🚀 Fast Download 🚀", url=download)],
                        [InlineKeyboardButton('🖥️ Watch online 🖥️', url=stream)]
                    ])
                )
                
                button = [
                    [InlineKeyboardButton('𝗌ᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url=f'https://t.me/{SUPPORT_CHAT}'),
                     InlineKeyboardButton('𝗎ᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ', url=CHNL_LNK)],
                    [InlineKeyboardButton('𝗕𝗢𝗧 𝗢𝗪𝗡𝗘𝗥', url="https://t.me/KeralaLeech")],
                    [InlineKeyboardButton("🚀 Fast Download 🚀", url=download),
                     InlineKeyboardButton('🖥️ Watch online 🖥️', url=stream)],
                    [InlineKeyboardButton("• ᴡᴀᴛᴄʜ ɪɴ ᴡᴇʙ ᴀᴘᴘ •", web_app=WebAppInfo(url=stream))]
                ]
            else:
                button = [
                    [InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url=f'https://t.me/{SUPPORT_CHAT}'),
                     InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ', url=CHNL_LNK)],
                    [InlineKeyboardButton('𝗕𝗢𝗧 𝗢𝗪𝗡𝗘𝗥', url="https://t.me/KeralaLeech")]
                ]
            
            await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file.file_id,
                caption=f_caption,
                protect_content=file.protect,
                reply_markup=InlineKeyboardMarkup(button)
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file.file_id,
                caption=f_caption,
                protect_content=file.protect,
                reply_markup=InlineKeyboardMarkup(button)
            )
        except Exception as e:
            logger.error(f"Failed to send file {file.file_id}: {str(e)}")
            await message.reply("Failed to send file. Please try again later.")

async def handle_batch_files(client, message):
    sts = await message.reply("<b>Please wait...</b>")
    file_id = data.split("-", 1)[1]
    msgs = BATCH_FILES.get(file_id)
    
    if not msgs:
        file = await client.download_media(file_id)
        try:
            with open(file) as file_data:
                msgs = json.loads(file_data.read())
            os.remove(file)
            BATCH_FILES[file_id] = msgs
        except Exception as e:
            await sts.edit("Failed to process batch file")
            await client.send_message(LOG_CHANNEL, f"BATCH FILE ERROR: {str(e)}")
            return
    
    filesarr = []
    warning_sent = False
    
    for msg in msgs:
        title = msg.get("title")
        size = get_size(int(msg.get("size", 0)))
        f_caption = msg.get("caption", "")
        
        if BATCH_FILE_CAPTION:
            try:
                f_caption = BATCH_FILE_CAPTION.format(
                    file_name='' if title is None else title,
                    file_size='' if size is None else size,
                    file_caption='' if f_caption is None else f_caption
                )
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        
        if f_caption is None:
            f_caption = f"{title}"
        
        try:
            if STREAM_MODE:
                log_msg = await client.send_cached_media(
                    chat_id=LOG_CHANNEL,
                    file_id=msg.get("file_id")
                )
                fileName = quote_plus(get_name(log_msg))
                stream = f"{URL}watch/{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}"
                download = f"{URL}{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}"
                
                await log_msg.reply_text(
                    text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{message.from_user.id}\n"
                    f"•• ᴜꜱᴇʀɴᴀᴍᴇ : {message.from_user.mention}\n\n"
                    f"•• ᖴᎥᒪᗴ Nᗩᗰᗴ : {fileName}",
                    quote=True,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🚀 Fast Download 🚀", url=download)],
                        [InlineKeyboardButton('🖥️ Watch online 🖥️', url=stream)]
                    ])
                )
                
                button = [
                    [InlineKeyboardButton('𝗌ᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url=f'https://t.me/{SUPPORT_CHAT}'),
                     InlineKeyboardButton('𝗎ᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ', url=CHNL_LNK)],
                    [InlineKeyboardButton('𝗕𝗢𝗧 𝗢𝗪𝗡𝗘𝗥', url="https://t.me/KeralaLeech")],
                    [InlineKeyboardButton("🚀 Fast Download 🚀", url=download),
                     InlineKeyboardButton('🖥️ Watch online 🖥️', url=stream)],
                    [InlineKeyboardButton("• ᴡᴀᴛᴄʜ ɪɴ ᴡᴇʙ ᴀᴘᴘ •", web_app=WebAppInfo(url=stream))]
                ]
            else:
                button = [
                    [InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url=f'https://t.me/{SUPPORT_CHAT}'),
                     InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ', url=CHNL_LNK)],
                    [InlineKeyboardButton('𝗕𝗢𝗧 𝗢𝗪𝗡𝗘𝗥', url="https://t.me/KeralaLeech")]
                ]
            
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=msg.get("file_id"),
                caption=f_caption,
                protect_content=msg.get('protect', False),
                reply_markup=InlineKeyboardMarkup(button)
            )
            filesarr.append(msg)
            
            if not warning_sent and len(filesarr) == 1:
                k = await client.send_message(
                    chat_id=message.from_user.id,
                    text="<b><u>❗️❗️❗️IMPORTANT❗️️❗️❗️</u></b>\n\n"
                    "This Movie Files/Videos will be deleted in <b><u>10 mins</u> 🫥 <i></b>(Due to Copyright Issues)</i>.\n\n"
                    "<b><i>Please forward this ALL Files/Videos to your Saved Messages and Start Download there</i></b>"
                )
                warning_sent = True
            
        except FloodWait as e:
            await asyncio.sleep(e.value)
            logger.warning(f"Floodwait of {e.value} sec.")
            continue
        except Exception as e:
            logger.warning(e, exc_info=True)
            continue
        
        await asyncio.sleep(1)
    
    await sts.delete()
    
    if filesarr:
        await asyncio.sleep(600)
        for x in filesarr:
            try:
                await x.delete()
            except:
                pass
        await k.edit_text("<b>Your All Files/Videos is successfully deleted!!!</b>")

async def handle_dstore_files(client, message):
    sts = await message.reply("<b>Please wait...</b>")
    b_string = data.split("-", 1)[1]
    decoded = (base64.urlsafe_b64decode(b_string + "=" * (-len(b_string) % 4))).decode("ascii")
    
    try:
        f_msg_id, l_msg_id, f_chat_id, protect = decoded.split("_", 3)
    except:
        f_msg_id, l_msg_id, f_chat_id = decoded.split("_", 2)
        protect = "/pbatch" if PROTECT_CONTENT else "batch"
    
    diff = int(l_msg_id) - int(f_msg_id)
    async for msg in client.iter_messages(int(f_chat_id), int(l_msg_id), int(f_msg_id)):
        if msg.media:
            media = getattr(msg, msg.media.value)
            # Add your file sending logic here
