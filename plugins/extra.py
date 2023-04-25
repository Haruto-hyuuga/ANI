from bot import Bot
from pyrogram import Client, filters, __version__
from pyrogram.types import Message
from config import ADMINS, Gif_Random, REQUEST_GC, ERR_TOPIC_ID, USER_LOG_CHANNEL
from database.inline import AllFSCB
from database.user_stats import get_user_Ani_Id, update_Anid
from database.req_Db import full_requestDB_DUB, full_requestDB_SUB, del_DUB_request, del_SUB_request
from req import search_user_name, search_user_id

GC_LOG_TXT = """
🔴 #New_GROUP
Title: {}

🆔: <code>{}</code>  #id{}
🔗: @{}
🚷 LEFT GROUP ✅
"""

"""

@Bot.on_message(filters.group & filters.new_chat_members)
async def leave_group(client, message: Message):
    
    added_by = [user.id for user in message.new_chat_members if user.is_bot]
    TGC_id = message.chat.id
    TGC_Lk = message.chat.username
    TGC_TT = message.chat.title
    FINAL_GIF = await Gif_Random()

    if ADMINS in added_by:

        THANKS_MSG = "<b>Thanks For Having Me In:</b> {}"
        await client.send_animation(chat_id=TGC_id, animation=FINAL_GIF, caption=THANKS_MSG.format(TGC_TT))
        pass

    if ADMINS not in added_by:

        ALLCC_MSG = "<b>FEEL FREE TO USE ME IN PRIVATE CHAT</b>\n𝙃𝙚𝙧𝙚'𝙨 𝙏𝙝𝙚 𝙇𝙞𝙨𝙩 𝙊𝙛 𝘼𝙡𝙡 𝘾𝙝𝙖𝙣𝙣𝙚𝙡𝙨:"
        try:
            await client.send_animation(chat_id=TGC_id, animation=FINAL_GIF, caption=ALLCC_MSG, reply_markup=AllFSCB)    
            await client.send_message(chat_id=USER_LOG_CHANNEL, text=GC_LOG_TXT.format(TGC_TT, TGC_id, TGC_id, TGC_Lk))
            await client.leave_chat(TGC_id)
        except Exception as e:
            await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️AUTO LEAVE UNAUTH GROUP\nwhile Leaving Group\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)

"""
        
@Bot.on_message(filters.command("auth") & filters.private)
async def auth_ani_acc(client, message):
    UID = message.from_user.id
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Bruh you stoopid? <b>Mention Name of Anime after Command or Anime Id</b>\n<i>You can Also Try using Command:</i> /find ")
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
                await message.reply_text("Something Went Wrong, Try Again Later If Problem Persist Contact Owner")
                await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️while Adding User Anilist\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)
        else:
            await message.reply_text(f"You're Anilist Account Is Already Added With ID: {Ani_id}\n\n<b>To Delete And Add New Id Use Command: /unauth </b>\nTo Add New Id Delete First Id Then /auth Agin")
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
            await message.reply_text("Something Went Wrong, Try Again Later If Problem Persist Contact Owner")
            await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️while Adding User Anilist\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)


@Bot.on_message(filters.command("unauth") & filters.private)
async def delete_anilist_acc(client, message):
    UID = message.from_user.id
    try:
        Ani_i = await get_user_Ani_Id(UID)
        if Ani_id == 0:
            await message.reply_text("You Never Added Anilist Account Retard")
        else:
            Ani_no = 0
            await update_Anid(UID, Ani_no)
            await message.reply_text("DELETED ANILIST ACCOUNT 🗑️✅")
    except:
        await message.reply_text("Something Went Wrong, Try Again Later If Problem Persist Contact Owner")
        await cleint.send_message(chat_id=REQUEST_GC, text=f"⚠️while Adding User Anilist\n\n{e}", reply_to_message_id=ERR_TOPIC_ID)


@Bot.on_message(filters.command("reqlist") & filters.user(ADMINS))
async def pending_req_list(client, message):
    L = "🕊️"
    EM = await message.reply_text(L)
    Msg = "〰️〰️〰️〰️SUB REQUEST〰️〰️〰️〰️\n"
    Squery = await full_requestDB_SUB()
    for i, user in enumerate(Squery):
        Msg += f"{i+1}> ℹ️: <code>/info {user}</code>  🗑️: <code>/delsreq {user}</code>\n"

    await EM.edit(Msg)

    L2 = "🦋"
    FM = await message.reply_text(L2)
    Mdg += "〰️〰️〰️DUB REQUEST〰️〰️〰️"
    Dquery = await full_requestDB_DUB()
    for i, user in enumerate(Dquery):
        Mdg += f"{i+1}> ℹ️: <code>/info {user}</code>  🗑️: <code>/deldreq {user}</code>\n"
    await FM.edit(Mdg)

@Bot.on_message(filters.command("delsreq") & filters.user(ADMINS))
async def delete_subreq_list(client, message):
    ani = message.text.split(None, 1)[1]
    try:
        anime = int(ani)
        await del_SUB_request(anime)
        await message.reply_text("🗑️✅")
    except Exception as e:
        await message.reply_text(e)

@Bot.on_message(filters.command("deldreq") & filters.user(ADMINS))
async def delete_dubreq_list(client, message):
    ani = message.text.split(None, 1)[1]
    try:
        anime = int(ani)
        await del_DUB_request(anime)
        await message.reply_text("🗑️✅")
    except Exception as e:
        await message.reply_text(e)
        

    











