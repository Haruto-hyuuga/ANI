from bot import Bot
from pyrogram import Client, filters, __version__
from pyrogram.types import Message
from config import ADMINS, Gif_Random, REQUEST_GC, ERR_TOPIC_ID, USER_LOG_CHANNEL
from database.inline import AllFSCB


GC_LOG_TXT = """
🔴 #New_GROUP
Title:

🆔: <code>{}</code>  #id{}
🔗: @{}
🚷 LEFT GROUP ✅
"""


@Bot.on_message(filters.group & filters.new_chat_members)
async def leave_group(client, message: Message):
    
    added_by = [user.id for user in message.new_chat_members if user.is_bot]
    TGC_id = message.chat.id
    TGC_Lk = message.chat.username
    TGC_TT = message.chat.title
    FINAL_GIF = await Gif_Random()

    if ADMINS not in added_by:
        ALLCC_MSG = "<b>FEEL FREE TO USE ME IN PRIVATE CHAT</b>\n𝙃𝙚𝙧𝙚'𝙨 𝙏𝙝𝙚 𝙇𝙞𝙨𝙩 𝙊𝙛 𝘼𝙡𝙡 𝘾𝙝𝙖𝙣𝙣𝙚𝙡𝙨:"
        try:
            await client.send_animation(chat_id=TGC_id, animation=FINAL_GIF, caption=ALLCC_MSG, reply_markup=AllFSCB)    
            await client.send_message(chat_id=USER_LOG_CHANNEL, text=GC_LOG_TXT.format(TGC_TT, TGC_id, TGC_id, TGC_Lk))
            await client.leave_chat(TGC_id)
        except Exception as e:
            await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️AUTO LEAVE UNAUTH GROUP\nwhile Leaving Group\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    else:
        THANKS_MSG = "<b>Thanks For Having Me In:</b> {}"
        await client.send_animation(chat_id=TGC_id, animation=FINAL_GIF, caption=THANKS_MSG.format(TGC_TT))
        pass










