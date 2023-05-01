from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Sub_C_url, BOT_C_url, GROUP_url, contributor_graph, memes_channel, Dub_C_url, DB_C_Pvturl
from config import BOTUSERNAME, OWNER


START_B = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦", callback_data="About_Bot"),
            InlineKeyboardButton("𝗖𝗛𝗔𝗡𝗡𝗘𝗟𝘀", callback_data="DL_Channels")
        ],
        [
            InlineKeyboardButton("𝗥𝗘𝗤𝗨𝗘𝗦𝗧 𝗔𝗡𝗜𝗠𝗘", callback_data="A_requests"),
            InlineKeyboardButton("𝗖𝗥𝗘𝗗𝗜𝗧𝘀", callback_data="Credits_a")
        ],
        [
            InlineKeyboardButton("𝗔𝗗𝗗 𝗕𝗢𝗧 𝗧𝗢 𝗬𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣", url=f"https://t.me/{BOTUSERNAME}?startgroup=true"),
        ]
    ]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("𝗕𝗔𝗖𝗞", callback_data="BACK_HOME"),
            InlineKeyboardButton("𝗚𝗜𝗩𝗘 𝗥𝗘𝗩𝗜𝗘𝗪 ⭐", url=BOT_C_url)
        ]
    ]
)

CHANNELS_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("𝗝𝗮𝗽𝗮𝗻𝗲𝘀𝗲 𝗦𝗨𝗕 (𝟰𝟴𝟬𝗽-𝟳𝟮𝟬𝗽-𝟭𝟬𝟴𝟬𝗽 | 🔊:🇯🇵)", url = Sub_C_url),
        ],
        [
            InlineKeyboardButton("𝗘𝗻𝗴𝗹𝗶𝘀𝗵 𝗗𝗨𝗕 (𝟰𝟴𝟬𝗽-𝟳𝟮𝟬𝗽-𝟭𝟬𝟴𝟬𝗽 | 🔊:🇯🇵🇬🇧)", url = Dub_C_url),
        ],
        [
            InlineKeyboardButton("𝗕𝗔𝗖𝗞", callback_data="BACK_HOME"),
            InlineKeyboardButton("𝗠𝗲𝗠𝗲𝗦", url=memes_channel)
        ]
    ]
)

REQUEST_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("𝗕𝗔𝗖𝗞", callback_data="BACK_HOME")
        ]
    ]
)

ERROR_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🗑️ 𝗖𝗟𝗢𝗦𝗘", callback_data="close"),
            InlineKeyboardButton("𝗥𝗲𝗽𝗼𝗿𝘁 𝗘𝗿𝗿𝗼𝗿 ⛑️", url = "https://t.me/Maid_Robot")
        ]
    ]
)

AllFSCB = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("𝗔𝗻𝗶𝗺𝗲 𝗦𝗨𝗕 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🇯🇵", url = Sub_C_url),
            InlineKeyboardButton("𝗔𝗻𝗶𝗺𝗲 𝗗𝗨𝗕 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🇬🇧", url = Dub_C_url)
        ],
        [
            InlineKeyboardButton("𝗕𝗼𝘁 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", url = BOT_C_url),
            InlineKeyboardButton("𝗖𝗛𝗔𝗧 𝗚𝗥𝗢𝗨𝗣", url = GROUP_url)
        ]
    ]
)
ANIME_RESULT_B = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("📥 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗", callback_data="anime_download_popup"),
            InlineKeyboardButton("ℹ️❔", callback_data="emoji_info_popup"),
            InlineKeyboardButton("𝗡𝗼𝘁 𝗜𝗻 𝗟𝗶𝘀𝘁 🔎", callback_data="anime_notfound_popup")
        ]
    ]
)
CREDIT_B = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", user_id=OWNER),
            InlineKeyboardButton("ʙᴏᴛ ꜱᴛᴀᴛᴜꜱ", url=BOT_C_url)
        ],
        [
            InlineKeyboardButton("♥️ 𝑪𝑯𝑨𝑵𝑵𝑬𝑳 𝑪𝑶𝑵𝑻𝑹𝑰𝑩𝑼𝑻𝑶𝑹𝑺 ♥️", url=contributor_graph)
        ],
        [
            InlineKeyboardButton("𝗕𝗔𝗖𝗞", callback_data="BACK_HOME")
        ]
    ]
)
BATCH_DBC_B = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("DB CHANNEL 📂", url=DB_C_Pvturl)
        ]
    ]
)

GO_BOTDM_B = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("GO TO PRIVATE CHAT 💚", url=f"https://t.me/{BOTUSERNAME}")
        ]
    ]
)

BOT_DM_B = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("💠 AUTHORISE 💠", url=f"https://t.me/{BOTUSERNAME}")
        ]
    ]
)

async def Ani_log_inline_f(UID: int, link: str) -> InlineKeyboardMarkup:
    ANI_LOG_BUT = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("USER🔗", user_id=UID),
                InlineKeyboardButton("POST🔗", url=link)
            ]
        ]
    )
    return ANI_LOG_BUT

async def Ani_log_group(link: str) -> InlineKeyboardMarkup:
    GC_LOG_BUT = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("CHAT LINK 💬🔗", url=link)
            ]
        ]
    )
    return GC_LOG_BUT

GC_START_B = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("➕ Add To Group", url = f"https://t.me/{BOTUSERNAME}?startgroup=true"),
            InlineKeyboardButton("Give Review 🌟", url = BOT_C_url)
        ]
    ]
)



async def user_close(UID: int) -> InlineKeyboardMarkup:
    USER_CLOSE = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🗑️ 𝗖𝗟𝗢𝗦𝗘", callback_data=f"FUclose_{UID}")
            ]
        ]
    )
    return USER_CLOSE

CLOSE_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🗑️ 𝗖𝗟𝗢𝗦𝗘", callback_data="close"),
        ]
    ]
)


NOani_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("𝗦𝗨𝗕 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", url = Sub_C_url),
            InlineKeyboardButton("𝗗𝗨𝗕 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", url = Dub_C_url)
        ],
        [
            InlineKeyboardButton("🗑️", callback_data="close"),
        ]
    ]
)

