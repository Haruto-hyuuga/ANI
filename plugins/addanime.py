from bot import Bot
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS, Sub_C_url, Dub_C_url, REQUEST_GC, BOTUSERNAME, REQ_TOPIC_ID, ERR_TOPIC_ID, ANI_LOG_CHANNEL
from helper_func import sub_PUB_Sc, sub_PUB_Dc, sub_BOT_c, sub_GC
from database.anime_db import present_sub_anime, get_sub_anime, add_sub_anime, del_sub_anime, full_sub_Animebase
from database.anime_db import present_dub_anime, get_dub_anime, add_dub_anime, del_dub_anime, full_dub_Animebase
from database.database import full_userbase
from database.inline import Ani_log_inline_f

import httpx
 
async def get_Log_anime_i(anime_id: int):
    
    query = '''
        query ($id: Int) {
          Media(id: $id, type: ANIME) {
            id
            title {
              romaji
              english
              native
            }
            episodes
            bannerImage
          }
        }
    '''
    variables = {"id": anime_id}
    url = "https://graphql.anilist.co"
    response = httpx.post(url, json={"query": query, "variables": variables})


    if response.status_code != 200:
        A_PIC = "https://te.legra.ph/file/3a603811e9275a9edd593.jpg"
        A_Title = "api_error⚠️"
        Episodes = "api_error⚠️"
        return A_PIC, A_Title, Episodes

    data = response.json()["data"]
    anime = data["Media"]
    if not anime:
        A_PIC = "https://te.legra.ph/file/3a603811e9275a9edd593.jpg"
        A_Title = "not_found⚠️"
        Episodes = "not_found⚠️"
        return A_PIC, A_Title, Episodes

    A_Title = anime["title"]["english"] or anime["title"]["romaji"]
    Episodes = anime["episodes"]
    A_PIC = anime["bannerImage"]
    return A_PIC, A_Title, Episodes
    

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


