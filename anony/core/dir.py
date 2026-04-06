# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import shutil
from pathlib import Path
from anony import logger

def ensure_dirs():
    """
    Ensure that the necessary directories exist.
    """
    # Check if Deno and FFmpeg are installed, but don't stop the bot
    if not shutil.which("deno"):
        logger.warning("Deno is not installed. Some features might not work.")
    
    if not shutil.which("ffmpeg"):
        logger.warning("FFmpeg is not installed. Music playback will fail.")

    # Create necessary directories
    for directory in ["cache", "downloads"]:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    logger.info("Cache and Downloads directories updated.")

# Is code ko save karne ke baad bot ko restart karein.
