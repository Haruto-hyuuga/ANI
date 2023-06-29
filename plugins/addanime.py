from bot import Bot
from pyrogram import Client, filters
from req import get_cmd
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS, Sub_C_url, Dub_C_url, REQUEST_GC, BOTUSERNAME, REQ_TOPIC_ID, ERR_TOPIC_ID, ANI_LOG_CHANNEL, ANI_LOG_URL
from helper_func import sub_PUB_Sc, sub_PUB_Dc, sub_BOT_c, sub_GC
from database.anime_db import present_sub_anime, get_sub_anime, add_sub_anime, del_sub_anime, full_sub_Animebase
from database.anime_db import present_dub_anime, get_dub_anime, add_dub_anime, del_dub_anime, full_dub_Animebase
from database.database import full_userbase
from database.user_stats import get_user_stats
from database.req_Db import full_requestDB_DUB, full_requestDB_SUB
from database.inline import Ani_log_inline_f, user_close
from pyrogram.errors import BadRequest
from req import get_Log_anime_i, channel_post_anime_info, only_banner_image, search_user_id
    


@Bot.on_message(get_cmd("banner") & filters.user(ADMINS))
async def first_ep_banner(client, message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /find or /search")
        return
    try:
        anime_id = int(args[1])
    except (IndexError, ValueError):
        await message.reply_text(f"Index Error!   *_*\n Did you fuck up with number after command??")
        return
    banner_pic, cover_pic, msg_caption = await only_banner_image(anime_id)
    try:
        await message.reply_photo(photo=banner_pic, caption=msg_caption) 
    except Exception as e:
        await message.reply_text(f"ERROR ⚠️:\n⌛ Sending Other Image....\n\n{e}")
        await message.reply_photo(photo=cover_pic, caption=msg_caption)


@Bot.on_message(get_cmd("deldub") & filters.user(ADMINS))
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


                    
@Bot.on_message(get_cmd("delsub") & filters.user(ADMINS))
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



@Bot.on_message(get_cmd("request") & filters.private & sub_PUB_Dc & sub_PUB_Sc & sub_GC & sub_BOT_c)
async def arequest(client, message):
    reply = message.reply_to_message
    if len(message.command) != 1:
        if reply:
            try:
                text = message.text.split(None, 1)[1]
                
                LOL = await reply.copy(REQUEST_GC, reply_to_message_id=REQ_TOPIC_ID)
                await client.send_message(chat_id=REQUEST_GC, text=f"👤{message.from_user.mention} ⚠️ #REQUESTED_ANIME \n🆔:<code>{message.from_user.id}</code>\n💬: {text}", reply_to_message_id=LOL.id)
                await message.reply_text("<b>REQUEST REGISTERED</b>\nThank-You Very Much💕")
            except Exception as e:
                await message.reply_text("Something Went Wrong👀\nReport This To @MaidRobot")
                await client.send_message(chat_id=REQUEST_GC, text=f"⚠️ Request CMD-REPLY Error:\n\n {e}", reply_to_message_id=ERR_TOPIC_ID)
        else:
            try:
                text = message.text.split(None, 1)[1]
                await client.send_message(chat_id=REQUEST_GC, text=f"👤{message.from_user.mention} ⚠️ #REQUESTED_ANIME \n🆔:<code>{message.from_user.id}</code>\n\n💬: {text}", reply_to_message_id=REQ_TOPIC_ID)
                await message.reply_text("<b>REQUEST REGISTERED</b>\nThank-You Very Much💕")
            except Exception as e:
                await message.reply_text("Something Went Wrong👀\nReport This To @MaidRobot")
                await client.send_message(chat_id=REQUEST_GC, text=f"⚠️ Request Len-CMD-Txt Error:\n\n {e}", reply_to_message_id=ERR_TOPIC_ID)
    else:
        await message.reply_text("Baka! mention link of anime you want to request\n〰️〰️〰️〰️OR〰️〰️〰️〰️\nWrite SUB/BUB after command while replying to a searched anime message")
 

@Bot.on_message(get_cmd("report") & filters.private & sub_PUB_Dc & sub_PUB_Sc & sub_GC & sub_BOT_c)
async def pvtreportt(client, message):
    reply = message.reply_to_message
    if reply:
        if len(message.command) != 1:
            try:
                text = message.text.split(None, 1)[1]
                
                LOL = await reply.copy(REQUEST_GC, reply_to_message_id=ERR_TOPIC_ID)
                await client.send_message(chat_id=REQUEST_GC, text=f"👤{message.from_user.mention} ⚠️ #REPORT \n🆔:<code>{message.from_user.id}</code>\n💬: {text}", reply_to_message_id=LOL.id)
                await message.reply_text("<b>REPORT SENT</b>\nThank-You Very Much💕")
            except Exception as e:
                await message.reply_text("Something Went Wrong👀\nReport This To @MaidRobot")
                await client.send_message(chat_id=REQUEST_GC, text=f"⚠️ Report CMD Error:\n\n {e}", reply_to_message_id=ERR_TOPIC_ID)
        else:
                await message.reply_text("Please Describe your issue regarding bot after command.\n\n/report Malfunction")
    if len(message.command) != 1 and not reply:
        text = message.text.split(None, 1)[1]
        await client.send_message(chat_id=REQUEST_GC, text=f"👤{message.from_user.mention} ⚠️ #REPORT \n🆔:<code>{message.from_user.id}</code>\n💬: {text}", reply_to_message_id=ERR_TOPIC_ID)
        await message.reply_text("<b>REPORT SENT</b>\nThank-You Very Much💕")
         
    if not len(message.command) != 1 and not reply:
        await message.reply_text("Baka! reply to error message or describe issue after command \nyou can mention reason while replying to a message too.")
 



NO_ANI_MEM = """
╔══════════════════════╗
╠╼ 👤 {}
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
╠<b>ᴀɴɪᴍᴇ ꜱᴇᴀʀᴄʜᴇᴅ:</b> {} 
╠<b>ᴀɴɪᴍᴇ ʀᴇ𝚀ᴜᴇꜱᴛᴇᴅ ꜱᴜʙ:</b> {} 
╠<b>ᴀɴɪᴍᴇ ʀᴇ𝚀ᴜᴇꜱᴛᴇᴅ ᴅᴜʙ:</b> {} 
╠<b>ᴀɴɪᴍᴇ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ:</b> {}
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ 
╠Anilist Account Not Linked
╚══════════════════════╝
"""

ANI_MEM = """
╔══════════════════════╗
╠╼ 👤 {}
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
╠><i> 𝘽𝙤𝙩 𝙎𝙩𝙖𝙩𝙨 💠</i>
╠<b>ᴀɴɪᴍᴇ ꜱᴇᴀʀᴄʜᴇᴅ:</b> {} 
╠<b>ᴀɴɪᴍᴇ ʀᴇ𝚀ᴜᴇꜱᴛᴇᴅ ꜱᴜʙ:</b> {} 
╠<b>ᴀɴɪᴍᴇ ʀᴇ𝚀ᴜᴇꜱᴛᴇᴅ ᴅᴜʙ:</b> {} 
╠<b>ᴀɴɪᴍᴇ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ:</b> {}
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ 
╠><i> 𝙐𝙨𝙚𝙧 𝘼𝙣𝙞𝙢𝙚 𝙎𝙩𝙖𝙩𝙨 🖥️</i>
╠<b>ᴀɴɪᴍᴇ ᴡᴀᴛᴄʜᴇᴅ:</b> {} 
╠<b>ᴇᴘɪꜱᴏᴅᴇꜱ ᴡᴀᴛᴄʜᴇᴅ:</b> {}
╠<b>ᴍɪɴᴜᴛᴇꜱ ᴡᴀᴛᴄʜᴇᴅ:</b> {}
╠<b>𝚂𝙲𝙾𝚁𝙴:</b> {}
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ 
╚══════════════════════╝
"""


NO_ANI_ADMIN = """
╔══════════════════════╗
╠╼ 👤 {}
╠╼ ⭐ <b>ʙᴏᴛ ᴀᴅᴍɪɴ</b>
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
╠<b>ᴀɴɪᴍᴇ ꜱᴇᴀʀᴄʜᴇᴅ:</b> {} 
╠<b>ᴀɴɪᴍᴇ ʀᴇ𝚀ᴜᴇꜱᴛᴇᴅ ꜱᴜʙ:</b> {} 
╠<b>ᴀɴɪᴍᴇ ʀᴇ𝚀ᴜᴇꜱᴛᴇᴅ ᴅᴜʙ:</b> {} 
╠<b>ᴀɴɪᴍᴇ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ:</b> {} 
╠══════════════════════
╠╼ 𝘿𝙖𝙩𝙖𝙗𝙖𝙨𝙚 𝙎𝙩𝙖𝙩𝙨  📂
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
╠<b>👥ᴜꜱᴇʀꜱ:</b> {}
╠<b>ᴛᴏᴛᴀʟ ꜱᴜʙ ᴀɴɪᴍᴇ:</b> {}
║<b>ꜱᴜʙ ᴘᴇɴᴅɪɴɢ ʀᴇ𝚀ᴜᴇꜱᴛ:</b> {}
╠<b>ᴛᴏᴛᴀʟ ᴅᴜʙ ᴀɴɪᴍᴇ:</b> {} 
║<b>ᴅᴜʙᴘᴇɴᴅɪɴɢ ʀᴇ𝚀ᴜᴇꜱᴛ:</b> {}
╚══════════════════════╝
"""

ANI_ADMIN = """
╔══════════════════════╗
╠╼ 👤 {}
╠╼ ⭐ <b>ʙᴏᴛ ᴀᴅᴍɪɴ</b>
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
╠><i> 𝙐𝙨𝙚𝙧 𝘼𝙣𝙞𝙢𝙚 𝙎𝙩𝙖𝙩𝙨 🖥️</i>
╠<b>ᴀɴɪᴍᴇ ᴡᴀᴛᴄʜᴇᴅ:</b> {} 
╠<b>ᴇᴘɪꜱᴏᴅᴇꜱ ᴡᴀᴛᴄʜᴇᴅ:</b> {}
╠<b>ᴍɪɴᴜᴛᴇꜱ ᴡᴀᴛᴄʜᴇᴅ:</b> {}
╠<b>𝚂𝙲𝙾𝚁𝙴:</b> {}
║
╠><i> 𝘽𝙤𝙩 𝘼𝙣𝙞𝙢𝙚 𝙎𝙩𝙖𝙩𝙨 💠</i>
╠<b>ᴀɴɪᴍᴇ ꜱᴇᴀʀᴄʜᴇᴅ:</b> {} 
╠<b>ᴀɴɪᴍᴇ ʀᴇ𝚀ᴜᴇꜱᴛᴇᴅ ꜱᴜʙ:</b> {} 
╠<b>ᴀɴɪᴍᴇ ʀᴇ𝚀ᴜᴇꜱᴛᴇᴅ ᴅᴜʙ:</b> {} 
╠<b>ᴀɴɪᴍᴇ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ:</b> {} 
╠══════════════════════
╠╼<i> 𝘽𝙤𝙩 𝘿𝙖𝙩𝙖𝙗𝙖𝙨𝙚 𝙎𝙩𝙖𝙩𝙨  📂</i>
╠<b>ᴜꜱᴇʀꜱ:</b> {}
╠<b>ᴛᴏᴛᴀʟ ꜱᴜʙ ᴀɴɪᴍᴇ:</b> {}
║<b>ꜱᴜʙ ᴘᴇɴᴅɪɴɢ ʀᴇ𝚀ᴜᴇꜱᴛ:</b> {}
╠<b>ᴛᴏᴛᴀʟ ᴅᴜʙ ᴀɴɪᴍᴇ:</b> {} 
║<b>ᴅᴜʙᴘᴇɴᴅɪɴɢ ʀᴇ𝚀ᴜᴇꜱᴛ:</b> {}
╚══════════════════════╝
"""


@Bot.on_message(get_cmd('stats') & sub_PUB_Dc & sub_PUB_Sc & sub_GC & sub_BOT_c)
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text="⌛")
    M = message.from_user.mention
    UID = message.from_user.id
    D_L, R_Qs, R_Qd, S_R, Ani_i = await get_user_stats(UID)
    USER_CLOSE = await user_close(UID)
    if UID in ADMINS:
        user = await full_userbase()
        US = len(user)
        suba = await full_sub_Animebase()
        SA = len(suba)
        duba = await full_dub_Animebase()
        DA = len(duba)
        r_s_p = await full_requestDB_SUB()
        SR = len(r_s_p)
        r_d_p = await full_requestDB_DUB()
        DR = len(r_d_p)
        if Ani_i == 0:
            await msg.edit(NO_ANI_ADMIN.format(M, S_R, R_Qs, R_Qd, D_L, US, SA, SR, DA, DR))
        else:
            message_photo, Ani_C, Ani_MW, Ani_EW, Ani_MS = await search_user_id(Ani_i)
            await msg.delete()
            await message.reply_photo(
                photo=message_photo,
                caption=ANI_ADMIN.format(M, Ani_C, Ani_EW, Ani_MW, Ani_MS, S_R, R_Qs, R_Qd, D_L, US, SA, SR, DA, DR),
                reply_markup=USER_CLOSE
            )

    else:
        if Ani_i == 0:
            await msg.edit(NO_ANI_MEM.format(M, S_R, R_Qs, R_Qd, D_L))
        else:
            message_photo, Ani_C, Ani_MW, Ani_EW, Ani_MS = await search_user_id(Ani_i)
            await msg.delete()
            await message.reply_photo(
                photo=message_photo,
                caption=ANI_MEM.format(M, S_R, R_Qs, R_Qd, D_L, Ani_C, Ani_EW, Ani_MW, Ani_MS),
                reply_markup=USER_CLOSE
            )

























