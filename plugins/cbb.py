from pyrogram import __version__
from bot import Bot
from pyrogram.types import Message, CallbackQuery
from database.inline import*
from config import START_MSG, ABOUT_TEXT, REQUEST_TEXT, ALL_CHANNEL_TEXT

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "BACK_HOME":
        await query.message.edit_text(
            text = START_MSG.format(query.from_user.mention),
            reply_markup = START_B
        )
    elif data == "About_Bot":
        await query.message.edit_text(
            text = ABOUT_TEXT,
            reply_markup = ABOUT_BUTTONS
        )
    elif data == "DL_Channels":
        await query.message.edit_text(
            text = ALL_CHANNEL_TEXT,
            reply_markup = CHANNELS_BUTTON
        )
    elif data == "A_requests":
        await query.message.edit_text(
            text = REQUEST_TEXT,
            reply_markup = REQUEST_BUTTONS
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
