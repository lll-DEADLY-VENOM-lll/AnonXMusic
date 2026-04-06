from pyrogram import types
from anony import app, config, lang
from anony.core.lang import lang_codes

class StartPanel:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

    def start_key(self, lang: dict, private: bool = False) -> types.InlineKeyboardMarkup:
        rows = [
            [self.ikb(text=lang["add_me"], url=f"https://t.me/{app.username}?startgroup=true")],
            [self.ikb(text=lang["help"], callback_data="help")],
            [
                self.ikb(text=lang["support"], url=config.SUPPORT_CHAT),
                self.ikb(text=lang["channel"], url=config.SUPPORT_CHANNEL),
            ],
            [
                self.ikb(text="ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/LingTech_Dev"), 
                # Yahan config.OWNER_ID se [0] hata diya gaya hai
                self.ikb(text="ᴏᴡɴᴇʀ", url=f"tg://user?id={config.OWNER_ID}") 
            ],
        ]
        if private:
            rows += [[self.ikb(text=lang["source"], url="https://t.me/+MK6R6rfagT8zNWQ1")]]
        else:
            rows += [[self.ikb(text=lang["language"], callback_data="language")]]
        return self.ikm(rows)

    def help_markup(self, _lang: dict, back: bool = False) -> types.InlineKeyboardMarkup:
        if back:
            rows = [[self.ikb(text=_lang["back"], callback_data="help back"), 
                     self.ikb(text=_lang["close"], callback_data="help close")]]
        else:
            cbs = ["admins", "auth", "blist", "lang", "ping", "play", "queue", "stats", "sudo"]
            buttons = [self.ikb(text=_lang[f"help_{i}"], callback_data=f"help {cb}") for i, cb in enumerate(cbs)]
            rows = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]
            # Yahan bhi theek kar diya gaya hai
            rows.append([self.ikb(text="ᴏᴡɴᴇʀ", url=f"tg://user?id={config.OWNER_ID}")])
        return self.ikm(rows)

    def lang_markup(self, _lang: str) -> types.InlineKeyboardMarkup:
        langs = lang.get_languages()
        buttons = [self.ikb(text=f"{name} ({code}) {'✔️' if code == _lang else ''}", 
                            callback_data=f"lang_change {code}") for code, name in langs.items()]
        rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        return self.ikm(rows)

    def settings_markup(self, lang: dict, admin_only: bool, cmd_delete: bool, language: str, chat_id: int) -> types.InlineKeyboardMarkup:
        return self.ikm([
            [self.ikb(text=lang["play_mode"] + " ➜", callback_data="settings"), self.ikb(text=admin_only, callback_data="settings play")],
            [self.ikb(text=lang["cmd_delete"] + " ➜", callback_data="settings"), self.ikb(text=cmd_delete, callback_data="settings delete")],
            [self.ikb(text=lang["language"] + " ➜", callback_data="settings"), self.ikb(text=lang_codes[language], callback_data="language")],
        ])

    def ping_markup(self, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm([
            [self.ikb(text=text, url=config.SUPPORT_CHAT)],
            [self.ikb(text="ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/LingTech_Dev")]
        ])
