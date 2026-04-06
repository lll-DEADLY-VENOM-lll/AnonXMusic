from pyrogram import types

class PlayPanel:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

    def controls(self, chat_id: int, status: str = None, timer: str = None, remove: bool = False) -> types.InlineKeyboardMarkup:
        keyboard = []
        if status:
            keyboard.append([self.ikb(text=status, callback_data=f"controls status {chat_id}")])
        elif timer:
            keyboard.append([self.ikb(text=timer, callback_data=f"controls status {chat_id}")])

        if not remove:
            keyboard.append([
                self.ikb(text="▷", callback_data=f"controls resume {chat_id}"),
                self.ikb(text="II", callback_data=f"controls pause {chat_id}"),
                self.ikb(text="⥁", callback_data=f"controls replay {chat_id}"),
                self.ikb(text="‣‣I", callback_data=f"controls skip {chat_id}"),
                self.ikb(text="▢", callback_data=f"controls stop {chat_id}"),
            ])
        return self.ikm(keyboard)

    # Yeh buttons aapke script ke filters.regex ("downloadvideo" aur "downloadaudio") se match karte hain
    def yt_key(self, link: str, vidid: str) -> types.InlineKeyboardMarkup:
        return self.ikm([
            [
                self.ikb(text="❐ Copy Link", copy_text=link),
                self.ikb(text="Youtube", url=link)
            ],
            [
                # Inka callback_data aapke filter regex se match karega
                self.ikb(text="🎵 Audio", callback_data=f"downloadaudio {vidid}"),
                self.ikb(text="🎬 Video", callback_data=f"downloadvideo {vidid}")
            ]
        ])

    def play_queued(self, chat_id: int, item_id: str, _text: str) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=_text, callback_data=f"controls force {chat_id} {item_id}")]])

    def queue_markup(self, chat_id: int, _text: str, playing: bool) -> types.InlineKeyboardMarkup:
        _action = "pause" if playing else "resume"
        return self.ikm([[self.ikb(text=_text, callback_data=f"controls {_action} {chat_id} q")]])

    def cancel_dl(self, text) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=text, callback_data=f"cancel_dl")]])
