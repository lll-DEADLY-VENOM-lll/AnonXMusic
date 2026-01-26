import time
import random
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

import config
from AnonXMusic import app
from AnonXMusic.misc import _boot_
from AnonXMusic.utils.database import is_on_off
from AnonXMusic.utils.decorators.language import LanguageStart
from AnonXMusic.utils.formatters import get_readable_time
from config import BANNED_USERS
from strings import get_string

@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@LanguageStart
async def ping_com(client, message: Message, _):
    # Aapke style mein pehle Sticker bhejna
    await message.reply_sticker("CAACAgUAAx0CdQO5IgACMTplUFOpwDjf-UC7pqVt9uG659qxWQACfQkAAghYGFVtSkRZ5FZQXDME")
    
    start = time.time()
    uptime = int(time.time() - _boot_)
    
    # Ping calculation
    ms = (time.time() - start) * 1000
    
    # Aapke style mein Photo + Caption + Keyboard
    await message.reply_photo(
        photo=random.choice(config.START_IMG_URL),
        caption=_["ping_1"].format(ms, app.mention, get_readable_time(uptime), config.SUPPORT_CHAT),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=_["S_B_3"],
                        url=f"https://t.me/{app.username}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=_["S_B_9"], url=config.SUPPORT_CHAT
                    ),
                    InlineKeyboardButton(
                        text=_["S_B_6"], url=config.UPSTREAM_REPO
                    )
                ],
            ]
        ),
    )
    
    # Aapke style mein LOGGER notification
    if await is_on_off(2):
        return await app.send_message(
            chat_id=config.LOGGER_ID,
            text=f"{message.from_user.mention} ᴊᴜsᴛ ᴄʜᴇᴄᴋᴇᴅ ᴛʜᴇ <b>ᴘɪɴɢ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
    )
