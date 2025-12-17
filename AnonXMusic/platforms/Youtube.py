import asyncio
import httpx
import yt_dlp
import os
import glob
import re
import random
import json
import requests
from typing import Union
from pyrogram.types import Message
from pyrogram.enums import MessageEntityType
from youtubesearchpython.__future__ import VideosSearch, CustomSearch
from AnonXMusic.utils.formatters import time_to_seconds

# Fixed: Renamed function variable to avoid shadowing function name inside
def cookie_txt_file():
    try:
        folder_path = f"{os.getcwd()}/cookies"
        filename = f"{os.getcwd()}/cookies/logs.csv"
        txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
        if not txt_files:
            raise FileNotFoundError("No .txt files found in the specified folder.")
        
        selected_cookie = random.choice(txt_files)
        
        with open(filename, 'a') as file:
            file.write(f'Choosen File : {selected_cookie}\n')
            
        return f"""cookies/{str(selected_cookie).split("/")[-1]}"""
    except:
        return None

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

async def get_stream_url(query, video=False):
    # API configuration
    apis = [
        {
            "url": "https://api.vniox.store/youtube",
            "key": "VNI0X_7nfdc0Ox6kbWoyF" 
        },
        {
            "url": "https://api.vniox.store/youtube",
            "key": "VNI0X_7nfdc0Ox6kbWoyF" 
        }
    ]

    async with httpx.AsyncClient(timeout=60) as client:
        for api in apis:
            try:
                params = {"query": query, "video": video, "api_key": api["key"]}
                response = await client.get(api["url"], params=params)

                if response.status_code == 200:
                    info = response.json()
                    stream_url = info.get("stream_url")
                    if stream_url:
                        return stream_url
            except Exception:
                continue
    return ""

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if re.search(self.regex, link):
            return True
        else:
            return False

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
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
        if offset in (None,):
            return None
        return text[offset : offset + length]

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
            
        # FIX: Initialize variables to prevent UnboundLocalError/NameError
        title = None
        duration_min = "00:00"
        duration_sec = 0
        thumbnail = ""
        vidid = ""

        try:
            results = VideosSearch(link, limit=1)
            search_result = (await results.next())
            if search_result and "result" in search_result and search_result["result"]:
                for result in search_result["result"]:
                    title = result["title"]
                    duration_min = result["duration"]
                    thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                    vidid = result["id"]
                    if str(duration_min) == "None":
                        duration_sec = 0
                    else:
                        duration_sec = int(time_to_seconds(duration_min))
        except Exception as e:
            print(f"Error in details: {e}")
            
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        # FIX: Initialize variable
        title = None
        try:
            results = VideosSearch(link, limit=1)
            search_result = (await results.next())
            if search_result and "result" in search_result and search_result["result"]:
                for result in search_result["result"]:
                    title = result["title"]
        except:
            pass
        return title

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
            
        # FIX: Initialize variable
        duration = None
        try:
            results = VideosSearch(link, limit=1)
            search_result = (await results.next())
            if search_result and "result" in search_result and search_result["result"]:
                for result in search_result["result"]:
                    duration = result["duration"]
        except:
            pass
        return duration

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
            
        # FIX: Initialize variable
        thumbnail = None
        try:
            results = VideosSearch(link, limit=1)
            search_result = (await results.next())
            if search_result and "result" in search_result and search_result["result"]:
                for result in search_result["result"]:
                    thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        except:
            pass
        return thumbnail

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        return await get_stream_url(link, True)

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        playlist = await shell_cmd(
            f"yt-dlp -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}"
        )
        try:
            result = playlist.split("\n")
            for key in result:
                if key == "":
                    result.remove(key)
        except:
            result = []
        return result

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
            
        # FIX: Initialize variables
        title = None
        duration_min = "00:00"
        vidid = ""
        yturl = ""
        thumbnail = ""
        
        try:
            results = VideosSearch(link, limit=1)
            search_result = (await results.next())
            if search_result and "result" in search_result and search_result["result"]:
                for result in search_result["result"]:
                    title = result["title"]
                    duration_min = result["duration"]
                    vidid = result["id"]
                    yturl = result["link"]
                    thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        except:
            pass
            
        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details, vidid

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        ytdl_opts = {"quiet": True}
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            try:
                r = ydl.extract_info(link, download=False)
                for format in r["formats"]:
                    try:
                        str(format["format"])
                    except:
                        continue
                    if not "dash" in str(format["format"]).lower():
                        try:
                            format["format"]
                            format["filesize"]
                            format["format_id"]
                            format["ext"]
                            format["format_note"]
                        except:
                            continue
                        formats_available.append(
                            {
                                "format": format["format"],
                                "filesize": format["filesize"],
                                "format_id": format["format_id"],
                                "ext": format["ext"],
                                "format_note": format["format_note"],
                                "yturl": link,
                            }
                        )
            except:
                pass
        return formats_available, link

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
            
        try:
            a = VideosSearch(link, limit=10)
            search_result = (await a.next())
            if search_result and "result" in search_result:
                result = search_result.get("result")
                title = result[query_type]["title"]
                duration_min = result[query_type]["duration"]
                vidid = result[query_type]["id"]
                thumbnail = result[query_type]["thumbnails"][0]["url"].split("?")[0]
                return title, duration_min, thumbnail, vidid
        except:
            pass
        return None, None, None, None

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
        if videoid:
            link = self.base + link
        loop = asyncio.get_running_loop()

        def audio_dl():
            ydl_optssx = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def video_dl():
            ydl_optssx = {
                "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def song_video_dl():
            formats = f"{format_id}+140"
            fpath = f"downloads/{title}"
            ydl_optssx = {
                "format": formats,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "merge_output_format": "mp4",
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            x.download([link])

        def song_audio_dl():
            fpath = f"downloads/{title}.%(ext)s"
            ydl_optssx = {
                "format": format_id,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            x.download([link])

        try:
            if songvideo:
                await loop.run_in_executor(None, song_video_dl)
                fpath = f"downloads/{title}.mp4"
                return fpath
            elif songaudio:
                await loop.run_in_executor(None, song_audio_dl)
                fpath = f"downloads/{title}.mp3"
                return fpath
            elif video:
                downloaded_file = await get_stream_url(link, True)
                direct = None
            else:
                direct = None
                downloaded_file = await get_stream_url(link, False)
                
            # Fallback if API returns empty
            if not downloaded_file:
                if video:
                     downloaded_file = await loop.run_in_executor(None, video_dl)
                else:
                     downloaded_file = await loop.run_in_executor(None, audio_dl)
                
            return downloaded_file, direct
        except Exception as e:
            return "", None