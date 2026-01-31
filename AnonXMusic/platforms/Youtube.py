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
            return "03:30", 210 # Default duration if fails

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        return bool(re.search(self.regex, link))

    async def url(self, message: Message) -> Union[str, None]:
        if message.entities:
            for entity in message.entities:
                if entity.type == MessageEntityType.URL:
                    return (message.text or message.caption)[entity.offset : entity.offset + entity.length]
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        try:
            # URL Encoding taaki special characters se error na aaye
            search_query = quote(link)
            search_url = f"{self.api_base}/search?query={search_query}"
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: requests.get(search_url).json())
            
            # API Response structure check
            if response.get("status") == "SUCCESS":
                data = response.get("data")
                # Kuch versions mein data['results'] hota hai, kuch mein direct data list hoti hai
                results = data.get("results") if isinstance(data, dict) else data
                
                if results and len(results) > 0:
                    song = results[0]
                    title = song.get("name", "Unknown Song")
                    duration_str, duration_sec = self.format_duration(song.get("duration", 0))
                    
                    # Image quality check
                    images = song.get("image", [])
                    thumb = images[-1]["link"] if images else "https://telegra.ph/file/default_thumb.png"
                    
                    vidid = song.get("id", "12345")
                    return title, duration_str, duration_sec, thumb, vidid
            
            logger.warning(f"No results found for: {link}")
            return None
        except Exception as e:
            logger.error(f"Error in details: {e}")
            return None

    async def track(self, link: str, videoid: Union[bool, str] = None):
        res = await self.details(link, videoid)
        if not res:
            # AGAR GAANA NA MILE, TO ERROR SE BACHNE KE LIYE DUMMY DATA
            return {
                "title": "Song Not Found",
                "link": link,
                "vidid": "none",
                "duration_min": "00:00",
                "thumb": "https://telegra.ph/file/default_thumb.png",
            }, "none"
            
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
        try:
            search_query = quote(link)
            search_url = f"{self.api_base}/search?query={search_query}"
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: requests.get(search_url).json())
            
            if response.get("status") == "SUCCESS":
                data = response.get("data")
                results = data.get("results") if isinstance(data, dict) else data
                if results:
                    download_urls = results[0].get("downloadUrl", [])
                    if download_urls:
                        # Sabse high quality link (320kbps)
                        return 1, download_urls[-1]["link"]
            return 0, "No Link"
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
        if res:
            return res[0], res[1], res[3], res[4]
        return None
