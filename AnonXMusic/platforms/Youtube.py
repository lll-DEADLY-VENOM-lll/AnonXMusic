import asyncio
import yt_dlp
import os
import re
from typing import Union
from pyrogram.types import Message
from pyrogram.enums import MessageEntityType
from ytmusicapi import YTMusic
from AnonXMusic.utils.formatters import time_to_seconds

# YTMusic initialize
ytm = YTMusic()

async def get_stream_url(link, video=False):
    loop = asyncio.get_running_loop()
    def extract():
        # Bina cookies ke chalane ke liye advanced options
        ydl_opts = {
            "format": "bestaudio/best" if not video else "bestvideo[height<=?720]+bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            # YouTube ko dhoka dene ke liye Fake User Agent aur Client
            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            "http_headers": {
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
            },
            # Isse YouTube ko lagta hai ki ye Official Android App hai
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "ios"],
                    "skip": ["dash", "hls"]
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(link, download=False)
                return info['url']
            except Exception as e:
                print(f"Streaming Error: {e}")
                return None
    return await loop.run_in_executor(None, extract)

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be|music\.youtube\.com)"

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        return bool(re.search(self.regex, link))

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        loop = asyncio.get_running_loop()
        
        # YouTube Music Search Logic
        if "http" not in link:
            search = await loop.run_in_executor(None, lambda: ytm.search(link, filter="songs"))
            if not search: # Fallback if no song found
                search = await loop.run_in_executor(None, lambda: ytm.search(link))
            
            item = search[0]
            vidid = item['videoId']
            title = item['title']
            duration_min = item.get('duration', "0:00")
            thumbnail = item['thumbnails'][-1]['url']
        else:
            # Link se metadata nikalna
            vidid = link.split("v=")[1].split("&")[0] if "v=" in link else link.split("/")[-1]
            try:
                data = await loop.run_in_executor(None, lambda: ytm.get_song(vidid))
                title = data['videoDetails']['title']
                duration_sec = int(data['videoDetails']['lengthSeconds'])
                duration_min = f"{duration_sec // 60}:{duration_sec % 60:02d}"
                thumbnail = data['videoDetails']['thumbnail']['thumbnails'][-1]['url']
            except:
                title, duration_min, _, thumbnail, vidid = "Unknown", "0:00", 0, "", vidid

        duration_sec = int(time_to_seconds(duration_min))
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        res = await self.details(link, videoid)
        return res[0]

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        return await get_stream_url(link, video=True)

    async def track(self, link: str, videoid: Union[bool, str] = None):
        title, duration_min, _, thumbnail, vidid = await self.details(link, videoid)
        return {
            "title": title,
            "link": self.base + vidid,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }, vidid

    async def download(self, link: str, mystic, video=None, videoid=None, songaudio=None, songvideo=None, format_id=None, title=None):
        if videoid: link = self.base + link
        if not (songaudio or songvideo):
            # Music Playback ke liye Direct Stream Link
            return await get_stream_url(link, video=bool(video)), None
        
        # Download logic agar koi manual download kare
        loop = asyncio.get_running_loop()
        def dl():
            ext = "mp4" if songvideo else "mp3"
            fpath = f"downloads/{title}.{ext}"
            opts = {"format": "bestaudio/best" if songaudio else "bestvideo+bestaudio", "outtmpl": fpath.replace(f".{ext}", ""), "quiet": True}
            if songaudio: opts["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]
            with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([link])
            return fpath
        return await loop.run_in_executor(None, dl)