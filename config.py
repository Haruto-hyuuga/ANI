import os
import logging
from logging.handlers import RotatingFileHandler
import random 

#BOT 1
#BOT_ID = 6116589740
#BOTUSERNAME = "AnimeDL_Robot"
#TG_BOT_TOKEN = "6116589740:AAEZ4AARouWW0nFsN7YfffeqOIU3sCwrxW4"
#USER_LOG_CHANNEL = -1001909557377
#DB_URI = "mongodb+srv://vagil76793:cO7oFNJzbCksNKkK@cluster0.cvj8wvf.mongodb.net/?retryWrites=true&w=majority"

#BOT 2
BOT_ID = 6286463449
BOTUSERNAME = "AnimeDownLoader_Robot"
TG_BOT_TOKEN = "6286463449:AAGThxmuOUis9HN_IYMCvZdcwjKeOOw3U7o"
USER_LOG_CHANNEL = -1001925844286
DB_URI = ""


APP_ID = 12585681
API_HASH = "7741e8a55a0b5174548c52a374ab94b8"
#DATABASE CHANNEL
CHANNEL_ID = -1001803639446
#APROVAL URL OF DB CHANNEL
DB_C_Pvturl = "https://t.me/+gwY34XgAgHgyNzI1"

REQUEST_GC = -1001903277336
Bot_Start_Topic = 28
ERR_TOPIC_ID = 50
REQ_TOPIC_ID = 49
USER_TOPIC_ID = 152


SUB_ANIME_DB = "mongodb+srv://lejah82077:7hDBz80lC4sKb7EN@cluster0.jo83ynu.mongodb.net/?retryWrites=true&w=majority"
DUB_ANIME_DB = "mongodb+srv://tasesey566:r7bEdOZnnE2lgL7H@cluster0.i17yfwi.mongodb.net/?retryWrites=true&w=majority"
USER_STATS_DB = "mongodb+srv://koneson986:IeFLbCQq60A5Hsmo@cluster0.68ublv1.mongodb.net/?retryWrites=true&w=majority"


SUB_CHANNEL = -1001741236715
Sub_C_url = "https://t.me/ANIME_DOWNLOADS_SUB"

DUB_CHANNEL = -1001916486716
Dub_C_url = "https://t.me/ANIME_DOWNLOADS_DUB"

FS_BOT_CHANNEL = -1001867076149
BOT_C_url = "https://t.me/AnimeRobots/24"

FS_GROUP = -1001525634215
FS_GROUP_text = "Join Group"
GROUP_url = "https://t.me/AnimeCommunityChat"

contributor_graph = "https://graph.org/ANIME-DOWNLOADER-BOT-HELPERS-04-21"
memes_channel = "https://t.me/Anime_Hub_Fz"
 

async def Vid_Random():
    SC_vid = "https://telegra.ph/file/ca4666765cafb7663de79.mp4"
    DC_vid = "https://telegra.ph/file/3552a5b596fa979b75fd6.mp4"
    GC_vid = "https://telegra.ph/file/662d9619f6db0aea49665.mp4"
    BC_vid = "https://telegra.ph/file/c5c0a57ac043c34f25b22.mp4"
    SC2_vid = "https://telegra.ph/file/ca4666765cafb7663de79.mp4"
    DC2_vid = "https://telegra.ph/file/3552a5b596fa979b75fd6.mp4"
    R_V = [SC_vid, DC_vid, GC_vid, BC_vid, SC2_vid, DC2_vid]
    FINAL_VID = random.choice(R_V)
    return FINAL_VID

async def Gif_Random():
    SC_gif = "https://telegra.ph/file/a16b17a0684fe097c0736.mp4"
    DC_gif = "https://telegra.ph/file/0029fb4f8b8964c59eb05.mp4"
    GC_gif = "https://telegra.ph/file/1980bb177042267d7f65a.mp4"
    BC_gif = "https://telegra.ph/file/51b98e9c9d6e76dc5caf1.mp4"
    R_G = [SC_gif, DC_gif, GC_gif, BC_gif]
    FINAL_GIF = random.choice(R_G)
    return FINAL_GIF

