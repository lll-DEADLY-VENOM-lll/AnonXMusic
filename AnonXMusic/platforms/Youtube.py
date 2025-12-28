import asyncio
import os
import re
import yt_dlp
from typing import Union
from pyrogram.types import Message
from pyrogram.enums import MessageEntityType
from ytmusicapi import YTMusic

from AnonXMusic.utils.database import is_on_off
from AnonXMusic.utils.formatters import time_to_seconds

# Global instance for YTMusic
yt_music = YTMusic()

# Ensure downloads folder exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# --- Dummy function to satisfy ImportErrors in call.py ---
def cookie_txt_file():
    return None # No folder or file needed

async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        if "unavailable videos are hidden" in (errorz.decode("utf-8")).lower():
            return out.decode("utf-8")
        else:
            return errorz.decode("utf-8")
    return out.decode("utf-8")

async def get_local_stream(link, video=False):
    loop = asyncio.get_running_loop()
    def extract():
        ydl_opts = {
            "format": "best[height<=?720]" if video else "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "nocheckcertificate": True,
            "cachedir": False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(link, download=False)
                return info.get("url")
            except Exception:
                return None
    
    return await loop.run_in_executor(None, extract)

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        if re.search(self.regex, link): return True
        return False

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text, offset, length = "", None, None
        for message in messages:
            if offset: break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        if offset is None: return None
        return text[offset : offset + length]

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        if "&" in link: link = link.split("&")[0]
        
        search = await asyncio.to_thread(yt_music.search, link, filter="songs", limit=1)
        if not search: return None
        
        res = search[0]
        title = res["title"]
        duration_min = res.get("duration", "04:00")
        thumbnail = res["thumbnails"][-1]["url"].split("?")[0]
        vidid = res["videoId"]
        duration_sec = int(time_to_seconds(duration_min))
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        res = await self.details(link, videoid)
        return res[0] if res else "Unknown Title"

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        res = await self.details(link, videoid)
        return res[1] if res else "00:00"

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        res = await self.details(link, videoid)
        return res[3] if res else None

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        url = await get_local_stream(link, video=True)
        return (1, url) if url else (0, "Error")

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid: link = self.listbase + link
        playlist = await shell_cmd(f"yt-dlp -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}")
        return [k for k in playlist.split("\n") if k != ""]

    async def track(self, link: str, videoid: Union[bool, str] = None):
        res = await self.details(link, videoid)
        if not res: return None, None
        title, duration_min, duration_sec, thumbnail, vidid = res
        track_details = {
            "title": title, "link": self.base + vidid, "vidid": vidid,
            "duration_min": duration_min, "thumb": thumbnail,
        }
        return track_details, vidid

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        search = await asyncio.to_thread(yt_music.search, link, filter="songs", limit=10)
        res = search[query_type]
        return res["title"], res.get("duration", "00:00"), res["thumbnails"][-1]["url"], res["videoId"]

    async def download(self, link: str, mystic, video=None, videoid=None, songaudio=None, songvideo=None, format_id=None, title=None):
        if videoid: link = self.base + link
        loop = asyncio.get_running_loop()

        if songvideo:
            fpath = f"downloads/{title}.mp4"
            def dl_v():
                with yt_dlp.YoutubeDL({"format": f"{format_id}+140", "outtmpl": f"downloads/{title}", "merge_output_format": "mp4", "quiet": True}) as ydl:
                    ydl.download([link])
            await loop.run_in_executor(None, dl_v)
            return fpath
        
        elif songaudio:
            fpath = f"downloads/{title}.mp3"
            def dl_a():
                opts = {"format": format_id, "outtmpl": f"downloads/{title}.%(ext)s", "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}], "quiet": True}
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([link])
            await loop.run_in_executor(None, dl_a)
            return fpath
        
        direct_url = await get_local_stream(link, video=bool(video))
        return direct_url, True