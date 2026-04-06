# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.

import os
import re
import yt_dlp
import random
import asyncio
import glob
from pathlib import Path
from py_yt import Playlist, VideosSearch

from anony import config, logger
from anony.helpers import FallenApi, Track, utils

if not os.path.exists("downloads"):
    os.mkdir("downloads")

class YouTube:
    def __init__(self):
        self.api = None
        self.base = "https://www.youtube.com/watch?v="
        self.cookies = []
        self.checked = False
        self.cookie_dir = "anony/cookies"
        self.warned = False
        
        self.regex = re.compile(
            r"^(https?://)?(www\.|m\.|music\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/|youtube\.com/playlist\?list=)([A-Za-z0-9_-]{11}|PL[A-Za-z0-9_-]+).*"
        )
        
        if not os.path.exists(self.cookie_dir):
            os.makedirs(self.cookie_dir)
            
        if config.API_URL and config.API_KEY:
            self.api = FallenApi(config.API_URL, config.API_KEY)

    def get_cookies(self):
        if not self.checked:
            if os.path.exists(self.cookie_dir):
                self.cookies = [
                    os.path.join(self.cookie_dir, f) 
                    for f in os.listdir(self.cookie_dir) if f.endswith(".txt")
                ]
            self.checked = True
        return random.choice(self.cookies) if self.cookies else None

    async def search(self, query: str, m_id: int, video: bool = False) -> Track | None:
        try:
            _search = VideosSearch(query, limit=1)
            results = await _search.next()
            if not results or not results.get("result"):
                return None
            data = results["result"][0]
            return Track(
                id=data.get("id"),
                channel_name=data.get("channel", {}).get("name"),
                duration=data.get("duration"),
                duration_sec=utils.to_seconds(data.get("duration")),
                message_id=m_id,
                title=data.get("title")[:50],
                thumbnail=data.get("thumbnails", [{}])[-1].get("url").split("?")[0],
                url=data.get("link"),
                view_count=data.get("viewCount", {}).get("short"),
                video=video,
            )
        except Exception as e:
            logger.error(f"Search Error: {e}")
            return None

    async def download(self, video_id: str, video: bool = False) -> str | None:
        if self.api:
            try:
                if file_path := await self.api.download_track(video_id):
                    return file_path
            except: pass

        # Cache check: agar file pehle se hai (kisi bhi extension mein)
        search_path = glob.glob(f"downloads/{video_id}.*")
        if search_path:
            return search_path[0]

        url = self.base + video_id
        cookie = self.get_cookies()
        
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "cookiefile": cookie,
            "format": "bestaudio/best" if not video else "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "outtmpl": f"downloads/{video_id}.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
            "retries": 2,
        }

        def _download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([url])
                    # Download ke baad check karein ki file kis extension se save hui
                    downloaded_files = glob.glob(f"downloads/{video_id}.*")
                    if downloaded_files:
                        return downloaded_files[0]
                    return None
                except Exception as e:
                    logger.error(f"yt-dlp Download Error: {e}")
                    return None

        return await asyncio.to_thread(_download)

    async def playlist(self, limit: int, user: str, url: str, video: bool) -> list:
        tracks = []
        try:
            plist = await Playlist.get(url)
            for data in plist.get("videos", [])[:limit]:
                track = Track(
                    id=data.get("id"),
                    channel_name=data.get("channel", {}).get("name", "Unknown"),
                    duration=data.get("duration"),
                    duration_sec=utils.to_seconds(data.get("duration")),
                    title=data.get("title")[:50],
                    thumbnail=data.get("thumbnails")[-1].get("url").split("?")[0],
                    url=data.get("link").split("&list=")[0],
                    user=user,
                    video=video,
                )
                tracks.append(track)
        except Exception as e:
            logger.error(f"Playlist Error: {e}")
        return tracks
