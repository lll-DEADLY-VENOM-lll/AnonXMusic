# Written by #fuck you
# Optimized for Ultra-Fast Performance by AI

import os
import re
import asyncio
import urllib.parse
from dataclasses import dataclass
from typing import Optional

import aiohttp
import aiofiles
from anony import app, logger

@dataclass(slots=True) # slots=True performance boost (memory efficient)
class MusicTrack:
    cdnurl: str
    url: str
    id: str
    key: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "MusicTrack":
        return cls(
            cdnurl=data.get("cdnurl", ""),
            url=data.get("url", ""),
            id=data.get("id", ""),
            key=data.get("key"),
        )

class FallenApi:
    def __init__(self, api_url: str, api_key: str, retries: int = 2):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.retries = retries
        # Fast Timeout: 5s connection, 15s total download
        self.timeout = aiohttp.ClientTimeout(total=20, connect=5)
        self.session: Optional[aiohttp.ClientSession] = None
        self.headers = {
            "X-API-Key": self.api_key,
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }

    async def get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            # TCPConnector tuning for speed
            connector = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300, use_dns_cache=True)
            self.session = aiohttp.ClientSession(
                connector=connector, 
                timeout=self.timeout,
                headers=self.headers
            )
        return self.session

    async def get_track(self, url: str) -> Optional[MusicTrack]:
        endpoint = f"{self.api_url}/api/track?url={urllib.parse.quote(url)}"
        session = await self.get_session()

        for attempt in range(self.retries):
            try:
                async with session.get(endpoint) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return MusicTrack.from_dict(data)
                    elif resp.status == 429: # Rate limit handling
                        await asyncio.sleep(1)
                    else:
                        logger.warning(f"API Error: Status {resp.status}")
            except Exception as e:
                logger.error(f"Attempt {attempt+1} failed: {e}")
                if attempt == self.retries - 1:
                    break
                await asyncio.sleep(0.5) # Fast retry
        return None

    async def download_cdn(self, cdn_url: str, video_id: str) -> Optional[str]:
        session = await self.get_session()
        try:
            async with session.get(cdn_url) as resp:
                if resp.status != 200:
                    return None

                # Extract filename from headers or URL
                cd = resp.headers.get("Content-Disposition")
                if cd and "filename=" in cd:
                    filename = re.findall(r'filename="?([^";]+)"?', cd)[0]
                else:
                    filename = f"{video_id}.mp3"

                save_path = os.path.join("downloads", filename)
                
                # Optimized for NVMe/Fast SSDs using 128KB chunks
                async with aiofiles.open(save_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(128 * 1024):
                        await f.write(chunk)
                return save_path
        except Exception as e:
            logger.error(f"CDN Download Error: {e}")
            return None

    async def download_track(self, video_id: str) -> Optional[str]:
        url = f"https://www.youtube.com/watch?v={video_id}"
        track = await self.get_track(url)
        if not track or not track.cdnurl:
            return None

        # Handling Telegram links properly
        # Example: https://t.me/c/1234567/890 or https://t.me/username/890
        tg_match = re.match(r"https?://t\.me/(?:c/)?([^/]+)/(\d+)", track.cdnurl)
        if tg_match:
            try:
                chat = tg_match.group(1)
                msg_id = int(tg_match.group(2))
                
                # If it's a private chat (starts with ID)
                if chat.isdigit():
                    chat = int(f"-100{chat}")
                
                msg = await app.get_messages(chat, msg_id)
                if msg.audio or msg.voice or msg.video or msg.document:
                    file_path = await msg.download(file_name=f"downloads/{video_id}")
                    return file_path
            except Exception as e:
                logger.error(f"Telegram Download Error: {e}")
                return None

        return await self.download_cdn(track.cdnurl, video_id)

    async def close(self):
        if self.session:
            await self.session.close()
