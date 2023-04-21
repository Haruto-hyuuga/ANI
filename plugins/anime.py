from bot import Bot
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import random 
import httpx
from database.inline import ERROR_BUTTON, ANIME_RESULT_B
from database.anime_db import present_sub_anime, get_sub_anime, present_dub_anime, get_dub_anime
from config import GROUP_url, FS_GROUP, ALLCMD_FS_TXT, ALLCMD_FS_PIC, ERR_TOPIC_ID, REQUEST_GC
from helper_func import sub_PUB_Sc, sub_PUB_Dc, sub_BOT_c, sub_GC

async def R_Banner_Pic():
    P1 = "https://telegra.ph/file/dd68804360b9e21ddadb3.jpg"
    P2 = "https://telegra.ph/file/d9a39ff5a124111e2f41d.jpg"
    P3 = "https://telegra.ph/file/4bbfb4c68f55259c071d9.jpg"
    P4 = "https://telegra.ph/file/76a2594f28616ef562db2.jpg"
    P5 = "https://telegra.ph/file/6e75a326ec4229e9c02d9.jpg"
    P6 = "https://telegra.ph/file/b624ef44cb45a20d8db51.jpg"
    P7 = "https://telegra.ph/file/7e4987fd73dda121bfccf.jpg"
    P8 = "https://telegra.ph/file/38a10470c95a78708f008.jpg"
    P9 = "https://telegra.ph/file/dd68804360b9e21ddadb3.jpg"
    P10 = "https://telegra.ph/file/85c5229265237e8c42055.jpg"
    P = [P1, P2, P3, P4, P5, P6, P7, P8, P9, P10]
    M_banner_Pic = random.choice(P)
    return M_banner_Pic

@Bot.on_message(filters.command(["search", "find"]) & sub_PUB_Dc & sub_PUB_Sc & sub_GC & sub_BOT_c & filters.private)
async def search_anime(client, message):
    
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>Bish Provide Name Of Anime You Want To Search!<b/>\n|> /search Naruto")
        return
    anime_name = " ".join(args[1:])

    
    query = '''
        query ($search: String) {
            Page {
                media(search: $search, type: ANIME) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    episodes
                    duration
                    status
                    bannerImage
                }
            }
        }
    '''
    variables = {"search": anime_name}
    url = "https://graphql.anilist.co"
    response = httpx.post(url, json={"query": query, "variables": variables})

   
    if response.status_code != 200:
        await message.reply_text("<b>FAILED TO GET ANIME INFO</b>\nTry Again, if problem persists contact me trough: @Maid_Robot", reply_markup=ERROR_BUTTON)
        return

    
    data = response.json()["data"]
    anime_list = data["Page"]["media"]
    if not anime_list:
        await message.reply_text(f"<b>NO ANIME FOUND FOR PROVIDED QUERY '{anime_name}'.</b>\n\nTry Searching On Our Channel or Anilist and Copy Paste Title")
        return

    banner_image = None
    if len(anime_list) == 1:
        banner_image = anime_list[0]["bannerImage"]
    else:
        banner_images = [anime["bannerImage"] for anime in anime_list if anime["bannerImage"]]
        if banner_images:
            banner_image = random.choice(banner_images)


    message_text = f"<u>𝙏𝙤𝙥 𝙨𝙚𝙖𝙧𝙘𝙝 𝙧𝙚𝙨𝙪𝙡𝙩𝙨 𝙛𝙤𝙧 '{anime_name}'</u>:\n\n"
    for i, anime in enumerate(anime_list[:10]):
        title = anime["title"]["english"] or anime["title"]["romaji"]
        anime_id = anime["id"]
        episodes = anime["episodes"] or "𝚞𝚗𝚔𝚗𝚘𝚠𝚗"
        status = anime["status"] or "𝚞𝚗𝚔𝚗𝚘𝚠𝚗"
        try:
            duration = f"{anime['duration']} mins" if anime['duration'] else ""
        except:
            duration = "𝚞𝚗𝚔𝚗𝚘𝚠𝚗"

        message_text += f"<b><u>{i+1}</u></b>🏷️: <b>{title}</b>\n🖥️ᴇᴘɪꜱᴏᴅᴇꜱ: <b>{episodes} 🕒: <b>{duration}</b>  ꜱᴛᴀᴛᴜꜱ: <b>{status}</b>\n➥<code> /download {anime_id} </code>\n\n"

    if banner_image:
        try:
            await message.reply_photo(
                photo=banner_image,
                caption=message_text,
                reply_markup=ANIME_RESULT_B
            )
        except Exception as e:
            await message.reply_text(
                text=message_text,
                reply_markup=ANIME_RESULT_B
            )
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Search CMD-PVT Error\nrandom API banner image\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
            
    else:
        M_banner_Pic = await R_Banner_Pic()
        try:
            await message.reply_photo(
                photo=M_banner_Pic,
                caption=message_text,
                reply_markup=ANIME_RESULT_B
            )
        except Exception as e:
            await message.reply_text(
                text=message_text,
                reply_markup=ANIME_RESULT_B
            )
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Search CMD-PVT Error\nrandom saved banner image\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
            

