from pyrogram import __version__
from bot import Bot
from pyrogram.types import Message, CallbackQuery
from database.inline import*
from config import START_MSG, ABOUT_TEXT, REQUEST_TEXT, ALL_CHANNEL_TEXT, CREATOR_GC

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "BACK_HOME":
        await query.message.edit_text(
            text = START_MSG.format(query.from_user.mention),
            reply_markup = START_B
        )
    elif data == "About_Bot":
        await query.message.edit_text(
            text = ABOUT_TEXT,
            reply_markup = ABOUT_BUTTONS
        )
    elif data == "DL_Channels":
        await query.message.edit_text(
            text = ALL_CHANNEL_TEXT,
            reply_markup = CHANNELS_BUTTON
        )
    elif data == "A_requests":
        await query.message.edit_text(
            text = REQUEST_TEXT,
            reply_markup = REQUEST_BUTTONS
        )
    elif data == "REQUEST_SA":
        await query.message.edit_text(
            text = f"{query.message.photo.caption}\n\n📬<b>REQUEST REGISTERED FOR THIS ANIME ✅</n>"
        )
        await Bot.copy_message(CREATOR_GC, query.message.chat.id, query.message.id)
        await Bot.send_message(CREATOR_GC, text=f"👤{query.message.from_user.id} \n<code>{query.message.from_user.id}</code>\n\n⚠️ REQUESTED ANIME FOR SUB CHANNEL")
    elif data == "REQUEST_DA":
        await query.message.edit_text(
            text = f"{query.message..photo.caption}\n\n📬<b>REQUEST REGISTERED FOR THIS ANIME ✅</n>"
        )
        await Bot.copy_message(CREATOR_GC, query.message.chat.id, query.message.id)
        await Bot.send_message(CREATOR_GC, text=f"👤{query.message.from_user.id} \n<code>{query.message.from_user.id}</code>\n\n⚠️ REQUESTED ANIME FOR DUB CHANNEL")
    elif data == "anime_download_popup":
        await query.answer("To Download The Anime You Want Tap On The (/download 12345) And Send or You Can Use /find Command Followed By Anime Id From Anilist", show_alert=True)
    elif data == "anime_notfound_popup":
        await query.answer("If The Anime You're Looking For Is Not In List, Try Searching More Accurate Title or Get Anime Id From Anilist", show_alert=True)
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