async def R_Banner_Pic():
    P1 = "https://telegra.ph/file/35651d60c717bd762a0b7.jpg"
    P2 = "https://telegra.ph/file/ab341bb7e4bcb3428a581.jpg"
    P3 = "https://telegra.ph/file/22cb65f51f31e70ae0d46.jpg"
    P4 = "https://telegra.ph/file/22720f01db899c0a2aff7.jpg"
    P5 = "https://telegra.ph/file/ab9195b35a195020a525e.jpg"
    P = [P1, P2, P3, P4, P5]
    M_banner_Pic = random.choice(P)
    return M_banner_Pic


PVT_FS_TXT = """
~It looks like you haven't started me in private yet...
<i>To use these commands, please start me in private first, nya~! 
Don't worry, I won't bite!</i>
"""
PVT_FS_VID = "https://telegra.ph/file/a958958b6b4877daaee41.mp4"

O_PVT_FS_TXT = """
<b>Umm... Excuse me, senpai!</b>
Just a friendly reminder that these commands are meant to be used in private chats with me to prevent any pesky spam in our lovely groups.
"""
O_PVT_FS_PIC = "https://telegra.ph/file/1bca5f24a5af913e591b9.jpg"



FORCE_MSG = """
<b><u>Hey There fellow Anime Lover!</u></b>
<b>To Use This Bot You Must Join My Channels and Group, Since This Is A Free Service But It Takes Heck Lot Of Work~</b>

"""

START_MSG = """
Welcome {} ♡!
<b>Let's embark on an exciting journey together and discover all the amazing stories and characters anime has to offer!</b>

<i>Use buttons below to explore all my features and commands and  thier usage.</i>
"""



ABOUT_TEXT = """
<b>COMMANDS LIST:</b>
〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️

/anime or /download <b>𝙰𝙽𝙸𝙼𝙴 𝙽𝙰𝙼𝙴 / 𝙸𝙳</b>
<i>Use this command to get anime download link from channels</i>

/find or /search  <b>𝙰𝙽𝙸𝙼𝙴 𝙽𝙰𝙼𝙴</b>
<i>search for anime that best matches your search query</i>

/list or /fullsearch <b>𝙰𝙽𝙸𝙼𝙴 𝙽𝙰𝙼𝙴</b>
<i>search for all anime that matches your search query</i>

/recommend 
<i>Use this command to get random anime recommendation, mention</i>
<i>type:</i> <code>/recommend dub/sub</code> to filter results

/anime_info or /ainfo <b>𝙰𝙽𝙸𝙼𝙴 𝙸𝙳</b>
<i>Use this command to get detailed anime info trailer and many more</i>

/channels
<i>Use this command to get all chennals links</i>

/stats 
<i>Check Your Stats/Activity on Bot</i>
"""

REQUEST_TEXT = """
<u>𝗧𝗼 𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗔𝗻𝗶𝗺𝗲 𝗦𝗲𝗿𝗶𝗲𝘀/𝗠𝗼𝘃𝗶𝗲𝘀:</u>
|• <i>Use Command:</i> <code>/download or /search</code>
|• <i>then click on Request Button on message</i>
OR
|• <i>Use Command:</i> /request (𝚛𝚎𝚙𝚕𝚢 𝚝𝚘 𝚜𝚎𝚊𝚛𝚌𝚑𝚎𝚍 𝚊𝚗𝚒𝚖𝚎)
|• <i>it will send request to add that anime</i>

<u>𝗧𝗼 𝗿𝗲𝗽𝗼𝗿𝘁 𝗮𝗻𝘆 𝗲𝗿𝗿𝗼𝗿 𝗶𝗻 𝗯𝗼𝘁 𝗼𝗿 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗳𝗶𝗹𝗲𝘀</u>
|• <i>Use Command:</i> /report
|• <i>Reply to bot message</i>
|• <i>write error after command</i>
"""



