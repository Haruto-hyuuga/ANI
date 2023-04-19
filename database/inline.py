from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PUBLIC_C_url, BOT_C_url, GROUP_url, contributor_graph, memes_channel, The_Other_Channel
from config import BOTUSERNAME, OWNER


START_B = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("COMMANDS", callback_data="About_Bot"),
            InlineKeyboardButton("CHANNELs", callback_data="DL_Channels")
        ],
        [
            InlineKeyboardButton("REQUEST ANIME", callback_data="A_requests"),
            InlineKeyboardButton("CREDITs", callback_data="Credits_a")
        ],
        [
            InlineKeyboardButton("GROUP CHAT", url=GROUP_url),
        ]
    ]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("BACK", callback_data="BACK_HOME"),
            InlineKeyboardButton("GIVE REVIEW ⭐", url=BOT_C_url)
        ]
    ]
)

CHANNELS_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("English-SUB | Original Audio", url = PUBLIC_C_url),
        ],
        [
            InlineKeyboardButton("English-SUB | English-DUB + Japanese", url = The_Other_Channel),
        ],
        [
            InlineKeyboardButton("BACK", callback_data="BACK_HOME"),
            InlineKeyboardButton("ANIMEMES", url=memes_channel)
        ]
    ]
)

REQUEST_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("BACK", callback_data="BACK_HOME")
        ]
    ]
)

ERROR_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("CLOSE", callback_data="close"),
            InlineKeyboardButton("REPORT ISSUE", url = "https://t.me/Maid_Robot")
        ]
    ]
)

AllFSCB = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Anime Channel", url = PUBLIC_C_url),
            InlineKeyboardButton("Bot Channel", url = BOT_C_url)
        ],
        [
            InlineKeyboardButton("Anime Group Chat", url = GROUP_url)
        ]
    ]
)
ANIME_RESULT_B = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("DOWNLOAD", callback_data="anime_download_popup"),
            InlineKeyboardButton("NOT FOUND", callback_data="anime_notfound_popup")
        ]
    ]
)
CREDIT_B = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Developer", user_id=OWNER),
            InlineKeyboardButton("More Bots", url=BOT_C_url)
        ],
        [
            InlineKeyboardButton("♥️CHANNEL CONTRIBUTORS♥️", url=contributor_graph)
        ],
        [
            InlineKeyboardButton("BACK", callback_data="BACK_HOME")
        ]
    ]
)
