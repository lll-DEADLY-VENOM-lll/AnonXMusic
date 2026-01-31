import asyncio
import requests
import re
from typing import Union
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from urllib.parse import quote

import config
from AnonXMusic import LOGGER

logger = LOGGER(__name__)

class YouTubeAPI:
    def __init__(self):
        self.api_base = "https://jiosaavn-apii.shivampatel425685.workers.dev"
        self.regex = r"(?:youtube\.com|youtu\.be|saavn\.com|jiosaavn\.com)"
        self.base = "https://www.youtube.com/watch?v="

    def format_duration(self, seconds):
        try:
            seconds = int(seconds)
            mins = seconds // 60
            secs = seconds % 60
            return f"{mins:02d}:{secs:02d}", seconds
        except:
            return "00:00", 0

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        return bool(re.search(self.regex, link))

    async def url(self, message: Message) -> Union[str, None]:
        if message.entities:
            for entity in message.entities:
                if entity.type == MessageEntityType.URL:
                    return (message.text or message.caption)[entity.offset : entity.offset + entity.length]
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        """Hamesha 5 values return karega, chahe gaana mile ya na mile"""
        default_res = ("Unknown Song", "00:00", 0, "https://telegra.ph/file/default_thumb.png", "none")
        try:
            # Clean search query
            search_query = quote(str(link).split("»")[0].strip()) 
            search_url = f"{self.api_base}/search?query={search_query}"
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: requests.get(search_url, timeout=10).json())
            
            if response.get("status") == "SUCCESS":
                data = response.get("data")
                results = data.get("results") if isinstance(data, dict) else data
                
                if results and len(results) > 0:
                    song = results[0]
                    title = song.get("name", "Unknown")
                    duration_str, duration_sec = self.format_duration(song.get("duration", 0))
                    images = song.get("image", [])
                    thumb = images[-1]["link"] if images else default_res[3]
                    vidid = song.get("id", "none")
                    return title, duration_str, duration_sec, thumb, vidid
            
            logger.warning(f"No results found for: {link}")
            return default_res
        except Exception as e:
            logger.error(f"Details Error: {e}")
            return default_res

    async def track(self, link: str, videoid: Union[bool, str] = None):
        """Hamesha 2 values return karega"""
        title, d_min, d_sec, thumb, vidid = await self.details(link, videoid)
        track_details = {
            "title": title,
            "link": link,
            "vidid": vidid,
            "duration_min": d_min,
            "thumb": thumb,
        }
        return track_details, vidid

    async def video(self, link: str, videoid: Union[bool, str] = None):
        """Gaane ka streaming link nikalne ke liye"""
        try:
            search_query = quote(str(link).split("»")[0].strip())
            search_url = f"{self.api_base}/search?query={search_query}"
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: requests.get(search_url, timeout=10).json())
            
            if response.get("status") == "SUCCESS":
                data = response.get("data")
                results = data.get("results") if isinstance(data, dict) else data
                if results and results[0].get("downloadUrl"):
                    return 1, results[0]["downloadUrl"][-1]["link"]
            return 0, "No Link Found"
        except Exception as e:
            return 0, str(e)

    async def download(self, link: str, mystic, video=None, videoid=None, songaudio=None, songvideo=None, format_id=None, title=None) -> str:
        res = await self.video(link)
        if res[0] == 1:
            return res[1], True
        return None, False

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        return []

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        res = await self.details(link)
        # Hamesha 4 values return karega slider ke liye
        return res[0], res[1], res[3], res[4]
