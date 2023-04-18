import os
import asyncio
import random 
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, PROTECT_CONTENT, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, MC_gif, BC_gif, GC_gif
from config import FS_BOT_TEXT, FORCE_MSG, START_MSG, FS_PUBLIC_TEXT, FS_GROUP_text, PUBLIC_C_url, BOT_C_url, GROUP_url
from helper_func import encode, decode, get_messages, sub_PUB_c, sub_BOT_c, sub_GC
from database.database import add_user, del_user, full_userbase, present_user
from database.inline import START_B, ERROR_BUTTON


@Bot.on_message(filters.command('start') & filters.private & sub_PUB_c & sub_GC & sub_BOT_c)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
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

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
            except:
                pass
        return
    else:
        await message.reply_animation(
            animation = MC_gif,
            caption = START_MSG.format(message.from_user.mention),
           reply_markup = START_B,
        )
        return

    
#=====================================================================================##

WAIT_MSG = """⏳"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##
from helper_func import is_subscribed_PC, is_subscribed_BOT, is_subscribed_GROUP, F_AC_Gif, F_BC_Gif, F_GC_Gif
from database.inline import AllFSCB

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    update = message
    MC = await is_subscribed_PC(filter, client, update)
    BC = await is_subscribed_BOT(filter, client, update)
    GC = await is_subscribed_GROUP(filter, client, update)
    buttons = []
    FSGIF = random.choice([BC_gif, GC_gif])
    if MC == False:
        try:
            buttons.append(
                [
                    InlineKeyboardButton("Anime Download Channel", url = PUBLIC_C_url),
                ]
            )
        except IndexError:
            pass
    if BC == False:
        try:
            buttons.append(
                [
                    InlineKeyboardButton("Bot Updates Channel", url = BOT_C_url)
                ]
            )
        except IndexError:
            pass
    if GC == False:
        try:
            buttons.append(
                [
                    InlineKeyboardButton("Anime Group Chat", url = GROUP_url)
                ]
            )
        except IndexError:
            pass
    try:
        buttons.append(
            [
                InlineKeyboardButton(text = 'CLICK TO RE-OPEN SAME ANIME LINK', url = f"https://t.me/{client.username}?start={message.command[1]}")
            ]
        )
    except IndexError:
        pass
    C1T = await F_AC_Gif(MC)
    C2T = await F_BC_Gif(BC)
    C3T = await F_GC_Gif(GC)
    try:
        await message.reply_animation(animation=FSGIF, caption = f"{FORCE_MSG} \n\n{C1T}\n\n{C2T}\n\n{C3T}", reply_markup = InlineKeyboardMarkup(buttons))
    except:
        await message.reply_animation(animation=MC_gif, caption = f"{FORCE_MSG}\n\n{C1T}\n\n{C2T}\n\n{C3T}", reply_markup = AllFSCB)
    
   
@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")


@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
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
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
