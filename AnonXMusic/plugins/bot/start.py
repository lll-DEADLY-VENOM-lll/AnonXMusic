import time
import re
import random
import asyncio

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate
from pyrogram.errors.exceptions.flood_420 import SlowmodeWait

import config
from AnonXMusic import app
from AnonXMusic.misc import _boot_
from AnonXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
    blacklist_chat,
)
from AnonXMusic.utils.decorators.language import LanguageStart
from AnonXMusic.utils.formatters import get_readable_time
from config import BANNED_USERS, LOGGER_ID
from strings import get_string

# --- Reaction Command in Private Chat ---
@app.on_message(filters.command(["react", "reaction"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def react_pm(client, message: Message, _):
    # User ko database mein add karna
    await add_served_user(message.from_user.id)
    
    # Aapke style mein pehle Sticker bhejna
    await message.reply_sticker("CAACAgUAAx0CdQO5IgACMTplUFOpwDjf-UC7pqVt9uG659qxWQACfQkAAghYGFVtSkRZ5FZQXDME")
    
    # Photo aur Caption ke sath reply (Strings use karke)
    await message.reply_photo(
        photo=random.choice(config.START_IMG_URL),
        caption=_["react_1"].format(message.from_user.mention, app.mention),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                ],
            ]
        ),
    )
    
    # Logger notification logic
    if await is_on_off(2):
        return await app.send_message(
            chat_id=config.LOGGER_ID,
            text=f"{message.from_user.mention} ᴊᴜsᴛ ᴄʜᴇᴄᴋᴇᴅ <b>ʀᴇᴀᴄᴛɪᴏɴ ғᴇᴀᴛᴜʀᴇ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
        )

# --- Reaction Command in Group Chat ---
@app.on_message(filters.command(["react", "reaction"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def react_gp(client, message: Message, _):
    uptime = int(time.time() - _boot_)
    try:
        await message.reply_photo(
            photo=random.choice(config.START_IMG_URL),
            caption=_["react_2"].format(app.mention, get_readable_time(uptime)),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            ),
        )
        return await add_served_chat(message.chat.id)
    except ChannelPrivate:
        return
    except SlowmodeWait as e:
        await asyncio.sleep(e.value)
        try:
            await message.reply_photo(
                photo=random.choice(config.START_IMG_URL),
                caption=_["react_2"].format(app.mention, get_readable_time(uptime)),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                        ],
                    ]
                ),
            )
            return await add_served_chat(message.chat.id)
        except:
            return

# --- Automatic Reaction Logic (Bonus) ---
# Ye bot ko har message par react karne se rokne ke liye Myanmar character filter bhi check karta hai
@app.on_message(filters.group & ~BANNED_USERS, group=10)
async def auto_reaction(client, message: Message):
    try:
        # Myanmar character filter (Aapke example ke logic se)
        if (message.chat.title and re.search(r'[\u1000-\u109F]', message.chat.title)) or \
           (message.text and re.search(r'[\u1000-\u109F]', message.text)):
            return # Agar Myanmar char hai toh react nahi karega

        # Example: Agar message mein 'music' ya 'bot' likha ho toh reaction dega
        if message.text and ("music" in message.text.lower() or "bot" in message.text.lower()):
            reactions = ["⚡", "🔥", "❤️", "🎉", "😎"]
            await message.react(random.choice(reactions))
            
    except Exception:
        pass
