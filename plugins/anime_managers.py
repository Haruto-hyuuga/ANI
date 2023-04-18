from bot import Bot
from database.anime_db import*
from pyrogram import Client, filters
from pyrogram.types import Message
from config import ADMINS, PUBLIC_C_url, The_Other_Channel 



@Bot.on_message(filters.command("addsub") & filters.user(ADMINS))
async def add_sub(client, message):
    if message.reply_to_message:
        link = message.reply_to_message.text
        if len(message.command) != 1:
            text = message.text.split(None, 1)[1]
            anime_id = int(text) 
            if not await present_sub_anime(anime_id):
                try:
                    await add_sub_anime(anime_id, link)
                    await message.reply_text(f"<b>ADDED!</b>\n\nID: <b>{anime_id}</b>\nLINK: {link}")
                except Exception as e:
                    await message.reply_text(f"An Error Occured//-\n\n{e}")
            else:
                dblink = await get_sub_anime(anime_id)
                await message.reply_text(f"<b>THIS ANIME ALREDY EXIST</b>\n\nID: <b>{anime_id}</b>\n<b>POST LINK:</b> {dblink}")
        else:
            await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /anime or /search")
    else:
        await message.reply_text(f"Bish Reply To Post Link From Channel:\n {PUBLIC_C_url}")
        
    
@Bot.on_message(filters.command("delsub") & filters.user(ADMINS))
async def add_sub(client, message):
    if len(message.command) != 1:
        text = message.text.split(None, 1)[1]
        anime_id = int(text) 
        if await present_sub_anime(anime_id):
            try:
                dblink = await get_sub_anime(anime_id)
                await del_sub_anime(anime_id)
                await message.reply_text(f"<b>DELETED!</b>\n\nID: <b>{anime_id}</b>\n<b>POST LINK:</b> {dblink}")
            except Exception as e:
                await message.reply_text(f"An Error Occured//-\n\n{e}")
        else:
            await message.reply_text(f"No Such Anime Was Inserted In DataBase With ID: {anime_id}")
    else:
        await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /anime or /search")
