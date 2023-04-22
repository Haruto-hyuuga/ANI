from pyrogram import filters, __version__
from bot import Bot
import asyncio
from pyrogram.types import Message, CallbackQuery
from database.inline import*
from config import START_MSG, ABOUT_TEXT, REQUEST_TEXT, ALL_CHANNEL_TEXT, REQUEST_GC, CREDIT_TEXT, REQ_TOPIC_ID, ERR_TOPIC_ID
from config import SUB_CHANNEL, DUB_CHANNEL, Sub_C_url, Dub_C_url


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
        try: 
            message = query.message
            picc = message.photo.file_id
            Caption = message.caption if message.caption else ""
            await message.edit_text(
                text=f"{Caption}\n\n📬<b>REQUEST REGISTERED FOR THIS ANIME FOR SUB CHANNEL✅</n>"
            )
            LOL = await client.send_photo(chat_id=REQUEST_GC, photo=picc, caption=Caption, reply_to_message_id=REQ_TOPIC_ID)
            await client.send_message(chat_id=REQUEST_GC, text=f"👤{query.from_user.mention} \n<code>{query.from_user.id}</code>\n\n⚠️ REQUESTED ANIME FOR SUB CHANNEL", reply_to_message_id=LOL.id)
        except Exception as e:
            await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️Request Button query Error\n SUB anime button\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    elif data == "REQUEST_DA":
        try:
            message = query.message
            picc = message.photo.file_id
            Caption = message.caption if message.caption else ""
            await message.edit_text(
                text=f"{Caption}\n\n📬<b>REQUEST REGISTERED FOR THIS ANIME FOR DUB CHANNEL✅</n>"
            )
            LOL = await client.send_photo(chat_id=REQUEST_GC, photo=picc, caption=Caption, reply_to_message_id=REQ_TOPIC_ID)
            await client.send_message(chat_id=REQUEST_GC, text=f"👤{query.from_user.mention} \n<code>{query.from_user.id}</code>\n\n⚠️ REQUESTED ANIME FOR DUB CHANNEL", reply_to_message_id=LOL.id)
        except Exception as e:
            await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️Request Button query Error\n DUB anime button\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    elif data == "anime_download_popup":
        await query.answer("TO DOWNLOAD THE ANIME YOU WANT TAP ON (/download 12345) And SEND, YOU'LL GET DOWNLOAD LINK or YOU CAN USE (/anime id) TOO", show_alert=True)
    elif data == "anime_notfound_popup":
        await query.answer("IF ANIME YOUR LOOKING FOR IS NOT IN LIST, TRY SEARCHING MORE ACCURATE TITLE 🔎", show_alert=True)
    elif data == "GroupAnimeInfo":
        await query.answer("START BOT IN PRIVATE FOR DETAILED ANIME INFO AND DOWNLOAD LINKS 💕", show_alert=True)
    elif data == "gcAresultclose":
        await query.message.edit_text(text=f"𝑪𝒍𝒐𝒔𝒆𝒅 𝑩𝒚 {query.from_user.mention}")

    elif data.startswith("SUBconfirmpostS_"):
        anime_id = query.data.split("_")[-1]
        try:
            message = query.message
            picc = message.photo.file_id
            Caption = message.caption
            FUCK = client.send_photo(chat_id=SUB_CHANNEL, photo=picc, caption=Caption)
            await message.edit_text("<b>POSTED SUCCESSFULLY ON SUB CHANNEL ✅</b>")
            await client.send_message(chat_id=message.chat.id, text=f"<i>REPLY TO BELOW LINK BY THIS COMMAND:</i>\n\n👉🏻  <code>/addsub {anime_id}</code>")
            Post_id = FUCK.id
            await client.send_message(chat_id=message.chat.id, text=f"{Sub_C_url}/{Post_id}")
            await asyncio.sleep(10)
            await client.send_message(chat_id=message.chat.id, text="Don't Forget To Edit Post's Inline Buttons")
        except Exception as e:
            await client.send_message(chat_id=message.chat.id, text=e)
            
    elif data.startswith("DUBconfirmpostD_"):
        anime_id = query.data.split("_")[-1]
        try:
            message = query.message
            picc = message.photo.file_id
            Caption = message.caption
            FUCK = client.send_photo(chat_id=DUB_CHANNEL, photo=picc, caption=Caption)
            await message.edit_text("<b>POSTED SUCCESSFULLY ON DUB CHANNEL ✅</b>")
            await client.send_message(chat_id=message.chat.id, text=f"<i>REPLY TO BELOW LINK BY THIS COMMAND:</i>\n\n👉🏻  <code>/adddub {anime_id}</code>")
            Post_id = FUCK.id
            await client.send_message(chat_id=message.chat.id, text=f"{Dub_C_url}/{Post_id}")
            await asyncio.sleep(10)
            await client.send_message(chat_id=message.chat.id, text="Don't Forget To Edit Post's Inline Buttons")
        except Exception as e:
            await client.send_message(chat_id=message.chat.id, text=e)
            
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass


