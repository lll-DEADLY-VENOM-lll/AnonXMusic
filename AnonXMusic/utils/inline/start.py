from pyrogram.types import InlineKeyboardButton

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
                text="sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ", url=f"https://t.me/ll_DEADLY_VENOM_ll" # Apna link yaha dalein
            ),
            InlineKeyboardButton(
                text="ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/KIRU_OP" # Apna username yaha dalein
            ),
        ],
        [
            InlineKeyboardButton(
                text="ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="settings_back_helper"
            )
        ],
    ]
    return buttons
