from bot import Bot
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.inline import ERROR_BUTTON, ANIME_RESULT_B
from config import FS_GROUP, ALLCMD_FS_TXT, ALLCMD_FS_PIC, ERR_TOPIC_ID, REQUEST_GC

from helper_func import sub_PUB_Sc, sub_PUB_Dc, sub_BOT_c, sub_GC
from req import get_full_anime_info, channel_post_anime_info, search_find_anime_list, search_anime_list_by_Name, full_info_anime_list_by_Name, download_anime_buttons_db



@Bot.on_message(filters.command(["download", "anime"]) & sub_PUB_Dc & sub_PUB_Sc & sub_GC & sub_BOT_c & filters.private)
async def anime_info(client, message):
    UID = message.from_user.id
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Bruh you stoopid? <b>Mention Name of Anime after Command or Anime Id</b>\n<i>You can Also Try using Command:</i> /find ")
        return
    arg = args[1]
    if arg.isdigit():
        try:
            anime_id = int(arg)
        except (IndexError, ValueError):
            await message.reply_text(f"{message.from_user.mention}-san Please Don't Did you fuck With Anime Id.\nProvide A valid Anime Id")
            return

        E_title, J_title, MSG_img, Format, episodes, status, average_score, Igenres, studio, duration, season = await channel_post_anime_info(anime_id)
            
        message_text = f"""
🇬🇧: <b><u>{E_title}</u></b>
🇯🇵: <b><u>{J_title}</u></b>
━━━━━━━━━━━━━━━━━━━━━━━━━
ᴇᴘɪꜱᴏᴅᴇꜱ: <b>{episodes}</b>
ᴅᴜʀᴀᴛɪᴏɴ: <b>{duration}</b>
ᴛʏᴘᴇ: <b>{Format}</b>
ꜱᴛᴀᴛᴜꜱ: <b>{status}</b>
ɢᴇɴʀᴇꜱ: <i>{Igenres}</i>

"""
        new_message_text, buttons = await download_anime_buttons_db(anime_id, message_text, client, UID)

        try:
            await message.reply_photo(MSG_img, caption=new_message_text, reply_markup=InlineKeyboardMarkup(buttons))
        except Exception as e:
            await message.reply_text("An Error Occurred, Try Again\nIf Problem persist Contact me 🛂", reply_markup=ERROR_BUTTON)
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Anime/Download CMD-PVT Error\nwhile sending final message\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    else:
        anime_name = " ".join(args[1:])
        message_text, message_button, message_photo = await search_anime_list_by_Name(anime_name, UID)
        try:
            await message.reply_photo(message_photo, caption=message_text, reply_markup=message_button)
        except Exception as e:
            await message.reply_text("An Error Occurred, Try Again\nIf Problem persist Contact me 🛂", reply_markup=ERROR_BUTTON)
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Anime/Download CMD-PVT Error\nwhile sending final message\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)


            

