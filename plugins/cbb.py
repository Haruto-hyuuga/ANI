from pyrogram import filters, __version__
from bot import Bot
from pyrogram.types import Message, CallbackQuery
from database.inline import*
from config import START_MSG, ABOUT_TEXT, REQUEST_TEXT, ALL_CHANNEL_TEXT, REQUEST_GC, CREDIT_TEXT, REQ_TOPIC_ID

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
        LOL = await client.send_photo(chat_id=REQUEST_GC, photo=picc, caption=Caption, reply_to_message_id=REQ_TOPIC_ID)
        await client.send_message(chat_id=REQUEST_GC, text=f"👤{query.from_user.mention} \n<code>{query.from_user.id}</code>\n\n⚠️ REQUESTED ANIME FOR SUB CHANNEL", reply_to_message_id=LOL.id)

    elif data == "REQUEST_DA":
        message = query.message
        picc = message.photo.file_id
        Caption = message.caption if message.caption else ""
        await message.edit_text(
            text=f"{Caption}\n\n📬<b>REQUEST REGISTERED FOR THIS ANIME FOR DUB CHANNEL✅</n>"
        )
        LOL = await client.send_photo(chat_id=REQUEST_GC, photo=picc, caption=Caption, reply_to_message_id=REQ_TOPIC_ID)
        await client.send_message(chat_id=REQUEST_GC, text=f"👤{query.from_user.mention} \n<code>{query.from_user.id}</code>\n\n⚠️ REQUESTED ANIME FOR DUB CHANNEL", reply_to_message_id=LOL.id)

    elif data == "anime_download_popup":
        await query.answer("TO DOWNLOAD THE ANIME YOU WANT TAP ON (/download 12345) And SEND, YOU'LL GET DOWNLOAD LINK or YOU CAN USE (/anime id) TOO", show_alert=True)
    elif data == "anime_notfound_popup":
        await query.answer("IF ANIME YOUR LOOKING FOR IS NOT IN LIST, TRY SEARCHING MORE ACCURATE TITLE 🔎", show_alert=True)
    elif data == "GroupAnimeInfo":
        await query.answer("START BOT IN PRIVATE FOR DETAILED ANIME INFO AND DOWNLOAD LINKS 💕", show_alert=True)
    elif data == "gcAresultclose":
        await query.message.edit_text(text=f"𝑪𝒍𝒐𝒔𝒆𝒅 𝑩𝒚 {query.from_user.mention}")
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass


