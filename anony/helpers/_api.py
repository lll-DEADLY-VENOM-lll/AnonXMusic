# Optimized for Ultra-Fast Performance by AI
# Improved Stability and Error Handling

import os
import re
import asyncio
import urllib.parse
from dataclasses import dataclass
from typing import Optional

import aiohttp
import aiofiles
from anony import app, logger

@dataclass(slots=True)
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
        # Fast Timeout: 5s connection, 25s total download for larger files
        self.timeout = aiohttp.ClientTimeout(total=25, connect=5)
        self.session: Optional[aiohttp.ClientSession] = None
        self.headers = {
            "X-API-Key": self.api_key,
            "Accept": "application/json",
            "User-Agent": "FallenMusicBot/1.0",
        }
        # Ensure download directory exists
        os.makedirs("downloads", exist_ok=True)

    async def get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            # TCPConnector tuning: limit=0 (unlimited), use_dns_cache for speed
            connector = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300, use_dns_cache=True)
            self.session = aiohttp.ClientSession(
                connector=connector, 
                timeout=self.timeout,
                headers=self.headers
            )
        return self.session

    async def get_track(self, url: str) -> Optional[MusicTrack]:
        encoded_url = urllib.parse.quote(url)
        endpoint = f"{self.api_url}/api/track?url={encoded_url}"
        session = await self.get_session()

        for attempt in range(self.retries):
            try:
                async with session.get(endpoint) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return MusicTrack.from_dict(data)
                    elif resp.status == 429:
                        await asyncio.sleep(1.5) # Rate limit cooling
                    else:
                        logger.warning(f"API Error: {resp.status} on attempt {attempt + 1}")
            except Exception as e:
                logger.error(f"Track Fetch Attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(0.5)
        return None

    async def download_cdn(self, cdn_url: str, video_id: str) -> Optional[str]:
        session = await self.get_session()
        try:
            async with session.get(cdn_url) as resp:
                if resp.status != 200:
                    logger.error(f"CDN returned status {resp.status}")
                    return None

                # Extract filename from headers or default to video_id
                filename = f"{video_id}.mp3"
                cd = resp.headers.get("Content-Disposition")
                if cd and "filename=" in cd:
                    found = re.findall(r'filename="?([^";]+)"?', cd)
                    if found:
                        filename = found[0]

                save_path = os.path.join("downloads", filename)
                
                # Using 256KB chunks for faster I/O on modern systems
                async with aiofiles.open(save_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(256 * 1024):
                        await f.write(chunk)
                return save_path
        except Exception as e:
            logger.error(f"CDN Download Error: {e}")
            return None

    async def download_track(self, video_id: str) -> Optional[str]:
        yt_url = f"https://www.youtube.com/watch?v={video_id}"
        track = await self.get_track(yt_url)
        
        if not track or not track.cdnurl:
            logger.error(f"Could not retrieve track info for {video_id}")
            return None

        # Enhanced Telegram Link Parsing
        tg_match = re.match(r"https?://t\.me/(?:c/)?([^/]+)/(\d+)", track.cdnurl)
        if tg_match:
            try:
                chat_id = tg_match.group(1)
                msg_id = int(tg_match.group(2))
                
                # Handle Private Channel IDs (prefixed with -100)
                if chat_id.isdigit():
                    chat_id = int(f"-100{chat_id}")
                
                msg = await app.get_messages(chat_id, msg_id)
                if msg and (msg.audio or msg.voice or msg.video or msg.document):
                    file_path = await msg.download(file_name=f"downloads/{video_id}_tg")
                    return file_path
            except Exception as e:
                logger.error(f"Telegram Download Error: {e}")
                # Fallback to CDN if Telegram fetch fails
                pass

        return await self.download_cdn(track.cdnurl, video_id)

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
