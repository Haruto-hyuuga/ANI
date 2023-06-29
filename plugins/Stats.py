from bot import Bot
from pyrogram import filters
from req import get_cmd
from pyrogram.types import Message
from config import ADMINS
from database.anime_db import full_sub_Animebase
from database.anime_db import full_dub_Animebase
from database.database import full_userbase
from database.user_stats import get_user_stats
from database.req_Db import full_requestDB_DUB, full_requestDB_SUB
from database.inline import user_close
from req import search_user_id
    

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


@Bot.on_message(get_cmd('stats'))
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

























