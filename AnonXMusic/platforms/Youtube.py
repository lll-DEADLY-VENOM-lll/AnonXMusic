import asyncio
import requests
import re
import os
from typing import Union
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# Config se values uthane ke liye
import config
from AnonXMusic import LOGGER

logger = LOGGER(__name__)

class SaavnAPI:
    def __init__(self):
        # Aapka provided Cloudflare Worker link
        self.api_base = "https://jiosaavn-apii.shivampatel425685.workers.dev"
        self.regex = r"(?:saavn\.com|jiosaavn\.com)"

    def format_duration(self, seconds):
        """Seconds ko MM:SS mein convert karne ke liye"""
        try:
            seconds = int(seconds)
            mins = seconds // 60
            secs = seconds % 60
            return f"{mins:02d}:{secs:02d}", seconds
        except:
            return "00:00", 0

    async def exists(self, link: str):
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

    async def search_saavn(self, query: str):
        """API se gaana search karne ke liye"""
        try:
            search_url = f"{self.api_base}/search?query={query.replace(' ', '+')}"
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: requests.get(search_url).json())
            
            if response.get("status") == "SUCCESS" and response["data"]["results"]:
                return response["data"]["results"][0] # Pehla result return karega
            return None
        except Exception as e:
            logger.error(f"Saavn Search Error: {e}")
            return None

    async def details(self, query: str):
        """AnonXMusic ke format mein details nikalna"""
        song = await self.search_saavn(query)
        if not song:
            return None

        title = song["name"]
        duration_str, duration_sec = self.format_duration(song["duration"])
        thumb = song["image"][-1]["link"] # Best quality image
        vidid = song["id"]
        # Stream link (Highest quality: 320kbps)
        stream_link = song["downloadUrl"][-1]["link"]
        
        return title, duration_str, duration_sec, thumb, vidid, stream_link

    async def track(self, query: str):
        res = await self.details(query)
        if not res:
            return None, None
        title, d_min, d_sec, thumb, vidid, stream_link = res
        track_details = {
            "title": title,
            "link": stream_link, # Ab ye direct mp4/m4a link hai
            "vidid": vidid,
            "duration_min": d_min,
            "thumb": thumb,
        }
        return track_details, vidid

    async def stream_link(self, query: str):
        """Voice chat mein play karne ke liye direct link"""
        res = await self.details(query)
        if res:
            return 1, res[5] # Index 5 is the stream_link
        return 0, "Not Found"

    async def download(self, query: str, title: str):
        """Gaana download karne ke liye (Aise hi bina yt-dlp ke)"""
        res = await self.details(query)
        if not res:
            return None, False
        
        stream_url = res[5]
        file_path = f"downloads/{title}.mp3"
        
        def download_file():
            r = requests.get(stream_url, stream=True)
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: f.write(chunk)
            return file_path

        loop = asyncio.get_event_loop()
        downloaded_file = await loop.run_in_executor(None, download_file)
        return downloaded_file, True

# Class usage update
Saavn = SaavnAPI()
