import math
from pyrogram.types import InlineKeyboardButton
import config
from AnonXMusic.utils.formatters import time_to_seconds

# 1. बेहतर ट्रैक सिलेक्शन (Audio/Video के साथ Support Chat)
def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text="🎵 ᴀᴜᴅɪᴏ",
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="🎥 ᴠɪᴅᴇᴏ",
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="💬 sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT
            ),
            InlineKeyboardButton(
                text="🗑 ᴄʟᴏsᴇ",
                callback_data=f"forceclose {videoid}|{user_id}",
            )
        ],
    ]
    return buttons

# 2. एडवांस प्लेयर (Progress Bar और Control Buttons के साथ)
def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100
    umm = math.floor(percentage)
    
    if 0 < umm <= 10:
        bar = "▰▱▱▱▱▱▱▱▱▱"
    elif 10 < umm < 20:
        bar = "▰▰▱▱▱▱▱▱▱▱"
    elif 20 <= umm < 30:
        bar = "▰▰▰▱▱▱▱▱▱▱"
    elif 30 <= umm < 40:
        bar = "▰▰▰▰▱▱▱▱▱▱"
    elif 40 <= umm < 50:
        bar = "▰▰▰▰▰▱▱▱▱▱"
    elif 50 <= umm < 60:
        bar = "▰▰▰▰▰▰▱▱▱▱"
    elif 60 <= umm < 70:
        bar = "▰▰▰▰▰▰▰▱▱▱"
    elif 70 <= umm < 80:
        bar = "▰▰▰▰▰▰▰▰▱▱"
    elif 80 <= umm < 95:
        bar = "▰▰▰▰▰▰▰▰▰▱"
    else:
        bar = "▰▰▰▰▰▰▰▰▰▰"

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                callback_data="GetTimer",
            )
        ],
        [   
            InlineKeyboardButton(text="⏮", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="II ᴘᴀᴜsᴇ", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="▶ ʀᴇsᴜᴍᴇ", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="▢ sᴛᴏᴘ", callback_data=f"ADMIN Stop|{chat_id}"),
            InlineKeyboardButton(text="📜 ǫᴜᴇᴜᴇ", callback_data=f"admin_cache{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="🚀 sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT),
            InlineKeyboardButton(text="🥀 ᴅᴇᴠ", url=f"https://t.me/ll_DEADLY_VENOM_ll"),
        ],
    ]
    return buttons

# 3. बेसिक प्लेयर (बिना टाइमर वाले स्ट्रीम के लिए)
def stream_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="▶", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="↻", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="⏭", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="✨ sᴜᴘᴘᴏʀᴛ ✨", url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons

# --- यहाँ से नए फंक्शन्स हैं जो एरर ठीक करेंगे ---

def livestream_markup(_, videoid, user_id, mode, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text="🎥 ᴊᴏɪɴ ʟɪᴠᴇ",
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🗑 ᴄʟᴏsᴇ",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons

def playlist_markup(_, videoid, user_id, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text="🎵 ᴀᴜᴅɪᴏ",
                callback_data=f"AnonPlaylists {videoid}|{user_id}|a|{fplay}",
            ),
            InlineKeyboardButton(
                text="🎥 ᴠɪᴅᴇᴏ",
                callback_data=f"AnonPlaylists {videoid}|{user_id}|v|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🗑 ᴄʟᴏsᴇ",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons

def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(
                text="🎵 ᴀᴜᴅɪᴏ",
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="🎥 ᴠɪᴅᴇᴏ",
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❮",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="🗑 ᴄʟᴏsᴇ",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
            InlineKeyboardButton(
                text="❯",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons
