import httpx
from database.inline import ERROR_BUTTON, ANIME_RESULT_B, NOani_BUTTON



ERROR_IMAGE = ""
NOani_IMAGE = ""
NO_banner_IMG = ""

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
        message_text = f"<b>NO ANIME FOUND FOR PROVIDED QUERY '{anime_name}'.</b>\n\nTry Searching On Our Channel or Anilist and Copy Paste Title")
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

