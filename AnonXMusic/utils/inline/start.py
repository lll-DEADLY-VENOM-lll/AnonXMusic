from pyrogram.types import InlineKeyboardButton
import config
from AnonXMusic import app

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons

def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="✚ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ ✚",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text="sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT
            ),
            InlineKeyboardButton(
                text="💌 ʏᴛ-ᴀᴘɪ", url=config.SUPPORT_CHANNEL # या अपना लिंक दें
            ),
        ],
        [
            InlineKeyboardButton(
                text="ʙᴏᴛ ᴅᴏᴄ's         ▢", url=f"https://t.me/about_deadly_venom"
            ),
            InlineKeyboardButton(
                text="ᴍɪɴɪ ᴀᴘᴘ         ▢", url=f"https://t.me/about_deadly_venom"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅ", callback_data="settings_back_helper"
            )
        ],
    ]
    return buttons
