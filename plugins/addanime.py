from bot import Bot
from pyrogram import Client, filters
from pyrogram.types import Message
from config import ADMINS, Sub_C_url, Dub_C_url, REQUEST_GC, BOTUSERNAME, REQ_TOPIC_ID, ERR_TOPIC_ID, ANI_LOG_CHANNEL
from helper_func import sub_PUB_Sc, sub_PUB_Dc, sub_BOT_c, sub_GC
from database.anime_db import present_sub_anime, get_sub_anime, add_sub_anime, del_sub_anime, full_sub_Animebase
from database.anime_db import present_dub_anime, get_dub_anime, add_dub_anime, del_dub_anime, full_dub_Animebase
from database.database import full_userbase
from database.inline import Ani_log_inline_f
from plugins.anime import get_Log_anime_i

ANI_SUB_LOG_TXT = """
🏷<b>TITLE:</b> {}
 
Anime{}    <code>{}</code>
<b>episodes</b>: {}
〰️〰️〰️〰️〰️〰️〰️〰️〰️
🟥 <b>SUB</b>: {}
〰️〰️〰️〰️〰️〰️〰️〰️〰️
👤<b>By:</b> {} 🆔: <code>{}</code>
〰️〰️〰️〰️〰️〰️〰️〰️〰️
"""

ANI_DUB_LOG_TXT = """
🏷<b>TITLE:</b> {}
 
Anime{}    <code>{}</code>
<b>episodes</b>: {}
〰️〰️〰️〰️〰️〰️〰️〰️〰️
🟩 <b>DUB</b>: {}
〰️〰️〰️〰️〰️〰️〰️〰️〰️
👤<b>By:</b> {} 🆔: <code>{}</code>
〰️〰️〰️〰️〰️〰️〰️〰️〰️
"""



@Bot.on_message(filters.command("adddub") & filters.user(ADMINS))
async def adddub(client, message):
    Umention = message.from_user.mention
    UID = message.from_user.id
    if message.reply_to_message:
        link = message.reply_to_message.text
        if len(message.command) != 1:
            text = message.text.split(None, 1)[1]
            anime_id = int(text) 
            if not await present_dub_anime(anime_id):
                A_PIC, A_Title, Episodes = await get_Log_anime_i(anime_id)
                ANI_LOG_BUT = await Ani_log_inline_f(UID, link)
                try:
                    await add_dub_anime(anime_id, link)
                    await client.send_photo(
                        chat_id=ANI_LOG_CHANNEL,
                        photo=A_PIC,
                        caption=ANI_SUB_LOG_TXT.format(A_Title, anime_id, anime_id, Episodes, link, Umention, UID),
                        reply_markup=ANI_LOG_BUT
                    )
                    await message.reply_text(f"<b>ADDED!</b>\n\nID: <b>{anime_id}</b>\nLINK: {link}")
                except Exception as e:
                    await message.reply_text(f"An Error Occured//-\n\n{e}")
                    await client.send_message(chat_id=REQUEST_GC, text=f"⚠️ Add-DUB CMD Error:\n\n {e}", reply_to_message_id=ERR_TOPIC_ID)
            else:
                dblink = await get_dub_anime(anime_id)
                await message.reply_text(f"<b>THIS ANIME ALREDY EXIST</b>\n\nID: <b>{anime_id}</b>\n<b>POST LINK:</b> {dblink}")
        else:
            await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /anime or /search")
    else:
        await message.reply_text(f"Bish Reply To Post Link From Channel:\n {Dub_C_url}")
        

@Bot.on_message(filters.command("deldub") & filters.user(ADMINS))
async def deldub(client, message):
    if len(message.command) != 1:
        text = message.text.split(None, 1)[1]
        anime_id = int(text) 
        if await present_dub_anime(anime_id):
            try:
                dblink = await get_dub_anime(anime_id)
                await del_dub_anime(anime_id)
                await message.reply_text(f"<b>DELETED!</b>\n\nID: <b>{anime_id}</b>\n<b>POST LINK:</b> {dblink}")
            except Exception as e:
                await message.reply_text(f"An Error Occured//-\n\n{e}")
        else:
            await message.reply_text(f"No Such Anime Was Inserted In DataBase With ID: {anime_id}")
    else:
        await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /anime or /search")