ALL_CHANNEL_TEXT = """
<b>GIVEN BELOW ARE TWO DIFFERENT CHANNELS:</b>

⛩️𝑪𝒉𝒂𝒏𝒏𝒆𝒍 𝟏: @ANIME_DOWNLOADS_SUB
ᴀᴜᴅɪᴏ: <b>Japanese 🇯🇵</b>
ꜱᴜʙᴛɪᴛʟᴇꜱ: <b>English</b>
ʀᴇꜱᴏʟᴜᴛɪᴏɴ: <b>720p | 1080p</b>


🗺️𝑪𝒉𝒂𝒏𝒏𝒆𝒍 𝟐: @ANIME_DOWNLOADS_DUB 
ᴀᴜᴅɪᴏ: <b>English</b> 🇬🇧
ꜱᴜʙᴛɪᴛʟᴇꜱ: <b>English + Sign&Songs</b>
ʀᴇꜱᴏʟᴜᴛɪᴏɴ: <b>720p | 1080p</b>
"""

DISCLAIMER_TXT = """
<u>𝗗𝗜𝗦𝗖𝗟𝗔𝗜𝗠𝗘𝗥 ⚠️</u>

<b>Our bot and channels are not affiliated with any anime studios, licensors, or distributors. We do not own any of the content that we provide, and we do not host any files on our servers. All content is provided through third-party sources and is intended for personal use only.</b>

<b>We do not condone piracy or illegal distribution of copyrighted materials. As a user of our bot and channels, it is your responsibility to ensure that your use of the content complies with all applicable laws and regulations. Additionally, please note that we do not provide Hentai content through this bot, refrain from requesting those.</b> 

<b>By using our bot and channels,{} you agree to these terms and conditions. </b>
"""


CREDIT_TEXT = """
𝑻𝒉𝒊𝒔 𝑩𝑶𝑻 𝒘𝒊𝒍𝒍 𝒎𝒂𝒌𝒆 𝒊𝒕 𝒆𝒂𝒔𝒚 𝒕𝒐 𝑫𝒊𝒔𝒄𝒐𝒗𝒆𝒓, 𝑹𝒆𝒒𝒖𝒆𝒔𝒕 𝒂𝒏𝒅 𝑫𝒐𝒘𝒏𝒍𝒐𝒂𝒅 𝒚𝒐𝒖𝒓 𝒇𝒂𝒗𝒐𝒓𝒊𝒕𝒆 𝒂𝒏𝒊𝒎𝒆 𝒆𝒇𝒇𝒐𝒓𝒕𝒍𝒆𝒔𝒔𝒍𝒚.
ᴠᴇʀꜱɪᴏɴ: CC 2.0

<b>DON'T FORGET TO READ LIST OF CONTRIBUTORS WHO MADE THIS BOT SUCCESSFUL</b>
"""


ALLCMD_FS_PIC = "https://telegra.ph/file/028f63b6ac6473ecab0a5.jpg"
ALLCMD_FS_TXT = """
𝙊𝙝 𝙔𝙤𝙪 𝘿𝙪𝙢𝙗 𝘿𝙪𝙢𝙗 𝘾𝙝𝙞𝙡𝙙, 𝙔𝙤𝙪 𝘾𝙖𝙣'𝙩 𝙐𝙨𝙚 𝘼𝙣𝙮 𝘾𝙤𝙢𝙢𝙖𝙣𝙙 𝙊𝙛 𝙏𝙝𝙞𝙨 𝘽𝙤𝙩 𝙐𝙣𝙩𝙞𝙡 𝙔𝙤𝙪 𝙅𝙤𝙞𝙣 𝘼𝙡𝙡 𝙊𝙪𝙧 𝘾𝙃𝘼𝙉𝙉𝙀𝙇𝙨 𝙖𝙣𝙙 𝙂𝙍𝙊𝙐𝙋.

<b>ᴜꜱᴇ ᴄᴏᴍᴍᴀɴᴅ: /channels ᴛᴏ ᴄʜᴇᴄᴋ ᴡʜɪᴄʜ ᴄʜᴀɴɴᴇʟ ᴏʀ ɢʀᴏᴜᴘ ʏᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ.</b>
<b>ᴏʀ ʀᴇꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ʙʏ: /start </b>
"""


PORT = 8080
TG_BOT_WORKERS = 25


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
if not 5541041517 in ADMINS:  # note
  ADMINS.append(5541041517)
if not 5329765587 in ADMINS:  # schwi
  ADMINS.append(5329765587)
if not 5908829591 in ADMINS:  # argha 2
  ADMINS.append(5908829591)
  



OWNER = 1497264683

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", True) == 'True'
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
