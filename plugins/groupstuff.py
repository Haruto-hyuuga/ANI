from bot import Bot
from pyrogram import Client, filters, errors
from pyrogram.types import Message

import asyncio
from config import ADMINS, BOT_ID, REQUEST_GC, ERR_TOPIC_ID, Vid_Random, OWNER
from config import USER_LOG_CHANNEL as LOGG
from database.database import present_chat, add_chat, full_chatbase, del_chat
from pyrogram.errors import FloodWait, Unauthorized, ChatWriteForbidden, UserNotParticipant
from database.inline import GC_START_B, Ani_log_group
from req import get_cmd
NCL_txt = """
#NEW_GROUP  ⛩️🟥
━━━━━━━━━━━━━━━
Title: {}
Public URL: @{}
CHAT ID: <code>{}</code>
{}
"""
GROUP_TEXT = """
Start me in private to discover all of my commands and functions, or to download amazing anime content. I'm excited to help you find your fav anime ♡
"""

NEW_GROUP_TEXT = """
Owo I've been brought into new world!
Thanks for having me in <b>{}</b>

To ensure that I can work properly, please make sure to promote me as an admin. I'm looking forward to helping you all ^_^
"""

async def new_gc_logger(client, chat_id, N, UN):
    try:
        link = await client.export_chat_invite_link(chat_id)
    except errors.ChatAdminRequired as e:
        link = "https://t.me/c/1909557377/9"
    except errors:
        link = "https://t.me/c/1909557377/22"
    LOG_BT = await Ani_log_group(link)
    h_id = f"#ID{(-1*chat_id)}"
    if not await present_chat(chat_id):
        await add_chat(chat_id)
        await client.send_message(LOGG, text=NCL_txt.format(N, UN, chat_id, h_id), reply_markup=LOG_BT)

            


@Bot.on_message(get_cmd(["start", "help"]) & filters.group)
async def on_startgclog(client, message):
    id = message.chat.id
    N = message.chat.title
    UN = message.chat.username
    try:
        await new_gc_logger(client, id, N, UN)
    except Exception as e:
        await client.send_message(REQUEST_GC, text=f"⚠️NEW GC LOG\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    video = await Vid_Random()
    await client.send_video(id, video, caption=GROUP_TEXT, reply_markup=GC_START_B)
    
 
@Bot.on_message(filters.new_chat_members & filters.user(BOT_ID))
async def welcomenewgc(client, message):
    id = message.chat.id
    N = message.chat.title
    UN = message.chat.username

    try:
        await new_gc_logger(client, id, N, UN)
    except Exception as e:
        await client.send_message(REQUEST_GC, text=f"⚠️NEW GC LOG\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    for member in message.new_chat_members:
        if member.id == BOT_ID:
            await asyncio.sleep(10)
            video = await Vid_Random()
            await client.send_video(message.chat.id, video, caption=NEW_GROUP_TEXT.format(N), reply_markup=GC_START_B)
    

Size_limit = 52428800
ci_alert_pic = "https://telegra.ph/file/ebe07cdaaa00689e247fc.jpg"
ci_alert_txt = """
⚠️ {}<b> please refrain from sending anime episodes or any files directly in the group chat that may infringe on copyright.</b>
Doing so could lead to copyright strike to group.
👤: @{}  🆔: <code>{}</code> 
"""
@Bot.on_message(filters.document | filters.video & filters.chat(FS_GROUP))
async def delfinedocorvideo(client, message):
    user_mention = message.from_user.mention
    user_id = message.from_user.id
    username = message.from_user.username
    if message.document:
        if message.document.file_size >= Size_limit:
            await message.delete()
            await bot.send_photo(
                photo=ci_alert_pic,
                caption=ci_alert_txt(user_mention, username, user_id)
            )
    if message.video:
        if message.video.file_size >= Size_limit:
            await message.delete()
            await bot.send_photo(
                photo=ci_alert_pic,
                caption=ci_alert_txt(user_mention, username, user_id)
            )





@Bot.on_message(get_cmd('anicastgc') & filters.user(OWNER))
async def gcbroadcastmsg(client, message):
    if message.reply_to_message:
        query = await full_chatbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        dbgct = len(query)
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("⏳")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except Unauthorized:
                unsuccessful += 1
            except ChatWriteForbidden:
                unsuccessful += 1
            except UserNotParticipant:
                await del_chat(chat_id)
                deleted += 1
                
                
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""Broadcast Completed📡
👥Total Groups: {dbgct}
📢Total Group Tried: {total} 
✅Successful: {successful}
⚠️Unsuccessful: {unsuccessful} // 🗑️Deleted: {deleted}
"""

        
        return await pls_wait.edit(status)

    else:
        await message.reply("Reply To the message")