@Bot.on_message(filters.command(["download", "anime"]) & sub_PUB_Dc & sub_PUB_Sc & sub_GC & sub_BOT_c & filters.private)
async def anime_info(client, message):

    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /find or /search")
        return
    try:
        anime_id = int(args[1])
    except (IndexError, ValueError):
        await message.reply_text(f"Index Error!   *_*\n Did you fuck up with number after command??")
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
            bannerImage
            coverImage {
                extraLarge
            }
            episodes
            status
            genres
            studios(isMain: true) {
                edges {
                    node {
                        name
                    }
                }
            }
            duration
            trailer {
                id
                site
                thumbnail
            }
        }
    }
    '''
    variables = {"id": anime_id}
    url = "https://graphql.anilist.co"
    response = httpx.post(url, json={"query": query, "variables": variables})

    if response.status_code != 200:
        await message.reply_text("<b>FAILED TO GET ANIME INFO</b>\nTry Again, if problem persists contact me trough: @Maid_Robot", reply_markup=ERROR_BUTTON)
        return

    data = response.json()["data"]
    anime = data["Media"]
    if not anime:
        await message.reply_text(f"No anime found with the ID '{anime_id}'.\n Did you fuck up the number after command?? *_*")
        return

    title = anime["title"]["english"] or anime["title"]["romaji"]
    episodes = anime["episodes"]
    status = anime["status"]
    genres = ", ".join(anime["genres"])
    
    duration = f"{anime['duration']} mins" if anime['duration'] else ""
    
    message_text = f"<b>{title}</b>\n\n"
    message_text += f"ɢᴇɴʀᴇꜱ: <i>{genres}</i>\n"
    message_text += f"ᴇᴘɪꜱᴏᴅᴇꜱ: <b>{episodes}</b>\n"
    message_text += f"ᴅᴜʀᴀᴛɪᴏɴ: <b>{duration}</b>\n"
    message_text += f"ꜱᴛᴀᴛᴜꜱ: <b>{status}</b>\n"

    buttons = []
    if await present_sub_anime(anime_id):
        try:
            sblink = await get_sub_anime(anime_id)
            buttons.append([InlineKeyboardButton("𝗝𝗮𝗽𝗮𝗻𝗲𝘀𝗲 𝗦𝗨𝗕 (𝟰𝟴𝟬𝗽-𝟳𝟮𝟬𝗽-𝟭𝟬𝟴𝟬𝗽 | 🔊:🇯🇵)", url = sblink)])
            message_text += "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"
            message_text += "<b>✅DOWNLOAD AVAILABLE SUB</b>\n"
        except Exception as e:
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️download CMD-PVT Error\nif present sub anime\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
            
    if await present_dub_anime(anime_id):
        try:
            dblink = await get_dub_anime(anime_id)
            buttons.append([InlineKeyboardButton("𝗘𝗻𝗴𝗹𝗶𝘀𝗵 𝗗𝗨𝗕 (𝟰𝟴𝟬𝗽-𝟳𝟮𝟬𝗽-𝟭𝟬𝟴𝟬𝗽 | 🔊:🇯🇵🇬🇧)", url = dblink)])
            message_text += "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"
            message_text += "<b>✅DOWNLOAD AVAILABLE DUB</b>\n"
        except Exception as e:
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️download CMD-PVT Error\nif present dub\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
    if not await present_sub_anime(anime_id):
        try:
            buttons.append([InlineKeyboardButton("𝗥𝗘𝗤𝗨𝗘𝗦𝗧 𝗔𝗡𝗜𝗠𝗘 (𝗦𝗨𝗕) ⛩️", callback_data="REQUEST_SA")])
            message_text += "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"
            message_text += "❌ @ANIME_DOWNLOADS_SUB\n<b>➥ NOT AVAILABLE</b>\n"
        except Exception as e:
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️download CMD-PVT Error\nif not present sub\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    if not await present_dub_anime(anime_id):
        try:
            buttons.append([InlineKeyboardButton("𝗥𝗘𝗤𝗨𝗘𝗦𝗧 𝗔𝗡𝗜𝗠𝗘 (𝗗𝗨𝗕) 🗺️", callback_data="REQUEST_DA")])
            message_text += "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"
            message_text += "❌ @ANIME_DOWNLOADS_DUB<b>\n➥ NOT AVAILABLE</b>\n"
        except Exception as e:
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️download CMD-PVT Error\nif not present dub\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    message_text += "〰️〰️〰️〰️〰️〰️✖️〰️〰️〰️〰️〰️〰️\n"
    message_text += f"<b>ꜰᴏʀ ᴍᴏʀᴇ ᴀɴɪᴍᴇ ᴅᴇᴛᴀɪʟꜱ ᴛʏᴘᴇ:</b> \n<code>/info {anime_id}</code>\n"
    
    title_img = f"https://img.anili.st/media/{anime_id}"
    try:
        await message.reply_photo(title_img, caption=message_text, reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        await message.reply_text("An Error Occurred, Try Agin\nIf Problem persist Contact me 🛂", reply_markup=ERROR_BUTTON)
        await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Anime/Download CMD-PVT Error\nwhile sending final message\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)  



@Bot.on_message(filters.command(["anime_info", "info"]) & sub_PUB_Dc & sub_PUB_Sc & sub_GC & sub_BOT_c & filters.private)
async def animefulinfo(client, message):
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
            bannerImage
            coverImage {
                extraLarge
            }
            description
            format
            status
            episodes
            duration
            season
            seasonYear
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            averageScore
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
            popularity
            siteUrl
            trailer {
                id
            }
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

    title = anime["title"]["english"] or anime["title"]["romaji"]
    cover_url = anime["coverImage"]["extraLarge"]
    banner_url = anime["bannerImage"]
    description = anime["description"]
    format = anime["format"]
    episodes = anime["episodes"]
    status = anime["status"]
    genres = ", ".join(anime["genres"])
    average_score = anime["averageScore"]
    mean_score = anime["meanScore"]
    popularity = anime['popularity']
    if "studios" in anime and anime["studios"] and "edges" in anime["studios"] and anime["studios"]["edges"] and len(anime["studios"]["edges"]) > 0 and "node" in anime["studios"]["edges"][0] and anime["studios"]["edges"][0]["node"] and "name" in anime["studios"]["edges"][0]["node"]:
        studio = anime["studios"]["edges"][0]["node"]["name"]
    else:
        studio = "Unknown Studio"
    start_date = f"{anime['startDate']['day']}/{anime['startDate']['month']}/{anime['startDate']['year']}"
    end_date = f"{anime['endDate']['day']}/{anime['endDate']['month']}/{anime['endDate']['year']}" if anime['endDate'] else ""
    duration = f"{anime['duration']} mins" if anime['duration'] else ""
    season = f"{anime['season']} {anime['seasonYear']}" if anime['season'] else ""
    trailer_url = f"https://www.youtube.com/watch?v={anime['trailer']['id']}" if anime['trailer'] else "https://t.me/AnimeRobots"
    site_url = anime['siteUrl']


#    message_text = f"<b>{title}</b>\n"
    message_text = " "
    try:
        message_text += f"ꜱᴛᴜᴅɪᴏ: <b>{studio}</b>\n"
    except:
        message_text += "ꜱᴛᴜᴅɪᴏ: unknown"
    message_text += f"ᴀᴠᴇʀᴀɢᴇ ꜱᴄᴏʀᴇ: <b>{average_score}</b>\n"
    message_text += f"ᴍᴇᴀɴ ꜱᴄᴏʀᴇ: <b>{mean_score}</b>\n"
    message_text += f"ɢᴇɴʀᴇꜱ: <i>{genres}</i>\n"
    message_text += f"ᴇᴘɪꜱᴏᴅᴇꜱ: <b>{episodes}</b>\n"
    message_text += f"ᴅᴜʀᴀᴛɪᴏɴ: <b>{duration}</b>\n"
    message_text += f"ꜰᴏʀᴍᴀᴛ: <b>{format}</b>\n"
    message_text += f"ᴘᴏᴘᴜʟᴀʀɪᴛʏ: <b>{popularity}</b>\n"
    message_text += f"ꜱᴛᴀᴛᴜꜱ: <b>{status}</b>\n"
    message_text += f"ʀᴇʟᴇᴀꜱᴇᴅ: <b>{season}</b>\n"
    message_text += f"ꜱᴛᴀʀᴛᴇᴅ: <b>{start_date}</b>\n"
    message_text += f"ᴇɴᴅᴇᴅ: <b>{end_date}</b>\n"
    
    try:
        await message.reply_photo(banner_url, caption=f"<b>{title}</b>\n\n{description}")
    except Exception as e:
        await message.reply_photo(cover_url, caption=f"<b>{title}</b>\n\n{description}")
        await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Full anime info CMD-PVT MSG-1 Error\nwhile banner img with description\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    YtRESULT_B = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🖥️ Anime Site", url=site_url),
                InlineKeyboardButton("Watch Trailer 🖥️", url=trailer_url)
            ],
            [
                InlineKeyboardButton("💬 ANIME GROUP CHAT 💬", url=GROUP_url),
            ]
        ]
    )
    title_img = f"https://img.anili.st/media/{anime_id}"
    try:
        await message.reply_photo(title_img, caption=message_text, reply_markup=YtRESULT_B)
    except Exception as e:
        await message.reply_text("An Error Occurred, Try Agin\nIf Problem persist Contact me 🛂", reply_markup=ERROR_BUTTON)
        await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Full anime info CMD-PVT MSG-2 Error\ntitle image and infos\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)



@Bot.on_message(filters.command(["search", "find"]) & filters.chat(FS_GROUP))
async def gcanimesearch(client, message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>Bish Provide Name Of Anime You Want To Search!<b/>\n|> /search Naruto")
        return
    anime_name = " ".join(args[1:])

    
    query = '''
        query ($search: String) {
            Page {
                media(search: $search, type: ANIME) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    episodes
                    duration
                    status
                    bannerImage
                }
            }
        }
    '''
    variables = {"search": anime_name}
    url = "https://graphql.anilist.co"
    response = httpx.post(url, json={"query": query, "variables": variables})

   
    if response.status_code != 200:
        await message.reply_text("<b>FAILED TO GET ANIME INFO</b>\nTry Again, if problem persists contact me trough: @Maid_Robot", reply_markup=ERROR_BUTTON)
        return

    
    data = response.json()["data"]
    anime_list = data["Page"]["media"]
    if not anime_list:
        await message.reply_text(f"<b>NO ANIME FOUND FOR PROVIDED QUERY '{anime_name}'.</b>\n\nTry Searching On Our Channel or Anilist and Copy Paste Title")
        return

    banner_image = None
    if len(anime_list) == 1:
        banner_image = anime_list[0]["bannerImage"]
    else:
        banner_images = [anime["bannerImage"] for anime in anime_list if anime["bannerImage"]]
        if banner_images:
            banner_image = random.choice(banner_images)


    message_text = f"<u>𝙏𝙤𝙥 𝙨𝙚𝙖𝙧𝙘𝙝 𝙧𝙚𝙨𝙪𝙡𝙩𝙨 𝙛𝙤𝙧 '{anime_name}'</u>:\n\n"
    for i, anime in enumerate(anime_list[:10]):
        title = anime["title"]["english"] or anime["title"]["romaji"]
        anime_id = anime["id"]
        episodes = anime["episodes"] or "𝚞𝚗𝚔𝚗𝚘𝚠𝚗"
        status = anime["status"] or "𝚞𝚗𝚔𝚗𝚘𝚠𝚗"
        duration = f"{anime['duration']} mins" if anime['duration'] else ""

        message_text += f"<b><u>{i+1}</u></b>🏷️: <b>{title}</b>\n🖥️ᴇᴘɪꜱᴏᴅᴇꜱ: <b>{episodes}</b> 🕒:<b>{duration}</b>  ꜱᴛᴀᴛᴜꜱ: <b>{status}</b>\n➥<code> /download {anime_id} </code>\n\n"


    RESULT_B = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🗑️ 𝗖𝗟𝗢𝗦𝗘", callback_data=f"gcAresultclose"),
                InlineKeyboardButton("𝗡𝗼𝘁 𝗶𝗻 𝗟𝗶𝘀𝘁 🔎", callback_data="anime_notfound_popup")
            ]
        ]
    )
    if banner_image:
        try:
            await message.reply_photo(
                photo=banner_image,
                caption=message_text,
                reply_markup=RESULT_B
            )
        except Exception as e:
            await message.reply_text(
                text=message_text,
                reply_markup=RESULT_B
            )
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Search CMD-GC Error\nrandom API banner image\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
    else:
        M_banner_Pic = await R_Banner_Pic()
        try:
            await message.reply_photo(
                photo=M_banner_Pic,
                caption=message_text,
                reply_markup=RESULT_B
            )
        except Exception as e:
            await message.reply_text(
                text=message_text,
                reply_markup=RESULT_B
            )
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Search CMD-GC Error\nrandom saved banner image\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
            

@Bot.on_message(filters.command(["download", "anime"]) & filters.chat(FS_GROUP))
async def gcanimedlcmd(client, message):
    user = message.from_user.id
    args = message.text.split()
    if len(args) < 2:
 #       await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /anime or /search")
        return
    try:
        anime_id = int(args[1])
    except (IndexError, ValueError):
 #       await message.reply_text(f"Index Error!   *_*\n Did you fuck up with number after command??")
        return

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
            status
            genres
            duration
            averageScore
          }
        }
    '''
    variables = {"id": anime_id}
    url = "https://graphql.anilist.co"
    response = httpx.post(url, json={"query": query, "variables": variables})


    if response.status_code != 200:
        await message.reply_text("<b>FAILED TO GET ANIME INFO</b>\nTry Again, if problem persists contact me trough: @Maid_Robot", reply_markup=ERROR_BUTTON)
        return

    data = response.json()["data"]
    anime = data["Media"]
    if not anime:
        await message.reply_text(f"No anime found with the ID '{anime_id}'.\n Did you fuck up with number after command?? *_*")
        return

    title = anime["title"]["english"] or anime["title"]["romaji"]
    episodes = anime["episodes"]
    status = anime["status"]
    genres = ", ".join(anime["genres"])
    title_img = f"https://img.anili.st/media/{anime_id}"
    average_score = anime["averageScore"]
    duration = f"{anime['duration']} mins" if anime['duration'] else ""

    message_text = f"<b>{title}</b>\n"
    message_text += f"ᴇᴘɪꜱᴏᴅᴇꜱ: <b>{episodes}</b>\n"
    message_text += f"ᴅᴜʀᴀᴛɪᴏɴ: <b>{duration}</b>\n"
    message_text += f"ꜱᴛᴀᴛᴜꜱ: <b>{status}</b>\n"
    message_text += f"ɢᴇɴʀᴇꜱ: <i>{genres}</i>\n\n"

    buttons = []

    if await present_sub_anime(anime_id):
        try:
            sblink = await get_sub_anime(anime_id)
            buttons.append([InlineKeyboardButton("𝗝𝗮𝗽𝗮𝗻𝗲𝘀𝗲 𝗦𝗨𝗕 (𝟰𝟴𝟬𝗽-𝟳𝟮𝟬𝗽-𝟭𝟬𝟴𝟬𝗽 | 🔊:🇯🇵)", url = sblink)])
            message_text += f"<b>ꜱᴜʙ ᴄʜᴀɴɴᴇʟ:</b> ✅\n"
        except Exception as e:
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️download CMD-GC Error\nif present SUB anime button\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
            
    if await present_dub_anime(anime_id):
        try:
            dblink = await get_dub_anime(anime_id)
            buttons.append([InlineKeyboardButton("𝗘𝗻𝗴𝗹𝗶𝘀𝗵 𝗗𝗨𝗕 (𝟰𝟴𝟬𝗽-𝟳𝟮𝟬𝗽-𝟭𝟬𝟴𝟬𝗽 | 🔊:🇯🇵🇬🇧)", url = dblink)])
            message_text += f"<b>ᴅᴜʙ ᴄʜᴀɴɴᴇʟ:</b> ✅\n"
        except Exception as e:
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️download CMD-GC Error\nif present DUB anime button\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    if not await present_sub_anime(anime_id):
        try:
            buttons.append([InlineKeyboardButton("𝗥𝗘𝗤𝗨𝗘𝗦𝗧 𝗔𝗡𝗜𝗠𝗘 (𝗦𝗨𝗕) ⛩️", callback_data="REQUEST_SA")])
            message_text += f"<b>ꜱᴜʙ ᴄʜᴀɴɴᴇʟ:</b> ❌\n"
        except Exception as e:
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️download CMD-GC Error\nif NOT present SUB anime button\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    if not await present_dub_anime(anime_id):
        try:
            buttons.append([InlineKeyboardButton("𝗥𝗘𝗤𝗨𝗘𝗦𝗧 𝗔𝗡𝗜𝗠𝗘 (𝗗𝗨𝗕) 🗺️", callback_data="REQUEST_DA")])
            message_text += f"<b>ᴅᴜʙ ᴄʜᴀɴɴᴇʟ</b> ❌\n"
        except Exception as e:
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️download CMD-GC Error\nif NOT present DUB anime button\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    if message.reply_to_message:
        try:
            buttons.append([InlineKeyboardButton("🗑️ 𝗖𝗟𝗢𝗦𝗘", callback_data=f"gcAresultclose"), InlineKeyboardButton("ℹ️⚠️", callback_data="GroupAnimeInfo")])
            await message.reply_to_message.reply_photo(title_img, caption=message_text, reply_markup=InlineKeyboardMarkup(buttons))
        except Exception as e:
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️download/anime CMD-GC Error\nFinal Msg while if replying to msg\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    if not message.reply_to_message:
        try:
            buttons.append([InlineKeyboardButton("🗑️ 𝗖𝗟𝗢𝗦𝗘", callback_data=f"gcAresultclose"), InlineKeyboardButton("ℹ️⚠️", callback_data="GroupAnimeInfo")])
            await client.send_photo(chat_id=message.chat.id, photo=title_img, caption=message_text, reply_markup=InlineKeyboardMarkup(buttons))
        except Exception as e:
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️download/anime CMD-GC Error\nFinal Msg Not Reply to msg\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)



@Bot.on_message(filters.command(["search", "find"]) & filters.private)
async def nosearchpvtcleft(client, message):
     await message.reply_photo(photo=ALLCMD_FS_PIC, caption=ALLCMD_FS_TXT)
  
@Bot.on_message(filters.command(["download", "anime"]) & filters.private)
async def nodownloadleftc(client, message):
     await message.reply_photo(photo=ALLCMD_FS_PIC, caption=ALLCMD_FS_TXT)
  
@Bot.on_message(filters.command(["anime_info", "info"]) & filters.private)
async def nofullanineleftc(client, message):
     await message.reply_photo(photo=ALLCMD_FS_PIC, caption=ALLCMD_FS_TXT)
        

@Bot.on_message(filters.command("request") & filters.private)
async def norequestleftc(client, message):
     await message.reply_photo(photo=ALLCMD_FS_PIC, caption=ALLCMD_FS_TXT)
    
