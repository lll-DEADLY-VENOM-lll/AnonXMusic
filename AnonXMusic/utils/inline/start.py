from pyrogram.types import InlineKeyboardButton
import config
from AloneMusic import app

def start_panel(_):
    # Yeh buttons tab dikhenge jab bot group mein start kiya jaye
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
        ],
        [
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
            InlineKeyboardButton(text="📢 ᴄʜᴀɴɴᴇʟ", url=config.SUPPORT_CHANNEL), # Extra button
        ],
    ]
    return buttons


def private_panel(_):
    # Yeh buttons tab dikhenge jab bot private (DM) mein start kiya jaye
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"], # Add me to your group
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text=_["S_B_4"], callback_data="settings_back_helper"), # Help & Commands
        ],
        [
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT), # Support Group
            InlineKeyboardButton(text="🛠 ᴅᴇᴠ", user_id=config.OWNER_ID[0]), # Owner link
        ],
        [
            InlineKeyboardButton(text="❄️ sᴏᴜʀᴄᴇ", url=f"https://t.me/HEROKU_CLUB"),
            InlineKeyboardButton(text="💌 ʏᴛ-ᴀᴘɪ", callback_data="bot_info_data"),
        ],
    ]
    return buttons
