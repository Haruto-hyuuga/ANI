import httpx
import random 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.inline import ERROR_BUTTON, ANIME_RESULT_B, NOani_BUTTON



ERROR_IMAGE = "https://telegra.ph/file/5d770ae91df7457adbd28.jpg"
NOani_IMAGE = "https://telegra.ph/file/ecbd1f30a4a3ea06d025b.jpg"
NO_banner_IMG = "https://telegra.ph/file/54cc2b780cb7a4f25c5dd.jpg"



async def search_anime_list_by_Name(anime_name: str):
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
        message_text = "<b>FAILED TO GET ANIME INFO</b>\nTry Again, if problem persists contact me trough: @Maid_Robot"
        message_button = ERROR_BUTTON
        message_photo = ERROR_IMAGE
        return message_text, message_button, message_photo 
    
    data = response.json()["data"]
    anime_list = data["Page"]["media"]
    if not anime_list:
        message_text = f"<b>NO ANIME FOUND FOR PROVIDED QUERY '{anime_name}'.</b>\n\nTry Searching On Our Channel or Anilist and Copy Paste Title"
        message_button = NOani_BUTTON
        message_photo = NOani_IMAGE
        return message_text, message_button, message_photo

    banner_image = None
    if len(anime_list) == 1:
        banner_image = anime_list[0]["bannerImage"]
    else:
        banner_images = [anime["bannerImage"] for anime in anime_list if anime["bannerImage"]]
        if banner_images:
            banner_image = random.choice(banner_images)

    message_text = "<u>𝙏𝙤𝙥 𝙨𝙚𝙖𝙧𝙘𝙝 𝙧𝙚𝙨𝙪𝙡𝙩𝙨 𝙛𝙤𝙧 '{anime_name}'</u>:\n\n"
    buttons = []
    for i, anime in enumerate(anime_list[:5]):
        title = anime["title"]["english"] or anime["title"]["romaji"]
        anime_id = anime["id"]
        status = anime["status"]
        
        if status == "FINISHED":
            status_emoji = "🖥️"
        elif status == "RELEASING":
            status_emoji = "🆕"
        elif status == "NOT_YET_RELEASED":
            status_emoji = "🔜"
        elif status == "CANCELLED":
            status_emoji = "❌"
        elif status == "HIATUS":
            status_emoji = "🛑"
        elif status == "UPCOMING":
            status_emoji = "🎞️"
        else:
            status_emoji = ""
            
        buttons.append([InlineKeyboardButton(f"{status_emoji} {title}", callback_data=f"Anime_{anime_id}")])
    try:
        buttons.append(
            [
                InlineKeyboardButton("🗑️ 𝗖𝗟𝗢𝗦𝗘", callback_data="close"),
                InlineKeyboardButton("Not In List", callback_data="anime_notfound_popup")
            ]
        )
    except:
        pass
    message_photo = banner_image or NO_banner_IMG
    message_button = InlineKeyboardMarkup(buttons)
    return message_text, message_button, message_photo


async def search_find_anime_list(anime_name: str):
    
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
        message_text = "<b>FAILED TO GET ANIME INFO</b>\nTry Again, if problem persists contact me trough: @Maid_Robot"
        message_button = ERROR_BUTTON
        message_photo = ERROR_IMAGE
        return message_text, message_button, message_photo

    
    data = response.json()["data"]
    anime_list = data["Page"]["media"]
    if not anime_list:
        message_text = f"<b>NO ANIME FOUND FOR PROVIDED QUERY '{anime_name}'.</b>\n\nTry Searching On Our Channel or Anilist and Copy Paste Title"
        message_button = NOani_BUTTON
        message_photo = NOani_IMAGE
        return message_text, message_button, message_photo

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

        message_text += f"<b><u>{i+1}</u></b>🏷️: <b>{title}</b>\n<i>🖥️ᴇᴘɪꜱᴏᴅᴇꜱ: {episodes} 🕒ᴅᴜʀᴀᴛɪᴏɴ: {duration}</i>\n➥<code> /download {anime_id} </code>\n\n"
        message_photo = banner_image or NO_banner_IMG
        message_button = ANIME_RESULT_B
        return message_text, message_button, message_photo
        
        
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
        A_PIC = ERROR_IMAGE
        Episodes = A_Title = "api_error⚠️"
        return A_PIC, A_Title, Episodes

    data = response.json()["data"]
    anime = data["Media"]
    if not anime:
        A_PIC = "https://te.legra.ph/file/3a603811e9275a9edd593.jpg"
        Episodes = A_Title = "not_found⚠️"
        return A_PIC, A_Title, Episodes

    A_Title = anime["title"]["english"] or anime["title"]["romaji"]
    Episodes = anime["episodes"]
    A_PIC = anime["bannerImage"]
    return A_PIC, A_Title, Episodes
        
        
async def channel_post_anime_info(anime_id: int):
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
        E_title=J_title=Format=episodes=status=average_score=Igenres=studio=duration=season="api_error⚠️"
        MSG_img = ERROR_IMAGE
        return E_title, J_title, MSG_img, Format, episodes, status, average_score, Igenres, studio, duration, season

    data = response.json()["data"]
    anime = data["Media"]
    if not anime:
        E_title=J_title=Format=episodes=status=average_score=Igenres=studio=duration=season="not_found⚠️"
        MSG_img = NOani_IMAGE
        return E_title, J_title, MSG_img, Format, episodes, status, average_score, Igenres, studio, duration, season

    E_title = anime["title"]["english"] or "➖"
    J_title = anime["title"]["romaji"] or "➖"
    Format = anime["format"]
    episodes = anime["episodes"]
    status = anime["status"]
    average_score = anime["averageScore"]
    genres = anime["genres"]
    Igenres = ", ".join([f"<i>{genre}</i> " for genre in genres])
    if "studios" in anime and anime["studios"] and "edges" in anime["studios"] and anime["studios"]["edges"] and len(anime["studios"]["edges"]) > 0 and "node" in anime["studios"]["edges"][0] and anime["studios"]["edges"][0]["node"] and "name" in anime["studios"]["edges"][0]["node"]:
        studio = anime["studios"]["edges"][0]["node"]["name"]
    else:
        studio = "unknown"
    duration = f"{anime['duration']} mins" if anime['duration'] else ""
    season = f"{anime['season']} {anime['seasonYear']}" if anime['season'] else ""
    MSG_img = f"https://img.anili.st/media/{anime_id}" 

    return E_title, J_title, MSG_img, Format, episodes, status, average_score, Igenres, studio, duration, season
        
        
async def only_banner_image(anime_id: int):
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
            studios(isMain: true) {
                edges {
                    node {
                        name
                    }
                }
            }
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
        msg_caption = "<b>FAILED TO GET ANIME INFO</b>\nTry Again, if problem persists contact me trough: @Maid_Robot"
        banner_pic = cover_pic = ERROR_IMAGE
        return

    data = response.json()["data"]
    anime = data["Media"]
    if not anime:
        msg_caption = f"No anime found with the ID '{anime_id}'.\n Did you fuck up the number after command?"
        banner_pic = cover_pic = NOani_IMAGE
        return

    cover_pic = anime["coverImage"]["extraLarge"]
    banner_pic = anime["bannerImage"]
    msg_caption = """
┏━━━━━━━━━━━━━━━━━━━━━━━
┣ʀᴇꜱᴏʟᴜᴛɪᴏɴ:
┣ᴀᴜᴅɪᴏ: {}
┣ꜱᴜʙᴛɪᴛʟᴇ: {}
┗━━━━━━━━━━━━━━━━━━━━━━━
"""
    return banner_pic, cover_pic, msg_caption



async def get_full_anime_info(anime_id: int):
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
        F_BOOL = False
        first_message = "<b>FAILED TO GET ANIME INFO</b>"
        message_text = "Try Again, if problem persists contact me trough: @Maid_Robot"
        trailer_url = site_url = "https://t.me/AnimeRobots"
        cover_url = banner_url = title_img = ERROR_IMAGE
        return F_BOOL, first_message, message_text, cover_url, banner_url, title_img, trailer_url, site_url

    data = response.json()["data"]
    anime = data["Media"]
    if not anime:
        F_BOOL = False
        first_message = f"<b>NO ANIME FOUND WITH GIVEN ID '{anime_id}'."
        message_text = "Try Searching Again Properly or Get Title From Anilist.co"
        trailer_url = site_url = "https://t.me/AnimeRobots"
        cover_url = banner_url = title_img = NOani_IMAGE
        return F_BOOL, first_message, message_text, cover_url, banner_url, title_img, trailer_url, site_url

    title = anime["title"]["english"] or anime["title"]["romaji"]
    cover_url = anime["coverImage"]["extraLarge"]
    banner_url = anime["bannerImage"]
    description = anime["description"]
    Format = anime["format"]
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
    title_img = f"https://img.anili.st/media/{anime_id}"

    first_message = f"{title}\n\n{description}"
    
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
    message_text += f"ꜰᴏʀᴍᴀᴛ: <b>{Format}</b>\n"
    message_text += f"ᴘᴏᴘᴜʟᴀʀɪᴛʏ: <b>{popularity}</b>\n"
    message_text += f"ꜱᴛᴀᴛᴜꜱ: <b>{status}</b>\n"
    message_text += f"ʀᴇʟᴇᴀꜱᴇᴅ: <b>{season}</b>\n"
    message_text += f"ꜱᴛᴀʀᴛᴇᴅ: <b>{start_date}</b>\n"
    message_text += f"ᴇɴᴅᴇᴅ: <b>{end_date}</b>\n"
    F_BOOL = True
    return F_BOOL, first_message, message_text, cover_url, banner_url, title_img, trailer_url, site_url
    

        
        
        
        
        
        
        
        
        
        
        
        
        

