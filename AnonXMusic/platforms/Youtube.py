import asyncio
import yt_dlp
import os
import glob
import re
import random
from typing import Union
from pyrogram.types import Message
from pyrogram.enums import MessageEntityType
from ytmusicapi import YTMusic

from AnonXMusic.utils.formatters import time_to_seconds

# YTMusic instance initialize karein (Bina headers ke works fine)
ytm = YTMusic()

def cookie_txt_file():
    try:
        folder_path = f"{os.getcwd()}/cookies"
        txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
        if not txt_files:
            return None
        return random.choice(txt_files)
    except:
        return None

async def get_stream_url(link, video=False):
    loop = asyncio.get_running_loop()
    def extract():
        ydl_opts = {
            "format": "bestaudio/best" if not video else "bestvideo[height<=?720]+bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
        }
        cookie_file = cookie_txt_file()
        if cookie_file:
            ydl_opts["cookiefile"] = cookie_file

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(link, download=False)
                return info['url']
            except:
                return None
    return await loop.run_in_executor(None, extract)

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be|music\.youtube\.com)"
        self.listbase = "https://youtube.com/playlist?list="

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[entity.offset : entity.offset + entity.length]
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        
        # Agar link hai toh direct details nikalo, agar query hai toh search karo
        if "index=" in link: link = link.split("index=")[0]
        
        loop = asyncio.get_running_loop()
        if "http" in link:
            # Extract ID from link
            vidid = link.split("v=")[1].split("&")[0] if "v=" in link else link.split("/")[-1]
            data = await loop.run_in_executor(None, lambda: ytm.get_song(vidid))
            # YTMusic metadata mapping
            title = data['videoDetails']['title']
            duration_sec = int(data['videoDetails']['lengthSeconds'])
            duration_min = f"{duration_sec // 60}:{duration_sec % 60:02d}"
            thumbnail = data['videoDetails']['thumbnail']['thumbnails'][-1]['url']
        else:
            # Search logic using YTMusic
            search_results = await loop.run_in_executor(None, lambda: ytm.search(link, filter="songs"))
            item = search_results[0]
            title = item['title']
            vidid = item['videoId']
            duration_min = item.get('duration', "0:00")
            duration_sec = time_to_seconds(duration_min)
            thumbnail = item['thumbnails'][-1]['url']

        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        title, _, _, _, _ = await self.details(link, videoid)
        return title

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        _, duration_min, _, _, _ = await self.details(link, videoid)
        return duration_min

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        _, _, _, thumbnail, _ = await self.details(link, videoid)
        return thumbnail

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        return await get_stream_url(link, video=True)

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid: link = self.listbase + link
        cmd = f"yt-dlp -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}"
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, _ = await proc.communicate()
        return [key for key in stdout.decode().split("\n") if key]

    async def track(self, link: str, videoid: Union[bool, str] = None):
        title, duration_min, _, thumbnail, vidid = await self.details(link, videoid)
        track_details = {
            "title": title,
            "link": self.base + vidid,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details, vidid

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid: link = self.base + link
        
        if not (songaudio or songvideo):
            # Normal streaming for AnonX
            stream_url = await get_stream_url(link, video=bool(video))
            return stream_url, None

        # Actual Download logic
        loop = asyncio.get_running_loop()
        def download_file():
            extension = "mp4" if songvideo else "mp3"
            fpath = f"downloads/{title}.{extension}"
            ydl_opts = {
                "format": format_id if format_id else ("bestaudio/best" if songaudio else "bestvideo+bestaudio"),
                "outtmpl": fpath.replace(f".{extension}", ""),
                "quiet": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
            }
            if songaudio:
                ydl_opts["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}]
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            return fpath

        return await loop.run_in_executor(None, download_file)