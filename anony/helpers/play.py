# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# File: play.py (Music Playback & Control UI)

from pyrogram import types
from anony.core.lang import lang_codes

class PlayMarkup:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

    def player_panel(
        self,
        chat_id: int,
        status: str = None,
        timer: str = None,
        remove: bool = False,
    ) -> types.InlineKeyboardMarkup:
        """Main Music Player Buttons"""
        keyboard = []
        
        # Display Status (Playing/Paused) or Time progress
        if status:
            keyboard.append([self.ikb(text=f"🎵 {status}", callback_data=f"controls status {chat_id}")])
        elif timer:
            keyboard.append([self.ikb(text=f"⏳ {timer}", callback_data=f"controls status {chat_id}")])

        if not remove:
            # Control Row: Playback icons
            keyboard.append(
                [
                    self.ikb(text="▷", callback_data=f"controls resume {chat_id}"),
                    self.ikb(text="II", callback_data=f"controls pause {chat_id}"),
                    self.ikb(text="⥁", callback_data=f"controls replay {chat_id}"),
                    self.ikb(text="‣‣I", callback_data=f"controls skip {chat_id}"),
                    self.ikb(text="▢", callback_data=f"controls stop {chat_id}"),
                ]
            )
            # Close button for clean UI
            keyboard.append([self.ikb(text="🗑 Close Player", callback_data="close")])
            
        return self.ikm(keyboard)

    def play_queued(self, chat_id: int, item_id: str, _text: str) -> types.InlineKeyboardMarkup:
        """Button to force play a song from the queue"""
        return self.ikm([[
            self.ikb(text=f"▶️ Play Now: {_text}", callback_data=f"controls force {chat_id} {item_id}")
        ]])

    def queue_markup(self, chat_id: int, _text: str, playing: bool) -> types.InlineKeyboardMarkup:
        """Queue management button"""
        _action = "pause" if playing else "resume"
        return self.ikm([[
            self.ikb(text=f"🔘 {_text}", callback_data=f"controls {_action} {chat_id} q")
        ]])

    def yt_key(self, link: str) -> types.InlineKeyboardMarkup:
        """YouTube link and Copy buttons"""
        return self.ikm([
            [
                self.ikb(text="📋 Copy Link", copy_text=link),
                self.ikb(text="📺 YouTube", url=link),
            ],
        ])

    def cancel_dl(self, text: str) -> types.InlineKeyboardMarkup:
        """Download cancellation button"""
        return self.ikm([[self.ikb(text=f"❌ {text}", callback_data="cancel_dl")]])
