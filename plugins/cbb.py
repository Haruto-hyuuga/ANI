from pyrogram import filters
from bot import Bot
import asyncio
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from database.inline import*
from database.user_stats import update_RQ_SUB, update_RQ_DUB, update_SC, update_Anid
from config import START_MSG, ABOUT_TEXT, REQUEST_TEXT, ALL_CHANNEL_TEXT, REQUEST_GC, CREDIT_TEXT, REQ_TOPIC_ID, ERR_TOPIC_ID
from config import SUB_CHANNEL, DUB_CHANNEL, Sub_C_url, Dub_C_url, CHANNEL_ID, ADMINS
from req import channel_post_anime_info, download_anime_buttons_db, search_user_id, get_full_anime_info
from database.req_Db import add_SUB_request, add_DUB_request



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
    elif data.startswith("REQUEST_SA_"):
        QDS = query.data.split("_")[-1]
        anime_id = int(QDS)
        UID = query.from_user.id
        try: 
            message = query.message
            picc = message.photo.file_id
            Caption = message.caption if message.caption else ""
            await message.edit_text(
                text=f"{Caption}\n\n📬<b>REQUEST REGISTERED ✅</n>"
            )
            LOL = await client.send_photo(chat_id=REQUEST_GC, photo=picc, caption=Caption, reply_to_message_id=REQ_TOPIC_ID)
            await client.send_message(chat_id=REQUEST_GC, text=f"👤{query.from_user.mention} \n<code>{UID}</code>\n\n⚠️<code>/anime {anime_id}</code> FOR SUB CHANNEL", reply_to_message_id=LOL.id)
           
            await add_SUB_request(anime_id)
            await update_RQ_SUB(UID)
        except Exception as e:
            await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️Request Button query Error\n SUB anime button\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    elif data.startswith("REQUEST_DA_"):
        QDS = query.data.split("_")[-1]
        anime_id = int(QDS)
        UID = query.from_user.id
        try:
            message = query.message
            picc = message.photo.file_id
            Caption = message.caption if message.caption else ""
            await message.edit_text(
                text=f"{Caption}\n\n📬<b>REQUEST REGISTERED ✅</n>"
            )
            LOL = await client.send_photo(chat_id=REQUEST_GC, photo=picc, caption=Caption, reply_to_message_id=REQ_TOPIC_ID)
            await client.send_message(chat_id=REQUEST_GC, text=f"👤{query.from_user.mention} \n<code>{UID}</code>\n\n⚠️<code>/anime {anime_id}</code> FOR DUB CHANNEL", reply_to_message_id=LOL.id)

            await add_DUB_request(anime_id)
            await update_RQ_DUB(UID)
        except Exception as e:
            await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️Request Button query Error\n DUB anime button\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    elif data == "anime_download_popup":
        await query.answer("TO DOWNLOAD THE ANIME YOU WANT TAP ON (/download 12345) And SEND\n\nYOU CAN ALSO USE (/anime id)", show_alert=True)
    elif data == "anime_notfound_popup":
        await query.answer("IF ANIME IS NOT IN LIST, TRY SEARCHING MORE ACCURATE TITLE 🔎.\nOR USE COMMAND /list or /fullsearch", show_alert=True)
    elif data == "GroupAnimeInfo":
        await query.answer("START BOT IN PRIVATE FOR DETAILED ANIME INFO AND DOWNLOAD LINKS 💕", show_alert=True)
    elif data == "emoji_info_popup":
        await query.answer("Emoji Info:\n🖥️: Finished Series\n🆕: Currently Airing\n🔜: Not Yet Released\n❌: Cancelled\n🛑: Hiatus\n🕊️: Upcoming", show_alert=True)
    elif data == "Request_Pending_popup":
        await query.answer("REQUEST FOR THIS ANIME IS ALREADY BEEN SENT BY OTHER USERS\n we'll add it as soon as possible 🕊️", show_alert=True)
    

    elif data == "gcAresultclose":
        await query.message.edit_text(text=f"𝑪𝒍𝒐𝒔𝒆𝒅 𝑩𝒚 {query.from_user.mention}")
    elif data == "DB_C_POST":
        if query.from_user.id in ADMINS:
            M = query.message
            P = M.photo.file_id
            C = M.caption if M.caption else "Unexpected Error ⚠️"
            await client.send_photo(CHANNEL_ID, photo=P, caption=C)
            await query.message.delete()
            await asyncio.sleep(5)
            await M.reply_text(text="<b>BANNER POSTED ✅</b>", reply_markup=BATCH_DBC_B)
        else: 
            await query.answer("You're Not Allowed Baka!", show_alert=True)
        
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

    elif data.startswith("SUBconfirmpostS_"):
        if query.from_user.id in ADMINS:
            anime_id = query.data.split("_")[-1]
            M = query.message.reply_to_message
            P = await M.copy(SUB_CHANNEL)
            await M.edit_text("<b>✅Sent:</b> @ANIME_DOWNLOADS_SUB")
            await query.message.edit_text(f"<i>Reply To Link Below by Command:</i>\n\n👉🏻  <code>/addsub {anime_id}</code>")    

            await client.send_message(SUB_CHANNEL, text="➖➖➖➖🖥️➖➖➖➖")
            await query.message.reply_text(f"{Sub_C_url}/{P.id}", disable_web_page_preview=True)
            await client.send_message(query.message.chat.id, text="➖➖➖➖👆🏻➖➖➖➖")
        else:
            await query.answer("You're Not Allowed Baka!", show_alert=True)

    elif data.startswith("DUBconfirmpostD_"):
        if query.from_user.id in ADMINS:
            anime_id = query.data.split("_")[-1]
            M = query.message.reply_to_message
            P = await M.copy(DUB_CHANNEL)
            await M.edit_text("<b>✅Sent:</b> @ANIME_DOWNLOADS_DUB")
            await query.message.edit_text(f"<i>Reply To Link Below By Command:</i>\n\n👉🏻  <code>/adddub {anime_id}</code>")

            await client.send_message(DUB_CHANNEL, text="➖➖➖➖🖥️➖➖➖➖")
            await query.message.reply_text(f"{Dub_C_url}/{P.id}", disable_web_page_preview=True)
            await client.send_message(query.message.chat.id, text="➖➖➖➖👆🏻➖➖➖➖")
        else:
            await query.answer("You're Not Allowed Baka!", show_alert=True)

    elif data.startswith("Anime_DL_"):
        B_DATA = query.data.split("_")[-1]
        u_id, a_id = B_DATA.split(":")
        user_id = int(u_id)
        anime_id = int(a_id)
        if user_id == query.from_user.id:
            E_title, J_title, MSG_img, Format, episodes, status, average_score, Igenres, studio, duration, season = await channel_post_anime_info(anime_id)
            message_text = f"""
🇬🇧: <b><u>{E_title}</u></b>
🇯🇵: <b><u>{J_title}</u></b>
━━━━━━━━━━━━━━━━━━━━━━━━━
ᴇᴘɪꜱᴏᴅᴇꜱ: <b>{episodes}</b>
ᴅᴜʀᴀᴛɪᴏɴ: <b>{duration}</b>
ᴛʏᴘᴇ: <b>{Format}</b>
ꜱᴛᴀᴛᴜꜱ: <b>{status}</b>
ɢᴇɴʀᴇꜱ: <i>{Igenres}</i>
"""
            UID = user_id
            new_message_text, buttons = await download_anime_buttons_db(anime_id, message_text, client, UID)
            if query.message.reply_to_message:
                try:
                    await query.message.delete()
                    await query.message.reply_to_message.reply_photo(photo=MSG_img, caption=new_message_text, reply_markup=InlineKeyboardMarkup(buttons))
                    await update_SC(UID)
                except Exception as e:
                    await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️ANIME Button query Error\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
            if not query.message.reply_to_message:
                try:
                    await query.message.delete()
                    await query.message.reply_photo(photo=MSG_img, caption=new_message_text, reply_markup=InlineKeyboardMarkup(buttons))
                    await update_SC(UID)
                except Exception as e:
                    await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️ANIME Button query Error\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
   
        else:
            await query.answer("The Person Who Searched This Anime Can Use These Buttons, Search Your Own: /anime", show_alert=True)

    elif data.startswith("Anime_FL_I_"):
        B_DATA = query.data.split("_")[-1]
        u_id, a_id = B_DATA.split(":")
        user_id = int(u_id)
        anime_id = int(a_id)
        if user_id == query.from_user.id:
            F_BOOL, first_message, message_text, cover_url, banner_url, title_img, trailer_url, site_url = await get_full_anime_info(anime_id)
            if F_BOOL == True:
                try:
                    F_MSG1 = await query.message.reply_photo(banner_url, caption=first_message)
                except Exception as e:
                    F_MSG1 = await query.message.reply_photo(cover_url, caption=first_message)
                    pass
                S_CB_DATA = f"{UID}:{anime_id}"
                YtRESULT_B = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🖥️ Anime Site", url=site_url),
                            InlineKeyboardButton("Watch Trailer 🖥️", url=trailer_url)
                        ],
                        [
                            InlineKeyboardButton("𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗", callback_data=f"Anime_DL_{S_CB_DATA}"),
                            InlineKeyboardButton("𝗖𝗟𝗢𝗦𝗘", callback_data="close"),             
                        ]
                   ]
                )
                try:
                    await query.F_MSG1.reply_photo(title_img, caption=message_text, reply_markup=YtRESULT_B)
                except Exception as e:
                    await message.reply_text("An Error Occurred, Try Agin\nIf Problem persist Contact me 🛂", reply_markup=ERROR_BUTTON)
                    await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Full anime info CMD-PVT MSG-2 Error\ntitle image and infos\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
            else:
                try:
                    await message.reply_photo(title_img, caption=f"{first_message}\n{message_text}", reply_markup=ERROR_BUTTON)
                except Exception as e:
                    await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Full anime info CMD-PVT MSG-2 Error\ntitle image and infos\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
  
        else:
            await query.answer("The Person Who Searched This Anime Can Use These Buttons, Search Your Own: /anime", show_alert=True)


    elif data.startswith("FUclose_"):
        UID = query.data.split("_")[-1]
        CLICK = query.from_user.id
        user_id = int(UID)
        if CLICK not in ADMINS:
            if not CLICK == user_id:
                await query.answer("You're Not Allowed Baka!", show_alert=True)
                return
            
        await query.message.delete()
        try: 
            await query.message.reply_to_message.delete()
        except:
            pass
            
    elif data.startswith("Ani_User_"):
        Ani_UID = query.data.split("_")[-1]
        user_id = query.from_user.id
        try:
            await update_Anid(user_id, Ani_UID)
            await query.message.delete()
            message_photo, Ani_C, Ani_MW, Ani_EW, Ani_MS = await search_user_id(Ani_UID)
            await query.message.reply_photo(
                photo=message_photo,
                caption=f"SUCCESSFULLY SET ANILIST ACCOUNT ✅\nAnime Watched: {Ani_C}\nEpisodes Watched: {Ani_EW}\nScore: {Ani_MS}"
            )
        except Exception as e:
            await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️Request Button query Error\n DUB anime button\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)























