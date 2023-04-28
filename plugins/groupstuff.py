from bot import Bot
from pyrogram import Client, filters
from pyrogram.types import Message

import asyncio
from config import ADMINS
from database.database import present_chat, add_chat, full_chatbase, del_chat
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, ChatWriteForbidden, BotKicked, UserNotParticipant


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
