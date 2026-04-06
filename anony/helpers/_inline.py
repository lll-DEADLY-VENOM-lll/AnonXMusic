# File: anony/helpers/_inline.py
from .markup.start import StartMarkup
from .markup.play import PlayMarkup
from anony import config

class Inline(StartMarkup, PlayMarkup):
    def __init__(self):
        super().__init__()

    def ping_markup(self, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=f"🚀 {text}", url=config.SUPPORT_CHAT)]])

    def yt_key(self, link: str) -> types.InlineKeyboardMarkup:
        return self.ikm([[
            self.ikb(text="📋 Copy Link", copy_text=link),
            self.ikb(text="📺 YouTube", url=link),
        ]])

    def cancel_dl(self, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=f"❌ {text}", callback_data="cancel_dl")]])