@Bot.on_message(filters.command(["download", "anime"]) & filters.chat(FS_GROUP))
async def gcanimedlcmd(client, message):
    UID = message.from_user.id
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Bruh you stoopid? <b>Mention Name of Anime after Command or Anime Id</b>\n<i>You can Also Try using Command:</i> /find ")
        return
    arg = args[1]
    if arg.isdigit():
        try:
            anime_id = int(arg)
        except (IndexError, ValueError):
            await message.reply_text(f"{message.from_user.mention}-san Please Don't Did you fuck With Anime Id.\nProvide A valid Anime Id")
            return

        E_title, J_title, MSG_img, Format, episodes, status, average_score, Igenres, studio, duration, season = await channel_post_anime_info(anime_id)
            
        message_text = f"""
🇬🇧: <b><u>{E_title}</u></b>
🇯🇵: <b><u>{J_title}</u></b>
━━━━━━━━━━━━━━━━━━━━━━━━━
ᴇᴘɪꜱᴏᴅᴇꜱ: <b>{episodes}</b>
ᴅᴜʀᴀᴛɪᴏɴ: <b>{duration}</b>
ᴛʏᴘᴇ: <b>{Format}</b>
ꜱᴛᴀᴛᴜꜱ: <b>{status}</b>
ɢᴇɴʀᴇꜱ: <i>{Igenres}</i>

"""
        new_message_text, buttons = await download_anime_buttons_db(anime_id, message_text, client, UID)
    
        if message.reply_to_message:
            try:
                await message.reply_to_message.reply_photo(MSG_img, caption=new_message_text, reply_markup=InlineKeyboardMarkup(buttons))
            except Exception as e:
                await client.send_message(chat_id=REQUEST_GC, text=f"⚠️download/anime CMD-GC Error\nFinal Msg while if replying to msg\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

        if not message.reply_to_message:
            try:
                await client.send_photo(chat_id=message.chat.id, photo=MSG_img, caption=new_message_text, reply_markup=InlineKeyboardMarkup(buttons))
            except Exception as e:
                await client.send_message(chat_id=REQUEST_GC, text=f"⚠️download/anime CMD-GC Error\nFinal Msg Not Reply to msg\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

    else:
        anime_name = " ".join(args[1:])
        message_text, message_button, message_photo = await search_anime_list_by_Name(anime_name, UID)
        try:
            await client.send_photo(chat_id=message.chat.id, photo=message_photo, caption=message_text, reply_markup=message_button)
        except Exception as e:
            await message.reply_text("An Error Occurred, Try Again\nIf Problem persist Contact me 🛂", reply_markup=ERROR_BUTTON)
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Anime/Download CMD-PVT Error\nwhile sending final message\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)



@Bot.on_message(filters.command(["search", "find"]) & sub_PUB_Dc & sub_PUB_Sc & sub_GC & sub_BOT_c & filters.private)
async def search_anime(client, message):
    UID = message.from_user.id
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>Bish Provide Name Of Anime You Want To Search!<b/>\n|> /search Naruto")
        return
    anime_name = " ".join(args[1:])
    message_text, message_button, message_photo = await full_info_anime_list_by_Name(anime_name, UID)
    try:
        await message.reply_photo(
            photo=message_photo,
            caption=message_text,
            reply_markup=message_button
        )
    except Exception as e:
        await message.reply_text(
            text=message_text,
            reply_markup=message_button 
        )
        await client.send_message(chat_id=REQUEST_GC, text=f"CMD-PVT ⚠️\nSearch List Error\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
            


@Bot.on_message(filters.command(["search", "find"]) & filters.chat(FS_GROUP))
async def gcanimesearch(client, message):
    UID = message.from_user.id
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>Bish Provide Name Of Anime You Want To Search!<b/>\n|> /search Naruto")
        return
    anime_name = " ".join(args[1:])
    message_text, message_button, message_photo = await full_info_anime_list_by_Name(anime_name, UID)
    try:
        await message.reply_photo(
            photo=message_photo,
            caption=message_text,
            reply_markup=message_button
        )
    except Exception as e:
        await message.reply_text(
            text=message_text,
            reply_markup=message_button 
        )
        await client.send_message(chat_id=REQUEST_GC, text=f"CMD-PVT ⚠️\nSearch List Error\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)



@Bot.on_message(filters.command(["search", "find"]) & filters.private)
async def nosearchpvtcleft(client, message):
     await message.reply_photo(photo=ALLCMD_FS_PIC, caption=ALLCMD_FS_TXT)
  
@Bot.on_message(filters.command(["download", "anime"]) & filters.private)
async def nodownloadleftc(client, message):
     await message.reply_photo(photo=ALLCMD_FS_PIC, caption=ALLCMD_FS_TXT)
  
@Bot.on_message(filters.command(["anime_info", "info"]) & filters.private)
async def nofullanineleftc(client, message):
     await message.reply_photo(photo=ALLCMD_FS_PIC, caption=ALLCMD_FS_TXT)
        
@Bot.on_message(filters.command(["list", "fullsearch"]) & filters.private)
async def listfullsearchfs(client, message):
     await message.reply_photo(photo=ALLCMD_FS_PIC, caption=ALLCMD_FS_TXT)
        
@Bot.on_message(filters.command("request") & filters.private)
async def norequestleftc(client, message):
     await message.reply_photo(photo=ALLCMD_FS_PIC, caption=ALLCMD_FS_TXT)



@Bot.on_message(filters.command(["anime_info", "info"]) & sub_PUB_Dc & sub_PUB_Sc & sub_GC & sub_BOT_c & filters.private)
async def animefulinfo(client, message):
    UID = message.from_user.id
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /find or /search")
        return
    try:
        anime_id = int(args[1])
    except (IndexError, ValueError):
        await message.reply_text(f"Index Error!   *_*\n Did you fuck up the number after command??")
        return
    
    F_BOOL, first_message, message_text, cover_url, banner_url, title_img, trailer_url, site_url = await get_full_anime_info(anime_id)
    
    if F_BOOL == True:
        
        try:
            await message.reply_photo(banner_url, caption=first_message)
        except Exception as e:
            await message.reply_photo(cover_url, caption=first_message)
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Full anime info CMD-PVT MSG-1 Error\nwhile banner img with description\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

        S_CB_DATA = f"{UID}:{anime_id}"
        YtRESULT_B = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🖥️ Anime Site", url=site_url),
                    InlineKeyboardButton("Watch Trailer 🖥️", url=trailer_url)
                ],
                [
                    InlineKeyboardButton("𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗", callback_data=f"Anime_DL_{S_CB_DATA}""),
                    InlineKeyboardButton("𝗖𝗟𝗢𝗦𝗘", callback_data="close"),             
                ]
            ]
        )
    
        try:
            await message.reply_photo(title_img, caption=message_text, reply_markup=YtRESULT_B)
        except Exception as e:
            await message.reply_text("An Error Occurred, Try Agin\nIf Problem persist Contact me 🛂", reply_markup=ERROR_BUTTON)
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Full anime info CMD-PVT MSG-2 Error\ntitle image and infos\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
            
    else:
        try:
            await message.reply_photo(title_img, caption=f"{first_message}\n{message_text}", reply_markup=ERROR_BUTTON)
        except Exception as e:
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️Full anime info CMD-PVT MSG-2 Error\ntitle image and infos\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
  


@Bot.on_message(filters.command(["list", "fullsearch"]) & sub_PUB_Dc & sub_PUB_Sc & sub_GC & sub_BOT_c & filters.private)
async def many_anime_list(client, message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>Bish Provide Name Of Anime You Want To Search!<b/>\n|> /search Naruto")
        return
    anime_name = " ".join(args[1:])
    message_text, message_button, message_photo = await search_find_anime_list(anime_name)
    try:
        await message.reply_photo(
            photo=message_photo,
            caption=message_text,
            reply_markup=message_button
        )
    except Exception as e:
        await message.reply_text(
            text=message_text,
            reply_markup=message_button 
        )
        await client.send_message(chat_id=REQUEST_GC, text=f"CMD-PVT ⚠️\nSearch List Error\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
            

