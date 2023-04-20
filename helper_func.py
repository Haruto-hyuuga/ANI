import base64
import re
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import ADMINS, SUB_CHANNEL, DUB_CHANNEL, FS_BOT_CHANNEL, FS_GROUP
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait

async def is_subscribed_SC(filter, client, update):
    user_id = update.from_user.id
    try:
        member = await client.get_chat_member(chat_id = SUB_CHANNEL, user_id = user_id)
    except UserNotParticipant:
        return False
    
    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    else:
        return True

async def F_SC_txt(MC):
    if MC == False:
        C1T = "𝗝𝗢𝗜𝗡 ⚠️: @ANIME_DOWNLOADS_SUB"
    else:
        C1T = "✅: <code>@ANIME_DOWNLOADS_SUB</code>"
    return C1T

async def is_subscribed_DC(filter, client, update):
    user_id = update.from_user.id
    try:
        member = await client.get_chat_member(chat_id = DUB_CHANNEL, user_id = user_id)
    except UserNotParticipant:
        return False
    
    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    else:
        return True

async def F_DC_txt(DC):
    if DC == False:
        C4T = "𝗝𝗢𝗜𝗡 ⚠️: @ANIME_DOWNLOADS_DUB"
    else:
        C4T = "✅: <code>@ANIME_DOWNLOADS_DUB</code>"
    return C4T

async def is_subscribed_BOT(filter, client, update):
    user_id = update.from_user.id
    try:
        member = await client.get_chat_member(chat_id = FS_BOT_CHANNEL, user_id = user_id)
    except UserNotParticipant:
        return False
    
    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    else:
        return True

async def F_BC_txt(BC):
    if BC == False:
        C2T = "𝗝𝗢𝗜𝗡 ⚠️: @AnimeRobots"
    else:
        C2T = "✅: <code>@AnimeRobots</code>"
    return C2T

async def is_subscribed_GROUP(filter, client, update):
    user_id = update.from_user.id
    try:
        member = await client.get_chat_member(chat_id = FS_GROUP, user_id = user_id)
    except UserNotParticipant:
        return False
    
    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    else:
        return True

async def F_GC_txt(GC):
    if GC == False:
        C3T = "𝗝𝗢𝗜𝗡 ⚠️: @AnimeCommunityChat"
    else:
        C3T = "✅: <code>@AnimeCommunityChat</code>"
    return C3T

async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string

async def decode(base64_string):
    base64_string = base64_string.strip("=") # links generated before this commit will be having = sign, hence striping them to handle padding errors.
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes) 
    string = string_bytes.decode("ascii")
    return string

async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    while total_messages != len(message_ids):
        temb_ids = message_ids[total_messages:total_messages+200]
        try:
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temb_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temb_ids
            )
        except:
            pass
        total_messages += len(temb_ids)
        messages.extend(msgs)
    return messages

async def get_message_id(client, message):
    if message.forward_from_chat:
        if message.forward_from_chat.id == client.db_channel.id:
            return message.forward_from_message_id
        else:
            return 0
    elif message.forward_sender_name:
        return 0
    elif message.text:
        pattern = "https://t.me/(?:c/)?(.*)/(\d+)"
        matches = re.match(pattern,message.text)
        if not matches:
            return 0
        channel_id = matches.group(1)
        msg_id = int(matches.group(2))
        if channel_id.isdigit():
            if f"-100{channel_id}" == str(client.db_channel.id):
                return msg_id
        else:
            if channel_id == client.db_channel.username:
                return msg_id
    else:
        return 0


def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time


MBCMD = ["stats", "request", "search", "find", "download", "anime", "", "", "", "", "", "", "", """""""""""""""""""""""]


sub_PUB_Sc = filters.create(is_subscribed_SC)
sub_PUB_Dc = filters.create(is_subscribed_DC)
sub_BOT_c = filters.create(is_subscribed_BOT)
sub_GC = filters.create(is_subscribed_GROUP)
