import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, OWNER, START_MSG, PROTECT_CONTENT, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, Vid_Random, Gif_Random, ERR_TOPIC_ID, REQUEST_GC, USER_LOG_CHANNEL
from helper_func import encode, decode, get_messages, sub_PUB_Sc, sub_PUB_Dc, sub_BOT_c, sub_GC, FSCMD
from database.database import add_user, del_user, full_userbase, present_user
from database.inline import START_B, ERROR_BUTTON, AllFSCB
from database.user_stats import add_user_stats, add_user_stats, update_DL, del_user_stats, present_user_stats

USER_LOG_TXT = """
🟢 #New_User

👤 {}
🔗 @{}
🆔 <code>{}</code>  #id{}
"""
async def Log_inl_but(id: str):
    LB = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("USER LINK", user_id=id)
            ]
        ]
    )   
    return LB


@Bot.on_message(filters.command('start') & filters.private & sub_PUB_Dc & sub_PUB_Sc & sub_GC & sub_BOT_c)
async def start_command(client , message: Message):
    id = message.from_user.id
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            await message.reply_text("Some Error Occured, Please Reort Bot Onwer", reply_markup=ERROR_BUTTON)
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!", reply_markup=ERROR_BUTTON)
            return

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if msg.reply_markup and isinstance(msg.reply_markup, InlineKeyboardMarkup):
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(1)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
            except:
                await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️Start CMD-PVT Error\nWhile Sending Anime:-\nString= {base64_string} \n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
        try:
            await update_DL(id)
        except Exception as e:
            await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️While Update_DL IN pvt start\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
        return
    else:
        try:
  
            FINAL_VID = await Vid_Random()
            await message.reply_video(
                video = FINAL_VID,
                caption = START_MSG.format(message.from_user.mention),
               reply_markup = START_B,
            )
            if not await present_user(id):
                await add_user(id)
                try:
                    LB = await Log_inl_but(id)
                    await client.send_message(chat_id=USER_LOG_CHANNEL, text=USER_LOG_TXT.format(message.from_user.mention, message.from_user.username, id, id), reply_markup=LB)
                except:
                    await client.send_message(chat_id=USER_LOG_CHANNEL, text=USER_LOG_TXT.format(message.from_user.mention, message.from_user.username, id, id))
                    pass 
            if not await present_user_stats(id):
                await add_user_stats(id)
        except Exception as e:
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Start CMD-PVT Error\nwhile sending final Msg\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
        return
    
#=====================================================================================##

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##
from req import get_cmd, fs_allc_start


@Bot.on_message(filters.private & ~sub_PUB_Dc & ~sub_PUB_Sc & ~sub_GC & ~sub_BOT_c)
async def not_joined(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
            LB = await Log_inl_but(id)
            await client.send_message(chat_id=USER_LOG_CHANNEL, text=USER_LOG_TXT.format(message.from_user.mention, message.from_user.username, id, id), reply_markup=LB)
        except Exception as e:
            await client.send_message(chat_id=USER_LOG_CHANNEL, text=USER_LOG_TXT.format(message.from_user.mention, message.from_user.username, id, id))
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Start CMD-PVT Error\nwhile Adding User To DB\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
            pass

    buttons, FORCE_MSG = await fs_allc_start(filter, client, message)

    try:
        buttons.append(
            [
                InlineKeyboardButton(text = '♻️ 𝘾𝙇𝙄𝘾𝙆 𝙏𝙊 𝙍𝙀-𝙊𝙋𝙀𝙉 𝙎𝘼𝙈𝙀 𝘼𝙉𝙄𝙈𝙀 𝙇𝙄𝙉𝙆 ♻️', url = f"https://t.me/{client.username}?start={message.command[1]}")
            ]
        )
    except IndexError:
        pass
    
    try:
        FINAL_GIF = await Gif_Random()
        await message.reply_animation(animation=FINAL_GIF, caption=FORCE_MSG, reply_markup = InlineKeyboardMarkup(buttons))
    except Exception as e:
        await message.reply_text("An Error Occurred, Try Again\nIf Problem persist Contact owner🛂", reply_markup=ERROR_BUTTON)
        await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️Start Force SUB CMD-PVT Error\nwhile sending final Msg\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    if not await present_user_stats(id):
        await add_user_stats(id)
    

@Bot.on_message(get_cmd('channels'))
async def mychannelstats(client: Client, message: Message):
    id = message.from_user.id
    buttons, FORCE_MSG = await fs_allc_start(filter, client, message)
    try:
        FINAL_GIF = await Gif_Random()
        await message.reply_animation(animation=FINAL_GIF, caption=FORCE_MSG,  reply_markup=AllFSCB)
    except Exception as e:
        await client.send_message(chat_id=REQUEST_GC, text=f"⚠️ channels CMD-PVT Error\n\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

   
@Bot.on_message(get_cmd('anicastpvt') & filters.user(OWNER))
async def send_text_pvt(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("🦋")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                await del_user_stats(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""
╔══════════════════════╗
║ 𝘽𝙍𝙊𝘼𝘿𝘾𝘼𝙎𝙏 𝙎𝙏𝘼𝙏𝙎 📡
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
╠> @AnimeDL_Robot
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
╠╼👤 <b>ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ: {total} </b>
╠✅ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟ: <b>{successful} </b>
╠🚫ʙʟᴏᴄᴋᴇᴅ: <b>{blocked}</b>
║
╠💀ᴅᴇʟᴇᴛᴇᴅ: <b>{deleted}</b>   ⚠️ᴇʀʀᴏʀ: <b>{unsuccessful}</b>
║▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
╚══════════════════════╝
"""     
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
