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
        # Primary API and Backup API
        self.api_list = [
            "https://jiosaavn-apii.shivampatel425685.workers.dev",
            "https://saavn.me", # Backup API
            "https://jiosaavn-api-beta.vercel.app" # 2nd Backup
        ]
        self.regex = r"(?:youtube\.com|youtu\.be|saavn\.com|jiosaavn\.com)"
        self.base = "https://www.youtube.com/watch?v="

    def clean_query(self, query):
        """Faltu words ko hatane ke liye"""
        query = str(query).lower()
        # Remove extra symbols and common junk words
        junk_words = ["full code", "lyrics", "mp3", "download", "video", "audio", "»"]
        for word in junk_words:
            query = query.replace(word, "")
        return query.strip()

    def format_duration(self, seconds):
        try:
            seconds = int(seconds)
            mins = seconds // 60
            secs = seconds % 60
            return f"{mins:02d}:{secs:02d}", seconds
        except:
            return "03:30", 210

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        return bool(re.search(self.regex, link))

    async def url(self, message: Message) -> Union[str, None]:
        if message.entities:
            for entity in message.entities:
                if entity.type == MessageEntityType.URL:
                    return (message.text or message.caption)[entity.offset : entity.offset + entity.length]
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        search_query = self.clean_query(link)
        encoded_query = quote(search_query)
        
        default_res = (f"Searching: {search_query}", "00:00", 0, "https://telegra.ph/file/default_thumb.png", "none")

        # Try multiple APIs if one fails
        for api in self.api_list:
            try:
                search_url = f"{api}/search/songs?query={encoded_query}" if "saavn.me" in api else f"{api}/search?query={encoded_query}"
                
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, lambda: requests.get(search_url, timeout=5).json())
                
                if response.get("status") == "SUCCESS":
                    data = response.get("data")
                    results = data.get("results") if isinstance(data, dict) else data
                    
                    if results and len(results) > 0:
                        song = results[0]
                        title = song.get("name", "Unknown Song")
                        duration_str, duration_sec = self.format_duration(song.get("duration", 0))
                        images = song.get("image", [])
                        thumb = images[-1]["link"] if images else default_res[3]
                        vidid = song.get("id", "none")
                        return title, duration_str, duration_sec, thumb, vidid
            except Exception as e:
                logger.error(f"API {api} failed: {e}")
                continue # Try next API

        return default_res

    async def track(self, link: str, videoid: Union[bool, str] = None):
        res = await self.details(link, videoid)
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
        search_query = self.clean_query(link)
        encoded_query = quote(search_query)

        for api in self.api_list:
            try:
                search_url = f"{api}/search/songs?query={encoded_query}" if "saavn.me" in api else f"{api}/search?query={encoded_query}"
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, lambda: requests.get(search_url, timeout=5).json())
                
                if response.get("status") == "SUCCESS":
                    data = response.get("data")
                    results = data.get("results") if isinstance(data, dict) else data
                    if results and results[0].get("downloadUrl"):
                        return 1, results[0]["downloadUrl"][-1]["link"]
            except:
                continue
        return 0, "No Link Found"

    async def download(self, link: str, mystic, video=None, videoid=None, songaudio=None, songvideo=None, format_id=None, title=None) -> str:
        res = await self.video(link)
        if res[0] == 1:
            return res[1], True
        return None, False

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        return []

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        res = await self.details(link)
        return res[0], res[1], res[3], res[4]
