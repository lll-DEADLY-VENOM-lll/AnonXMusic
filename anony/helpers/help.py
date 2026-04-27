from pyrogram import types

class HelpInline:
    def help_markup(self, _lang: dict, back: bool = False) -> types.InlineKeyboardMarkup:
        if back:
            rows = [[self.ikb(text=_lang["back"], callback_data="help back"), self.ikb(text=_lang["close"], callback_data="help close")]]
        else:
            cbs = ["admins", "auth", "blist", "lang", "ping", "play", "queue", "stats", "sudo"]
            buttons = [self.ikb(text=_lang[f"help_{i}"], callback_data=f"help {cb}") for i, cb in enumerate(cbs)]
            rows = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]
        return self.ikm(rows)
