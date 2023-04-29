
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, CREATOR_GC
from helper_func import encode, AC_CMD

@Bot.on_message(filters.chat(CREATOR_GC) & filters.user(ADMINS) & ~filters.command(AC_CMD))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        await reply_text.edit_text(f"AN ERROR: \n{e}")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview = True)

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)



@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):


"""

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
"""

"""
from config import SUB_CHANNEL, DUB_CHANNEL, Sub_C_url, Dub_C_url

@Bot.on_message(filters.channel & filters.incoming & filters.chat(SUB_CHANNEL))
async def sub_post_link_gc(client, message: Message):
    P_id = message.id
    Link = f"{Sub_C_url}/{P_id}"
    await client.send_message(chat_id=CREATOR_GC, text=Link)
    

@Bot.on_message(filters.channel & filters.incoming & filters.chat(DUB_CHANNEL))
async def dub_post_link_gc(client, message: Message):
    P_id = message.id
    Link = f"{Dub_C_url}/{P_id}"
    await client.send_message(chat_id=CREATOR_GC, text=Link)
    
"""