@Bot.on_message(filters.command("addsub") & filters.user(ADMINS))
async def addsub(client, message):
    Umention = message.from_user.mention
    UID = message.from_user.id
    if message.reply_to_message:
        link = message.reply_to_message.text
        if len(message.command) != 1:
            text = message.text.split(None, 1)[1]
            anime_id = int(text) 
            if not await present_sub_anime(anime_id):
                A_PIC, A_Title, Episodes = await get_Log_anime_i(anime_id)
                ANI_LOG_BUT = await Ani_log_inline_f(UID, link)
                try:
                    await add_sub_anime(anime_id, link)
                    await client.send_photo(
                        chat_id=ANI_LOG_CHANNEL,
                        photo=A_PIC,
                        caption=ANI_DUB_LOG_TXT.format(A_Title, anime_id, anime_id, Episodes, link, Umention, UID),
                        reply_markup=ANI_LOG_BUT
                    )
                    await message.reply_text(f"<b>ADDED!</b>\n\nID: <b>{anime_id}</b>\nLINK: {link}")
                except Exception as e:
                    await message.reply_text(f"An Error Occured//-\n\n{e}")
                    await client.send_message(chat_id=REQUEST_GC, text=f"⚠️ Add-SUB CMD Error:\n\n {e}", reply_to_message_id=ERR_TOPIC_ID)
            else:
                dblink = await get_sub_anime(anime_id)
                await message.reply_text(f"<b>THIS ANIME ALREDY EXIST</b>\n\nID: <b>{anime_id}</b>\n<b>POST LINK:</b> {dblink}")
        else:
            await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /anime or /search")
    else:
        await message.reply_text(f"Bish Reply To Post Link From Channel:\n {Sub_C_url}")
        
    
@Bot.on_message(filters.command("delsub") & filters.user(ADMINS))
async def delsub(client, message):
    if len(message.command) != 1:
        text = message.text.split(None, 1)[1]
        anime_id = int(text) 
        if await present_sub_anime(anime_id):
            try:
                dblink = await get_sub_anime(anime_id)
                await del_sub_anime(anime_id)
                await message.reply_text(f"<b>DELETED!</b>\n\nID: <b>{anime_id}</b>\n<b>POST LINK:</b> {dblink}")
            except Exception as e:
                await message.reply_text(f"An Error Occured//-\n\n{e}")
        else:
            await message.reply_text(f"No Such Anime Was Inserted In DataBase With ID: {anime_id}")
    else:
        await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /anime or /search")

REQPFX = ["/", "#"]
@Bot.on_message(filters.command("request", prefixes=REQPFX) & filters.private & sub_PUB_Dc & sub_PUB_Sc & sub_GC & sub_BOT_c)
async def arequest(client, message):
    reply = message.reply_to_message
    if reply:
        if len(message.command) != 1:
            try:
                text = message.text.split(None, 1)[1]
                pic = reply.photo.file_id
                Text = reply.caption
                LOL = await client.send_photo(chat_id=REQUEST_GC, photo=pic, caption=Text, reply_to_message_id=REQ_TOPIC_ID)
                await client.send_message(chat_id=REQUEST_GC, text=f"👤{message.from_user.mention} \n🆔:<code>{message.from_user.id}</code>\n💬: {text}\n⚠️ REQUESTED ANIME", reply_to_message_id=LOL.id)
                await message.reply_text("<b>REQUEST REGISTERED</b>\nThanks💕 We'll Add It To Channel Soon.")
            except Exception as e:
                await message.reply_text("Something Went Wrong👀\nTry Again And Reply Only to Bot Message\nSearch for anime /download Then Reply")
                await client.send_message(chat_id=REQUEST_GC, text=f"⚠️ Request CMD Error:\n\n {e}", reply_to_message_id=ERR_TOPIC_ID)
        else:
            await message.reply_text("Mention Category after command, you want it in Dub Or Sub\n\nformat: /request DUB")
    else:
        await message.reply_text("Bish Reply To Searched Anime Using Command: /anime")
        


NON_A_S_T = """
╔══════════════════════╗
╠╼ 𝘿𝙖𝙩𝙖𝙗𝙖𝙨𝙚 𝙎𝙩𝙖𝙩𝙨  📂
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
╠<b>ᴛᴏᴛᴀʟ ꜱᴜʙ ᴀɴɪᴍᴇ:</b> {}
╠<b>ᴛᴏᴛᴀʟ ᴅᴜʙ ᴀɴɪᴍᴇ:</b> {} 
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
╠╼ @{} 💕
╚══════════════════════╝
"""

ADMIN_S_T = """
╔══════════════════════╗
╠╼ 𝘿𝙖𝙩𝙖𝙗𝙖𝙨𝙚 𝙎𝙩𝙖𝙩𝙨  📂
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
╠<b>ᴜꜱᴇʀꜱ:</b> {}
╠<b>ᴛᴏᴛᴀʟ ꜱᴜʙ ᴀɴɪᴍᴇ:</b> {}
╠<b>ᴛᴏᴛᴀʟ ᴅᴜʙ ᴀɴɪᴍᴇ:</b> {} 
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
╠╼ @{} 💕
╚══════════════════════╝
"""


@Bot.on_message(filters.command('stats') & sub_PUB_Dc & sub_PUB_Sc & sub_GC & sub_BOT_c)
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text="⌛")
    UID = message.from_user.id
    suba = await full_sub_Animebase()
    SA = len(suba)
    duba = await full_dub_Animebase()
    DA = len(duba)
    if UID in ADMINS:
        user = await full_userbase()
        US = len(user)
        await msg.edit(ADMIN_S_T.format(US, SA, DA, BOTUSERNAME))
    else:
        await msg.edit(ADMIN_S_T.format(SA, DA, BOTUSERNAME))



