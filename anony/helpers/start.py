from pyrogram import types
from anony import app, config, lang
from anony.core.lang import lang_codes

class StartInline:
    def start_key(self, lang: dict, private: bool = False) -> types.InlineKeyboardMarkup:
        rows = [[self.ikb(text=lang["add_me"], url=f"https://t.me/{app.username}?startgroup=true")],
                [self.ikb(text=lang["help"], callback_data="help")],
                [self.ikb(text=lang["support"], url=config.SUPPORT_CHAT),
                 self.ikb(text=lang["channel"], url=config.SUPPORT_CHANNEL)]]
        if private:
            rows += [[self.ikb(text=lang["source"], url="https://github.com/AnonymousX1025/AnonXMusic")]]
        else:
            rows += [[self.ikb(text=lang["language"], callback_data="language")]]
        return self.ikm(rows)

    def settings_markup(self, lang: dict, admin_only: bool, cmd_delete: bool, language: str, chat_id: int) -> types.InlineKeyboardMarkup:
        return self.ikm([
            [self.ikb(text=lang["play_mode"] + " ➜", callback_data="settings"), self.ikb(text=admin_only, callback_data="settings play")],
            [self.ikb(text=lang["cmd_delete"] + " ➜", callback_data="settings"), self.ikb(text=cmd_delete, callback_data="settings delete")],
            [self.ikb(text=lang["language"] + " ➜", callback_data="settings"), self.ikb(text=lang_codes[language], callback_data="language")]
        ])
    
    def lang_markup(self, _lang: str) -> types.InlineKeyboardMarkup:
        langs = lang.get_languages()
        buttons = [self.ikb(text=f"{name} ({code}) {'✔️' if code == _lang else ''}", callback_data=f"lang_change {code}") for code, name in langs.items()]
        return self.ikm([buttons[i : i + 2] for i in range(0, len(buttons), 2)])

    def ping_markup(self, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=text, url=config.SUPPORT_CHAT)]])