@Bot.on_message(filters.command("subpost") & filters.user(ADMINS))
async def fchannelSUBpost(client, message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /find or /search")
        return
    try:
        anime_id = int(args[1])
    except (IndexError, ValueError):
        await message.reply_text(f"Index Error!   *_*\n Did you fuck up the number after command??")
        return

    query = '''
    query ($id: Int) {
        Media (id: $id, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            description
            format
            status
            episodes
            duration
            season
            seasonYear
            studios(isMain: true) {
                edges {
                    node {
                        name
                    }
                }
            }
            genres
            averageScore
            meanScore
        }
    }
    '''

    variables = {"id": anime_id}
    url = "https://graphql.anilist.co"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"query": query, "variables": variables})


    if response.status_code != 200:
        await message.reply_text("<b>FAILED TO GET ANIME INFO</b>\nTry Again, if problem persists contact me trough: @Maid_Robot", reply_markup=ERROR_BUTTON)
        return

    data = response.json()["data"]
    anime = data["Media"]
    if not anime:
        await message.reply_text(f"<b>NO ANIME FOUND WITH GIVEN ID '{anime_id}'.\n Did you fuck up with number after command??</b>\nTry Again, if problem persists contact me trough: @Maid_Robot", reply_markup=ERROR_BUTTON)
        return

    E_title = anime["title"]["english"] or "➖"
    J_title = anime["title"]["romaji"] or "➖"
    format = anime["format"]
    episodes = anime["episodes"]
    status = anime["status"]
    average_score = anime["averageScore"]
    
    MAX_GENRES_LEN = 30 
    genres = ", ".join(anime["genres"])
    if len(genres) > MAX_GENRES_LEN:
        genres = "\n│ ".join([genres[:MAX_GENRES_LEN], genres[MAX_GENRES_LEN:]])
    
    if "studios" in anime and anime["studios"] and "edges" in anime["studios"] and anime["studios"]["edges"] and len(anime["studios"]["edges"]) > 0 and "node" in anime["studios"]["edges"][0] and anime["studios"]["edges"][0]["node"] and "name" in anime["studios"]["edges"][0]["node"]:
        studio = anime["studios"]["edges"][0]["node"]["name"]
    else:
        studio = "unknown"
    duration = f"{anime['duration']} mins" if anime['duration'] else ""
    season = f"{anime['season']} {anime['seasonYear']}" if anime['season'] else ""
    
    title_img = f"https://img.anili.st/media/{anime_id}"

    POST_CAPTION = f"""
🇯🇵: <b>{J_title}</b>
🇬🇧: <b>{E_title}</b>
┏━━━━━━━━━━━━━━━━━━━━━━━
├<b>ᴇᴘɪꜱᴏᴅᴇꜱ:</b> {episodes}
├<b>ᴅᴜʀᴀᴛɪᴏɴ:</b> {duration}
├<b>ᴛʏᴘᴇ:</b> {format}
├<b>ɢᴇɴʀᴇꜱ:</b> <i>{genres}</i>
├<b>ꜱᴄᴏʀᴇ:</b> {average_score}
├<b>ꜱᴛᴜᴅɪᴏ:</b> {studio}
├<b>ꜱᴛᴀᴛᴜꜱ:</b> {status}
├<b>ᴘʀᴇᴍɪᴇʀᴇᴅ:</b> {season}
┣━━━━━━━━━━━━━━━━━━━━━━━
├<b>ᴀᴜᴅɪᴏ ᴛʀᴀᴄᴋ:</b> Japanese
├<b>ꜱᴜʙᴛɪᴛʟᴇ:</b> English 
┗━━━━━━━━━━━━━━━━━━━━━━━
"""
    CONFIRM_SUB_PB = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❗ CONFIRM POST TO SUB ✅", callback_data=f"SUBconfirmpostS_{anime_id}")
            ],
            [
                InlineKeyboardButton("🗑️ 𝗖𝗟𝗢𝗦𝗘", callback_data="close")
            ]
        ]
    )
    try:
        await message.reply_photo(photo=title_img, caption=POST_CAPTION, reply_markup=CONFIRM_SUB_PB)
    except Exception as e:
        await message.reply_text(e)
        await client.send_message(chat_id=REQUEST_GC, text=f"⚠️SUB Post CMD Error\nwhile sending final message\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)  


@Bot.on_message(filters.command("dubpost") & filters.user(ADMINS))
async def fchannelDuBpost(client, message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /find or /search")
        return
    try:
        anime_id = int(args[1])
    except (IndexError, ValueError):
        await message.reply_text(f"Index Error!   *_*\n Did you fuck up the number after command??")
        return

    query = '''
    query ($id: Int) {
        Media (id: $id, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            description
            format
            status
            episodes
            duration
            season
            seasonYear
            studios(isMain: true) {
                edges {
                    node {
                        name
                    }
                }
            }
            genres
            averageScore
            meanScore
        }
    }
    '''

    variables = {"id": anime_id}
    url = "https://graphql.anilist.co"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"query": query, "variables": variables})


    if response.status_code != 200:
        await message.reply_text("<b>FAILED TO GET ANIME INFO</b>\nTry Again, if problem persists contact me trough: @Maid_Robot", reply_markup=ERROR_BUTTON)
        return

    data = response.json()["data"]
    anime = data["Media"]
    if not anime:
        await message.reply_text(f"<b>NO ANIME FOUND WITH GIVEN ID '{anime_id}'.\n Did you fuck up with number after command??</b>\nTry Again, if problem persists contact me trough: @Maid_Robot", reply_markup=ERROR_BUTTON)
        return

    E_title = anime["title"]["english"] or "➖"
    J_title = anime["title"]["romaji"] or "➖"
    format = anime["format"]
    episodes = anime["episodes"]
    status = anime["status"]
    average_score = anime["averageScore"]
    
    MAX_GENRES_LEN = 30 
    genres = ", ".join(anime["genres"])
    if len(genres) > MAX_GENRES_LEN:
        genres = "\n│ ".join([genres[:MAX_GENRES_LEN], genres[MAX_GENRES_LEN:]])
    
    if "studios" in anime and anime["studios"] and "edges" in anime["studios"] and anime["studios"]["edges"] and len(anime["studios"]["edges"]) > 0 and "node" in anime["studios"]["edges"][0] and anime["studios"]["edges"][0]["node"] and "name" in anime["studios"]["edges"][0]["node"]:
        studio = anime["studios"]["edges"][0]["node"]["name"]
    else:
        studio = "unknown"
    duration = f"{anime['duration']} mins" if anime['duration'] else ""
    season = f"{anime['season']} {anime['seasonYear']}" if anime['season'] else ""
    
    title_img = f"https://img.anili.st/media/{anime_id}"

    POST_CAPTION = f"""
🇬🇧: <b>{E_title}</b>
🇯🇵: <b>{J_title}</b>
┏━━━━━━━━━━━━━━━━━━━━━━━
├<b>ᴇᴘɪꜱᴏᴅᴇꜱ:</b> {episodes}
├<b>ᴅᴜʀᴀᴛɪᴏɴ:</b> {duration}
├<b>ᴛʏᴘᴇ:</b> {format}
├<b>ɢᴇɴʀᴇꜱ:</b> <i>{genres}</i>
├<b>ꜱᴄᴏʀᴇ:</b> {average_score}
├<b>ꜱᴛᴜᴅɪᴏ:</b> {studio}
├<b>ꜱᴛᴀᴛᴜꜱ:</b> {status}
├<b>ᴘʀᴇᴍɪᴇʀᴇᴅ:</b> {season}
┣━━━━━━━━━━━━━━━━━━━━━━━
├<b>ᴀᴜᴅɪᴏ ᴛʀᴀᴄᴋ:</b> English, Japanese 
├<b>ꜱᴜʙᴛɪᴛʟᴇ:</b> Full English, Sign & Songs
┗━━━━━━━━━━━━━━━━━━━━━━━
"""
    CONFIRM_DUB_PB = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❗ CONFIRM POST TO SUB ✅", callback_data=f"DUBconfirmpostD_{anime_id}")
            ],
            [
                InlineKeyboardButton("🗑️ 𝗖𝗟𝗢𝗦𝗘", callback_data="close")
            ]
        ]
    )

    try:
        await message.reply_photo(photo=title_img, caption=POST_CAPTION, reply_markup=CONFIRM_DUB_PB)
    except Exception as e:
        await message.reply_text(e)
        await client.send_message(chat_id=REQUEST_GC, text=f"⚠️DUB Post CMD Error\nwhile sending final message\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)  

