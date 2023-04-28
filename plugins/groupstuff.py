

from pyrogram.errors.exceptions import FloodWait, UserIsBlocked, InputUserDeactivated, ChatWriteForbidden, BotKicked, UserNotParticipant

@app.on_message(get_cmd('gcbroadcast') & filters.user(DEV))
async def gcbroadcastmsg(client: app, message: Message):
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
        
        status = f"""**Broadcast Completed**📡
👥__Total Groups:__ {total}
✅__Successful:__ {successful}
⚠️__Unsuccessful:__ {unsuccessful}
💀__Deleted:__ {deleted}  || 🚫__Error:__ {blocked}
"""
        
        return await pls_wait.edit(status)

    else:
        await app.send_sticker(message.chat.id, sticker=REPY_ERROR_STICKER)
        await message.reply(REPLY_ERROR)
