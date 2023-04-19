from bot import Bot
from pyrogram import Client, filters
from pyrogram.types import Message


@Bot.on_message(filters.command("addsub"))
async def addsub(client, message):
    await message.reply_text("hi")

@Bot.on_message(filters.command("delsub"))
async def delsub(client, message):
    await message.reply_text("hi")

@Bot.on_message(filters.command("adddub"))
async def adddub(client, message):
    await message.reply_text("hi")

@Bot.on_message(filters.command("deldub"))
async def deldub(client, message):
    await message.reply_text("hi")
