from bot import Bot
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from database.inline import ERROR_BUTTON, ANIME_RESULT_B
from database.anime_db import present_sub_anime, get_sub_anime, present_dub_anime, get_dub_anime
from config import GROUP_url

@Bot.on_message(filters.command(["search", "find"]))
async def search_anime(client, message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>Bish Provide Name Of Anime You Want To Search!<b/>\n|> /search Naruto")
        return
    anime_name = " ".join(args[1:])

    # Build the AniList API query URL
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
            }
        }
    }
    '''
    variables = {"search": anime_name}
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})

    # Check if the API request was successful
    if response.status_code != 200:
        await message.reply_text("<b>FAILED TO GET ANIME INFO</b>\nTry Again, if problem persists contact me trough: @Maid_Robot", reply_markup=ERROR_BUTTON)
        return

    # Parse the API response and format the message
    data = response.json()["data"]
    anime_list = data["Page"]["media"]
    if not anime_list:
        await message.reply_text(f"<b>NO ANIME FOUND FOR PROVIDED QUERY '{anime_name}'.</b>\n\nTry Searching On Our Channel or Anilist and Copy Paste Title")
        return

    # Build the list of search results
    message_text = f"<u>Top search results for '{anime_name}'</u>:\n\n"
    for i, anime in enumerate(anime_list[:10]):
        title = anime["title"]["english"] or anime["title"]["romaji"]
        anime_id = anime["id"]
        message_text += f"<u>{i+1}</u>🖥️ : <b>{title}</b> \nDownload : <code> /download {anime_id} </code>\n\n"

    await message.reply_text(message_text, reply_markup=ANIME_RESULT_B)



@Bot.on_message(filters.command(["download", "anime"]))
async def anime_info(client, message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /anime or /search")
        return
    try:
        anime_id = int(args[1])
    except IndexError:
        await message.reply_text(f"Index Error!   *_*\n Did you fuck up with number after command?? *_*")
        return
    except ValueError:
        await message.reply_text(f"Value Error!   *_* \n Did you fuck up with number after command??")
        return
    
    # Build the AniList API query URL
    query = '''
    query ($id: Int) {
        Media (id: $id, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            coverImage {
                extraLarge
            }
            description
            format
            episodes
            status
            genres
            averageScore
            studios(isMain: true) {
                edges {
                    node {
                        name
                    }
                }
            }
            duration
            season
            seasonYear
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
    response = requests.post(url, json={"query": query, "variables": variables})

    # Check if the API request was successful
    if response.status_code != 200:
        await message.reply_text("<b>FAILED TO GET ANIME INFO</b>\nTry Again, if problem persists contact me trough: @Maid_Robot", reply_markup=ERROR_BUTTON)
        return

    # Parse the API response and format the message
    data = response.json()["data"]
    anime = data["Media"]
    if not anime:
        await message.reply_text(f"No anime found with the ID '{anime_id}'.\n Did you fuck up with number after command?? *_*")
        return

    title = anime["title"]["english"] or anime["title"]["romaji"]
    cover_url = anime["coverImage"]["extraLarge"]
    episodes = anime["episodes"]
    status = anime["status"]
    genres = ", ".join(anime["genres"])
    average_score = anime["averageScore"]
    duration = f"{anime['duration']} mins" if anime['duration'] else ""
    season = f"{anime['season']} {anime['seasonYear']}" if anime['season'] else ""
    
    message_text = f"<b>{title}</b>\n\n"
    message_text += f"ɢᴇɴʀᴇꜱ: <i>{genres}</i>\n"
    message_text += f"ᴇᴘɪꜱᴏᴅᴇꜱ: <b>{episodes}</b>\n"
    message_text += f"ᴅᴜʀᴀᴛɪᴏɴ: <b>{duration}</b>\n"
    message_text += f"ꜱᴄᴏʀᴇ: <b>{average_score}</b>\n"
    message_text += f"ꜱᴛᴀᴛᴜꜱ: <b>{status}</b>\n"
    message_text += f"ʀᴇʟᴇᴀꜱᴇᴅ: <b>{season}</b>\n"
    message_text += f"<b>𝑭𝒐𝒓 𝒅𝒆𝒕𝒂𝒊𝒍𝒆𝒅 𝑰𝒏𝒇𝒐 𝒂𝒃𝒐𝒖𝒕 𝑨𝒏𝒊𝒎𝒆 𝒕𝒚𝒑𝒆:</b> <code>/info {anime_id}</code>\n"
    buttons = []
    
    if await present_sub_anime(anime_id):
        try:
            sblink = await get_sub_anime(anime_id)
            buttons.append([InlineKeyboardButton("𝗝𝗮𝗽𝗮𝗻𝗲𝘀𝗲 𝗦𝗨𝗕 (𝟰𝟴𝟬𝗽-𝟳𝟮𝟬𝗽-𝟭𝟬𝟴𝟬𝗽 | 🔊:🇯🇵)", url = sblink)])
            message_text += "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"
            message_text += "<b>✅DOWNLOAD AVAILABLE SUB<b/>\n"
        except Exception as e:
            await message.reply_text(e)
            
    if await present_dub_anime(anime_id):
        try:
            dblink = await get_dub_anime(anime_id)
            buttons.append([InlineKeyboardButton("𝗘𝗻𝗴𝗹𝗶𝘀𝗵 𝗗𝗨𝗕 (𝟰𝟴𝟬𝗽-𝟳𝟮𝟬𝗽-𝟭𝟬𝟴𝟬𝗽 | 🔊:🇯🇵🇬🇧)", url = dblink)])
            message_text += "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"
            message_text += "<b>✅DOWNLOAD AVAILABLE DUB</b>\n"
        except Exception as e:
            await message.reply_text(e)
    if not await present_sub_anime(anime_id):
        try:
            buttons.append([InlineKeyboardButton("𝗥𝗘𝗤𝗨𝗘𝗦𝗧 𝗔𝗡𝗜𝗠𝗘 (𝗦𝗨𝗕) ⛩️", callback_data="REQUEST_SA")])
            message_text += "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"
            message_text += "<b>❌SUB DOWNLOAD NOT AVAILABLE</b>\n"
        except Exception as e:
            await message.reply_text(e)
    if not await present_dub_anime(anime_id):
        try:
            buttons.append([InlineKeyboardButton("𝗥𝗘𝗤𝗨𝗘𝗦𝗧 𝗔𝗡𝗜𝗠𝗘 (𝗗𝗨𝗕) 🗺️", callback_data="REQUEST_DA")])
            message_text += "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"
            message_text += "<b>❌DUB DOWNLOAD NOT AVAILABLE</b>\n"
        except Exception as e:
            await message.reply_text(e)
    message_text += "〰️〰️〰️〰️〰️〰️✖️〰️〰️〰️〰️〰️〰️\n"
    try:
        await message.reply_photo(cover_url, caption=message_text, reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        await message.reply_text(e, reply_markup=ERROR_BUTTON)   



@Bot.on_message(filters.command(["anime_info", "info"]))
async def animefulinfo(client, message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /anime or /search")
        return
    try:
        anime_id = int(args[1])
    except IndexError:
        await message.reply_text(f"Index Error!   *_*\n Did you fuck up with number after command?? *_*")
        return
    except ValueError:
        await message.reply_text(f"Value Error!   *_* \n Did you fuck up with number after command??")
        return

    # Build the AniList API query URL
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
            studios(isMain: true) {
                nodes {
                    name
                }
            }
            genres
            averageScore
            meanScore
            popularity
            siteUrl
        }
    }
    '''

    variables = {"id": anime_id}
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})

    # Check if the API request was successful
    if response.status_code != 200:
        await message.reply_text("Failed to get anime info.")
        return

    # Parse the API response and format the message
    data = response.json()["data"]
    anime = data["Media"]
    if not anime:
        await message.reply_text(f"No anime found with the ID '{anime_id}'.")
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
    studio = anime["studios"]["edges"][0]["node"]["name"]
    start_date = f"{anime['startDate']['day']}/{anime['startDate']['month']}/{anime['startDate']['year']}"
    end_date = f"{anime['endDate']['day']}/{anime['endDate']['month']}/{anime['endDate']['year']}" if anime['endDate'] else ""
    duration = f"{anime['duration']} mins" if anime['duration'] else ""
    season = f"{anime['season']} {anime['seasonYear']}" if anime['season'] else ""
    trailer_url = f"https://www.youtube.com/watch?v={anime['trailer']['id']}" if anime['trailer'] else "https://t.me/AnimeRobots"
    site_url = anime['siteUrl']


    message_text = f"<b>{title}</b>\n"
    try:
        message_text += f"ꜱᴛᴜᴅɪᴏ: <b>{studio}</b>\n"
    except:
        message_text += "ꜱᴛᴜᴅɪᴏ: unable to fetch"
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
        await message.reply_photo(cover_url, caption=f"<b>{title}</b>\n{description}")
    except Exception as e:
        await message.reply_text(e, reply_markup=ERROR_BUTTON)   

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
    try:
        await message.reply_photo(banner_url, caption=message_text, reply_markup=YtRESULT_B)
    except Exception as e:
        await message.reply_text(e, reply_markup=ERROR_BUTTON)   















