from pyrogram import types

class PlayInline:
    def controls(self, chat_id: int, status: str = None, timer: str = None, remove: bool = False) -> types.InlineKeyboardMarkup:
        keyboard = []
        if status: keyboard.append([self.ikb(text=status, callback_data=f"controls status {chat_id}")])
        elif timer: keyboard.append([self.ikb(text=timer, callback_data=f"controls status {chat_id}")])
        if not remove:
            keyboard.append([
                self.ikb(text="▷", callback_data=f"controls resume {chat_id}"),
                self.ikb(text="II", callback_data=f"controls pause {chat_id}"),
                self.ikb(text="⥁", callback_data=f"controls replay {chat_id}"),
                self.ikb(text="‣‣I", callback_data=f"controls skip {chat_id}"),
                self.ikb(text="▢", callback_data=f"controls stop {chat_id}"),
            ])
        return self.ikm(keyboard)

    def yt_key(self, link: str) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text="❐", copy_text=link), self.ikb(text="Youtube", url=link)]])

    def cancel_dl(self, text) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=text, callback_data="cancel_dl")]])
