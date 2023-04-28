from bot import Bot
from pyrogram import Client, filters
from pyrogram.types import Message

import asyncio
from config import ADMINS
from database.database import present_chat, add_chat, full_chatbase, del_chat
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, ChatWriteForbidden, BotKicked, UserNotParticipant

@Bot.on_message(filters.command(["start", "help"]) & filters.group)
async def on_start(client, message):
    id = message.chat.id
    name = message.chat.title
    uname = message.chat.username
    h_id = f"#ID{(-1*id)}"
    if not await present_chat(id):
        try:
            await add_chat(id)
            await client.send_message(LOG_CHANNEL, text=NEW_CHAT_LOG_TEXT.format(name, uname, id, h_id))
        except:
            pass
    video = random.choice(START_VIDEO)
    if id == FORCE_SUB_GROUP:
        await client.send_video(id, video, caption=MAIN_GROUP_TEXT, reply_markup=MAIN_GROUP_BUTTONS)
    else:
        await client.send_video(id, video, caption=OTHER_GROUP_TEXT.format(name), reply_markup=OTHER_GROUP_BUTTONS)
 
 
@Bot.on_message(filters.new_chat_members, group=1)
async def welcome(client, message):
    chat_id = message.chat.id
    name = message.chat.title
    uname = message.chat.username
    h_id = f"#ID{(-1*chat_id)}"
    if not await present_chat(chat_id):
        await client.send_message(LOG_CHANNEL, text=NEW_CHAT_LOG_TEXT.format(name, uname, chat_id, h_id))
        try:
            await add_chat(chat_id)
        except:
            pass
    for member in message.new_chat_members:
        if member.id == botid:
            await asyncio.sleep(15)
            video = random.choice(START_VIDEO)
            await message.reply_video(video, caption=NEW_GROUP_TEXT.format(name), reply_markup=OTHER_GROUP_BUTTONS)









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
