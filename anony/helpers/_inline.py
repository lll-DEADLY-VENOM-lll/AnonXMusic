from pyrogram import types
from .start import StartInline
from .help import HelpInline
from .play import PlayInline

class Inline(StartInline, HelpInline, PlayInline):
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

# Global instance taaki har jagah use ho sake
buttons = Inline()
