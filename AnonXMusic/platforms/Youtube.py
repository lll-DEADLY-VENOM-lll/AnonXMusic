import asyncio
import requests
import re
import os
from typing import Union
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

import config
from AnonXMusic import LOGGER

logger = LOGGER(__name__)

class YouTubeAPI: # Naam wahi rakha hai taaki error na aaye
    def __init__(self):
        # Aapka Cloudflare Worker API
        self.api_base = "https://jiosaavn-apii.shivampatel425685.workers.dev"
        self.regex = r"(?:youtube\.com|youtu\.be|saavn\.com|jiosaavn\.com)"
        self.base = "" # For compatibility

    def format_duration(self, seconds):
        try:
            seconds = int(seconds)
            mins = seconds // 60
            secs = seconds % 60
            duration_str = f"{mins:02d}:{secs:02d}"
            return duration_str, seconds
        except:
            return "00:00", 0

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        return bool(re.search(self.regex, link))

    async def url(self, message: Message) -> Union[str, None]:
        messages = [message]
        if message.reply_to_message:
            messages.append(message.reply_to_message)
        for msg in messages:
            if msg.entities:
                for entity in msg.entities:
                    if entity.type == MessageEntityType.URL:
                        return (msg.text or msg.caption)[entity.offset : entity.offset + entity.length]
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        """Saavn API se details nikalne ke liye"""
        try:
            # Agar YouTube link hai to sirf title extract karne ki koshish karega
            search_query = link
            search_url = f"{self.api_base}/search?query={search_query}"
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: requests.get(search_url).json())
            
            if response.get("status") == "SUCCESS" and response["data"]["results"]:
                song = response["data"]["results"][0]
                title = song["name"]
                duration_str, duration_sec = self.format_duration(song["duration"])
                thumb = song["image"][-1]["link"]
                vidid = song["id"]
                return title, duration_str, duration_sec, thumb, vidid
            return None
        except Exception as e:
            logger.error(f"Error in details: {e}")
            return None

    async def track(self, link: str, videoid: Union[bool, str] = None):
        res = await self.details(link, videoid)
        if not res:
            return None, None
        title, d_min, d_sec, thumb, vidid = res
        track_details = {
            "title": title,
            "link": link,
            "vidid": vidid,
            "duration_min": d_min,
            "thumb": thumb,
        }
        return track_details, vidid

    async def video(self, link: str, videoid: Union[bool, str] = None):
        """Streaming link nikalne ke liye"""
        try:
            search_url = f"{self.api_base}/search?query={link}"
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: requests.get(search_url).json())
            
            if response.get("status") == "SUCCESS" and response["data"]["results"]:
                stream_link = response["data"]["results"][0]["downloadUrl"][-1]["link"]
                return 1, stream_link
            return 0, "No Link Found"
        except Exception as e:
            return 0, str(e)

    async def download(self, link: str, mystic, video=None, videoid=None, songaudio=None, songvideo=None, format_id=None, title=None) -> str:
        """Download logic (Direct Saavn Link)"""
        try:
            res = await self.video(link)
            if res[0] == 1:
                return res[1], True
            return None, False
        except Exception as e:
            logger.error(f"Download Error: {e}")
            return None, False

    # Playlist support (Optional: dummy returning empty list)
    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        return []

    # Slider support
    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        res = await self.details(link)
        if res:
            return res[0], res[1], res[3], res[4]
        return None
