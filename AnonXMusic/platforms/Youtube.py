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
        # Stable APIs ka collection (Agar ek fail ho to dusri kaam karegi)
        self.api_list = [
            "https://saavn.dev",
            "https://jiosaavn-api-v3.vercel.app",
            "https://jiosaavn-apii.shivampatel425685.workers.dev"
        ]
        self.regex = r"(?:youtube\.com|youtu\.be|saavn\.com|jiosaavn\.com)"
        self.base = "https://www.youtube.com/watch?v="

    def clean_query(self, query):
        """Search query ko saaf karne ke liye taaki results achhe aayein"""
        query = str(query).lower()
        junk = ["full code", "lyrics", "mp3", "download", "video", "audio", "»", "song", "full video"]
        for word in junk:
            query = query.replace(word, "")
        return query.strip()

    def format_duration(self, seconds):
        """Duration ko convert karne ke liye"""
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

    async def fetch_data(self, url):
        """Background mein safely data fetch karne ke liye"""
        try:
            loop = asyncio.get_event_loop()
            # 7 seconds ka timeout taaki bot hang na ho
            response = await loop.run_in_executor(None, lambda: requests.get(url, timeout=7))
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            # DNS ya Connection error ko yahan handle kiya gaya hai
            return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        """Gaane ki saari details nikalna (Hamesha 5 values return karega)"""
        search_query = self.clean_query(link)
        encoded_query = quote(search_query)
        
        # Default data agar kuch na mile
        default_res = (f"{search_query}", "03:00", 180, "https://telegra.ph/file/default_thumb.png", "none")

        for api in self.api_list:
            search_url = f"{api}/api/search/songs?query={encoded_query}" if "saavn.dev" in api else f"{api}/search?query={encoded_query}"
            
            data = await self.fetch_data(search_url)
            if data and data.get("status") == "SUCCESS":
                results = data.get("data")
                if isinstance(results, dict): results = results.get("results")
                
                if results and len(results) > 0:
                    song = results[0]
                    title = song.get("name", "Unknown Song")
                    d_str, d_sec = self.format_duration(song.get("duration", 0))
                    images = song.get("image", [])
                    thumb = images[-1]["link"] if images else default_res[3]
                    vidid = str(song.get("id", "none"))
                    return title, d_str, d_sec, thumb, vidid
        
        return default_res

    async def track(self, link: str, videoid: Union[bool, str] = None):
        """Core play logic ke liye (Hamesha 2 values return karega)"""
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
        """Direct streaming link nikalne ke liye"""
        search_query = self.clean_query(link)
        encoded_query = quote(search_query)

        for api in self.api_list:
            search_url = f"{api}/api/search/songs?query={encoded_query}" if "saavn.dev" in api else f"{api}/search?query={encoded_query}"
            data = await self.fetch_data(search_url)
            
            if data and data.get("status") == "SUCCESS":
                results = data.get("data")
                if isinstance(results, dict): results = results.get("results")
                if results and results[0].get("downloadUrl"):
                    # 320kbps link
                    return 1, results[0]["downloadUrl"][-1]["link"]
        
        return 0, "No Link Found"

    async def download(self, link: str, mystic, video=None, videoid=None, songaudio=None, songvideo=None, format_id=None, title=None) -> str:
        """Download ke liye direct stream link bhejta hai"""
        res = await self.video(link)
        if res[0] == 1:
            return res[1], True
        return None, False

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        """Playlist support filhal band hai (YouTube API ke bina mushkil hai)"""
        return []

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        """Search slider ke liye"""
        res = await self.details(link)
        return res[0], res[1], res[3], res[4]
