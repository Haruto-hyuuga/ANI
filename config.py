import os
import logging
from logging.handlers import RotatingFileHandler


# raiden
#TG_BOT_TOKEN = "5844274164:AAHGFMBKEIcoUBS5uPekGAtag7BBaLi5GQI"
# yae miko
TG_BOT_TOKEN = "5930523466:AAGPG1MSNMOZ6icw6O2y_6E_Zi3OvBDYP64"
#
#TG_BOT_TOKEN = "5384960204:AAF45AwUFQtTYG7OhjFpwI937KSbr6V7ofY"


APP_ID = 12585681
API_HASH = "7741e8a55a0b5174548c52a374ab94b8"
BOTUSERNAME = "AnimeDL_Robot"



#DATABASE CHANNEL
CHANNEL_ID = -1001859794315
CREATOR_GC = -1001671956585

DB_URI = "mongodb+srv://vagil76793:cO7oFNJzbCksNKkK@cluster0.cvj8wvf.mongodb.net/?retryWrites=true&w=majority"
SUB_ANIME_DB = "mongodb+srv://lejah82077:7hDBz80lC4sKb7EN@cluster0.jo83ynu.mongodb.net/?retryWrites=true&w=majority"
DUB_ANIME_DB = "mongodb+srv://tasesey566:r7bEdOZnnE2lgL7H@cluster0.i17yfwi.mongodb.net/?retryWrites=true&w=majority"


FS_PUBLIC_CHANNEL = -1001741236715
FS_PUBLIC_TEXT = "Join Main Cahnnel"
PUBLIC_C_url = "https://t.me/ANIME_DOWNLOADS_SUB"
MC_gif = "https://telegra.ph/file/34b19d8ba3c07f04826f8.mp4"

FS_BOT_CHANNEL = -1001867076149
FS_BOT_TEXT = "Join  Bot Channel"
BOT_C_url = "https://t.me/AnimeRobots"
BC_gif = "https://telegra.ph/file/744efc86967a9291dee23.mp4"

FS_GROUP = -1001671956585
FS_GROUP_text = "Join Group"
GROUP_url = "https://t.me/AnimeCommunityChat"
GC_gif = "https://telegra.ph/file/307aecec6325f2147306e.mp4"

contributor_graph = "https://t.me/AnimeCommunityChat"
memes_channel = "https://t.me/Anime_Hub_Fz"
The_Other_Channel = "https://t.me/ANIME_DOWNLOADS_DUB"


FORCE_MSG = """
<b><u>Hey There fellow Anime Lover!</u></b>
<b>To Use This Bot You Must Join My Channels and Group, Since This Is A Free Service But It Takes Heck Lot Of Work~</b>

|• <i>Join Anime Channel To Get Links Of Series You'll Download.</i>
|• <i>Join Bot Owner Channel To Get Updates On Bot Status.</i>
|• <i>Join Group To Recommend Anime or Report Malfunction.</i>
"""

START_MSG = """
Welcome {}!

♡ Click On About To Get Info About Bot.
♡ Click on Request To Suggest Anime Which We Yet Haven't Added To Bot or Channels.
⁠♡ Click On Channels, Go Through Link Search For Anine You're intrested In Then Start The Bot vai that link.
"""

ABOUT_TEXT = """
<b>COMMANDS LIST:</b>
〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️

/find or /search  'ANIME TITLE'
<i>Use this command to get list of anime series that matches your search query and get download id</i>

/anime or /download 'ANIME ID'
<i>Use this command to get anime download link from channels</i>

/anime_info or /info 'ANIME ID'
<i>Use this command to get detailed anime info trailer and many more</i>
"""

REQUEST_TEXT = """
<b>To Request Anime Series/Movies:</b>
|- <i>Use Command:</i> <code>/download id</code>
|- <i>Read ABOUT to get more info on this command.</i>
|- <i>Then Reply To That Anime Series By Command:</i> /request or #request

<b>Another Method Of requesting Anime Is: Send Link of anime From</b> anilist.co/search/anime <b>directy here to bot.</b>
<b>Or You Can Simply Message Bot About Requesting Anime, Chances Are Less That we'll Respond In This Method</b>
"""



ALL_CHANNEL_TEXT = """
<b>GIVEN BELOW ARE TWO DIFFERENT CHANNELS:</b>

⛩️𝑪𝒉𝒂𝒏𝒏𝒆𝒍 𝟏: @ANIME_DOWNLOADS_SUB
ᴀᴜᴅɪᴏ: <b>Japanese 🇯🇵</b>
ꜱᴜʙᴛɪᴛʟᴇꜱ: <b>English</b>
ʀᴇꜱᴏʟᴜᴛɪᴏɴ: <b>480p | 720p | 1080p</b>


🗺️𝑪𝒉𝒂𝒏𝒏𝒆𝒍 𝟐: @ANIME_DOWNLOADS_DUB 
ᴀᴜᴅɪᴏ: <b>Japanese + English</b> 🇯🇵🇬🇧
ꜱᴜʙᴛɪᴛʟᴇꜱ: <b>English + Sign&Songs</b>
ʀᴇꜱᴏʟᴜᴛɪᴏɴ: <b>480p | 720p | 1080p</b>
"""

CREDIT_TEXT = """
This Bot Will Make it Easy To Search anime and Get Download Links.
Made by: @MaidShiro with 💕

<b>DON'T FORGET TO READ LIST OF CONTRIBUTORS WHO MADE THIS BOT SUCCESSFUL ♥️⚡</b>
"""

PORT = os.environ.get("PORT", "8080")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))




ADMINS = []
if not 1497264683 in ADMINS:  #Shiro
  ADMINS.append(1497264683)
if not 5024928504 in ADMINS:  # mei
  ADMINS.append(5024928504)
if not 1302714537 in ADMINS:  # DSp
  ADMINS.append(1302714537)
if not 1225219091 in ADMINS:  # argha
  ADMINS.append(1225219091)
if not 5296520170 in ADMINS:  # emi
  ADMINS.append(5296520170)

OWNER = 1497264683

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'
LOG_FILE_NAME = "filesharingbot.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
