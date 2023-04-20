from pyrogram import __version__
from bot import Bot
from pyrogram.types import Message, CallbackQuery
from database.inline import*
from config import START_MSG, ABOUT_TEXT, REQUEST_TEXT, ALL_CHANNEL_TEXT, CREATOR_GC, CREDIT_TEXT

@Bot.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
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
    elif data == "Credits_a":
        await query.message.edit_text(
            text = CREDIT_TEXT,
            reply_markup = CREDIT_B
        )
    elif data == "REQUEST_SA":
        message = query.message
        picc = message.photo.file_id
        Caption = message.caption if message.caption else ""
        await message.edit_text(
            text=f"{Caption}\n\n📬<b>REQUEST REGISTERED FOR THIS ANIME FOR SUB CHANNEL✅</n>"
        )
        await client.send_photo(chat_id=CREATOR_GC, photo=picc, caption=Caption)
        await client.send_message(chat_id=CREATOR_GC, text=f"👤{message.from_user.mention} \n<code>{message.from_user.id}</code>\n\n⚠️ REQUESTED ANIME FOR SUB CHANNEL")

    elif data == "REQUEST_DA":
        message = query.message
        picc = message.photo.file_id
        Caption = message.caption if message.caption else ""
        await message.edit_text(
            text=f"{Caption}\n\n📬<b>REQUEST REGISTERED FOR THIS ANIME FOR DUB CHANNEL✅</n>"
        )
        await client.send_photo(chat_id=CREATOR_GC, photo=picc, caption=Caption)
        await client.send_message(chat_id=CREATOR_GC, text=f"👤{message.from_user.mention} \n<code>{message.from_user.id}</code>\n\n⚠️ REQUESTED ANIME FOR DUB CHANNEL")

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


@Bot.on_callback_query(filters.regex("gcAresultclose"))
async def resultAclose(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(
                "You're not allowed to close this.", show_alert=True
            )
        except:
            return

    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        return


