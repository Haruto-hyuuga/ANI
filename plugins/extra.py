from bot import Bot
from pyrogram import Client, filters, __version__
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS, Gif_Random, REQUEST_GC, ERR_TOPIC_ID, USER_LOG_CHANNEL, BOT_C_url
from database.inline import AllFSCB, CLOSE_BUTTON
from database.user_stats import get_user_Ani_Id, update_Anid
from database.req_Db import full_requestDB_DUB, full_requestDB_SUB, del_DUB_request, del_SUB_request
from req import search_user_name, search_user_id, get_cmd

GC_LOG_TXT = """
🔴 #New_GROUP
Title: {}

🆔: <code>{}</code>  #id{}
🔗: @{}
🚷 LEFT GROUP ✅
"""

        
@Bot.on_message(get_cmd("auth") & filters.private)
async def auth_ani_acc(client, message):
    UID = message.from_user.id
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>Mention Your Anilist Username or Id</b>")
        return
    arg = args[1]
    if arg.isdigit():
        try:
            Ani_id = int(arg)
        except (IndexError, ValueError):
            await message.reply_text(f"{message.from_user.mention}-san Please Don't Did you fuck With Anime Id.\nProvide A valid Anime Id")
            return
        Ani_i = await get_user_Ani_Id(UID)
        if Ani_i == 0:
            try:
                message_photo, Ani_C, Ani_MW, Ani_EW, Ani_MS = await search_user_id(Ani_id)
                if Ani_C==Ani_MW==Ani_EW==Ani_MS=="None":
                    await message.reply_text("No User Found With This ID, Check and Try Agin")
                elif Ani_C==Ani_MW==Ani_EW==Ani_MS=="error⚠️":
                    await message.reply_text("Some Error Occurred, Try Again Later Or Contact Bot Owner")
                else:
                    await update_Anid(UID, Ani_id)
                    await message.reply_photo(
                        photo=message_photo,
                        caption=f"SUCCESSFULLY SET ANILIST ACCOUNT ✅\nAnime Watched: {Ani_C}\nEpisodes Watched: {Ani_EW}\nScore: {Ani_MS}"
                    )
            except Exception as e:
                await message.reply_text("Invalid Anilist User ID, Double Check Your Anilist id or search By username")
                await client.send_message(chat_id=REQUEST_GC, text=f"⚠️while Adding User Anilist\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
        else:
            await message.reply_text(f"You're Anilist Account Is Already Added With ID: {Ani_i}\n\n<b>To Delete And Add New Id Use Command: /unauth </b>\nTo Add New Id Delete First Id Then /auth Agin")
    else:
        user_name = message.text.split(None, 1)[1]
        try:
            message_text, message_button = await search_user_name(user_name)
            Pic = "https://telegra.ph/file/9445f7c606afe00882ab8.jpg"
            await message.reply_photo(
                photo=Pic,
                caption=message_text,
                reply_markup=message_button
            )
        except Exception as e:
            await message.reply_text("Can't Find Any Anilist Account For given Query")
            await client.send_message(chat_id=REQUEST_GC, text=f"⚠️while Adding User Anilist\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)


@Bot.on_message(get_cmd("unauth") & filters.private)
async def delete_anilist_acc(client, message):
    UID = message.from_user.id
    try:
        Ani_i = await get_user_Ani_Id(UID)
        if Ani_i == 0:
            await message.reply_text("You Never Added Anilist Account Retard")
        else:
            Ani_no = 0
            await update_Anid(UID, Ani_no)
            await message.reply_text("DELETED ANILIST ACCOUNT 🗑️✅")
    except Exception as e:
        await message.reply_text("Something Went Wrong, Try Again Later If Problem Persist Contact Owner")
        await client.send_message(chat_id=REQUEST_GC, text=f"⚠️while Deleting User Anilist\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)


@Bot.on_message(get_cmd("reqlist") & filters.user(ADMINS))
async def pending_req_list(client, message):

    Squery = await full_requestDB_SUB()
    TSR = len(Squery)
    msg = f"Total SUB Requests: {TSR}\n〰️〰️〰️〰️⌛〰️〰️〰️〰️\n\n"
    for i, user in enumerate(Squery):
        msg += f"{i+1}> ℹ️: <code>/info {user}</code>  🗑️: <code>/delsreq {user}</code>\n"
    await message.reply_text(msg)


    Dquery = await full_requestDB_DUB()
    TDR = len(Dquery)
    msg2 = f"Total DUB Requests: {TDR}\n〰️〰️〰️〰️⌛〰️〰️〰️〰️\n\n"
    for i, user in enumerate(Dquery):
        msg2 += f"{i+1}> ℹ️: <code>/info {user}</code>  🗑️: <code>/deldreq {user}</code>\n"
    await message.reply_text(msg2)



@Bot.on_message(get_cmd("delsreq") & filters.user(ADMINS))
async def delete_subreq_list(client, message):
    ani = message.text.split(None, 1)[1]
    try:
        anime = int(ani)
        await del_SUB_request(anime)
        await message.reply_text("🗑️✅")
    except Exception as e:
        await message.reply_text(e)

@Bot.on_message(get_cmd("deldreq") & filters.user(ADMINS))
async def delete_dubreq_list(client, message):
    ani = message.text.split(None, 1)[1]
    try:
        anime = int(ani)
        await del_DUB_request(anime)
        await message.reply_text("🗑️✅")
    except Exception as e:
        await message.reply_text(e)
        

    
@Bot.on_message(get_cmd("reqply") & filters.user(ADMINS))
async def request_reply(client, message):
    if message.reply_to_message:
        MSG = message.reply_to_message
        if len(message.command) != 1:
            args = message.text.split()
            try:
                arg = args[1]
                user = await client.get_users(arg)
                mrm = user.mention
                uru = user.username
                UID = user.id
                await MSG.copy(UID)
                await message.reply_to_message.reply_text(f"Successfully Sent✅\n\n👤: {mrm}\n🆔: <code>{UID}</code>\n🔗: @{uru}")
            except Exception as e:
                await message.reply(e)
        else:
            await message.reply("Mention user id or username after command")
    else:
        await message.reply("Reply To A message you want to sent, and mention user you want to send after command")
        
decline_img = "https://telegra.ph/file/f622a97180154d69fff86.jpg"


@Bot.on_message(get_cmd("reqno", "decline") & filters.user(ADMINS))
async def request_decline(client, message):
    if message.reply_to_message:
        MSG = message.reply_to_message.text
        if len(message.command) != 1:
            args = message.text.split()
            try:
                arg = args[1]
                user = await client.get_users(arg)
                mrm = user.mention
                uru = user.username
                UID = user.id
                await client.send_photo(UID, photo=decline_img, caption=MSG, reply_markup=CLOSE_BUTTON)
                await message.reply_photo(photo=decline_img, caption=f"{MSG}\n\nSuccessfully Sent✅\n\n👤: {mrm}\n🆔: <code>{UID}</code>\n🔗: @{uru}")
            except Exception as e:
                await message.reply(e)
        else:
            await message.reply("Mention user id or username after command")
    else:
        await message.reply("Reply To A message you want to sent, and mention user you want to send after command")
        

@Bot.on_message(get_cmd(["reqyes", "accept"]))
async def request_accept(client, message):
    if message.reply_to_message:
        MSG = message.reply_to_message.text
        try:
            user = await client.get_users(arg)
            um = user.mention
            un = user.username
            UID = user.id
        except Exception as e:
            await message.reply(f"Error While Getting User\n\n{e}")
            return 
        if len(args) < 2:
            await message.reply_text("Mention Anime Id")
            return
        arg = args[1]
        if arg.isdigit():
            try:
                anime_id = int(arg)
            except (IndexError, ValueError):
                ErM = await message.reply_text(f"{message.from_user.mention}-san Did you fuck Anime Id After Command\nProvide A valid Anime Id")
                return

        E_title, J_title, MSG_img, Format, episodes, status, average_score, Igenres, studio, duration, season = await channel_post_anime_info(anime_id)
        buttons = await recommend_anime_button(anime_id)
        try:
            buttons.append(
                [
                    InlineKeyboardButton(text = '🌟 GIVE YOUR REVIEW ABOUT BOT ❓', url=BOT_C_url)
                ]
            )
        except IndexError:
            pass        
        message_text = f"""
Dear {um},
<b>Your Request For Anime:</b> 
🇬🇧:{E_title} 
🇯🇵:{J_title}
ᴇᴘɪꜱᴏᴅᴇꜱ: {episodes}
ᴛʏᴘᴇ: {Format}
ɢᴇɴʀᴇꜱ:{Igenres}
<b>has been completed, Thanks For Using Our Bot Don't Forget To Give Review 🌟.</b>
"""
        
        try:
            await del_DUB_request(anime_id)
            await message.reply_text("🗑️✅")
            await client.send_photo(UID, photo=MSG_img, caption=message_text, reply_markup=InlineKeyboardMarkup(buttons))
            await client.send_photo(message.chat.id, photo=MSG_img, caption=f"{message_text}\n\nSuccessfully Sent✅\n\n👤: {um}\n🆔: <code>{UID}</code>\n🔗: @{un}", reply_markup=InlineKeyboardMarkup(buttons)) 
        except Exception as e:
            await message.reply(f"While Sending Message\n\n{e})








