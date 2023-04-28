from bot import Bot
from pyrogram import Client, filters, errors
from pyrogram.types import Message

import asyncio
from config import ADMINS, BOT_ID
from config import USER_LOG_CHANNEL as LOGG
from database.database import present_chat, add_chat, full_chatbase, del_chat
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, ChatWriteForbidden, BotKicked, UserNotParticipant
from database.inline import GC_START_B, Ani_log_group

NCL_txt = """
#NEW_GROUP  ⛩️🟥
━━━━━━━━━━━━━━━
__Title:__ {}
__Public URL:__ @{}
__CHAT ID:__ `{}`
{}
"""
GROUP_TEXT = ""


async def get_invite_link(client, id):




@Bot.on_message(filters.command(["start", "help"]) & filters.group)
async def on_start(client, message):
    id = message.chat.id
    name = message.chat.title
    uname = message.chat.username
    h_id = f"#ID{(-1*id)}"
    try:
        link = await client.export_chat_invite_link(id)
    except errors.ChatAdminRequired as e:
        link = "https://t.me/c/1909557377/9"
    except errors:
        link = "https://t.me/c/1909557377/22"

    LOG_BT = await Ani_log_group(link)
    if not await present_chat(id):
        try:
            await add_chat(id)
            await client.send_message(LOGG, text=NCL_txt.format(name, uname, id, h_id), reply_markup=LOG_BT)
        except:
            pass
    video = await Vid_Random()
    await client.send_video(id, video, caption=GROUP_TEXT, reply_markup=GC_START_B)
    
 
@Bot.on_message(filters.new_chat_members & filters.user(BOT_ID))
async def welcome(client, message):
    chat_id = message.chat.id
    name = message.chat.title
    uname = message.chat.username
    h_id = f"#ID{(-1*chat_id)}"
    try:
        link = await client.export_chat_invite_link(chat_id)
    except errors.ChatAdminRequired as e:
        link = "https://t.me/c/1909557377/9"
    except errors:
        link = "https://t.me/c/1909557377/22"

    LOG_BT = await Ani_log_group(link)
 
    if not await present_chat(chat_id):
        try:
            await add_chat(chat_id)
            await client.send_message(LOG_CHANNEL, text=NCL_txt.format(name, uname, chat_id, h_id), reply_markup=LOG_BT)
        except:
            pass

    for member in message.new_chat_members:
        if member.id == BOT_ID:
            await asyncio.sleep(10)
            video = await Vid_Random()
            await client.send_video(message.chat.id, video, caption=GROUP_TEXT, reply_markup=GC_START_B)
    







@Bot.on_message(filters.command('gcbroadcast') & filters.user(ADMINS))
async def gcbroadcastmsg(client, message):
    if message.reply_to_message:
        query = await full_chatbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
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
            except UserIsBlocked:
                await del_chat(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_chat(chat_id)
                deleted += 1
            except ChatWriteForbidden:
                unsuccessful += 1
            except BotKicked:
                await del_chat(chat_id)
                deleted += 1
            except UserNotParticipant:
                await del_chat(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""Broadcast Completed📡
👥Total Groups: {total}
✅Successful: {successful}
⚠️Unsuccessful: {unsuccessful}
💀Deleted: {deleted}  || 🚫Error: {blocked}
"""
        
        return await pls_wait.edit(status)

    else:
        await message.reply("Reply To the message")
