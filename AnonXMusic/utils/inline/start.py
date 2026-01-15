from pyrogram.types import InlineKeyboardButton
import config
from AnonXMusic import app

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="✚ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ✚",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text="ʜᴇʟᴘ", callback_data="settings_back_helper"
            ),
            InlineKeyboardButton(
                text="sᴇᴛᴛɪɴɢs", callback_data="settings_helper"
            ),
        ],
    ]
    return buttons

def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="✚ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ✚",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text="sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT
            ),
            InlineKeyboardButton(
                text="ᴄʜᴀɴɴᴇʟ", url=config.SUPPORT_CHANNEL
            ),
        ],
        [
            InlineKeyboardButton(
                text="sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ", url=f"https://t.me/ll_DEADLY_VENOM_ll"
            ),
            InlineKeyboardButton(
                text="ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/KIRU_OP"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="settings_back_helper"
            )
        ],
    ]
    return buttons
