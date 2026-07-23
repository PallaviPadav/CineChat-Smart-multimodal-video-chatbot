"""

Downloads a YouTube video, trims the required segment using FFmpeg,
and stores the video along with its metadata.

"""

import json
import subprocess
from pathlib import Path

from yt_dlp import YoutubeDL

from config import config
from Code.utils.logger import get_logger


def save_metadata(metadata: dict) -> None:
    """
    Save downloaded video metadata as a JSON file.

    Parameters
    ----------
    metadata : dict
        Metadata extracted from the downloaded video.
    """
    save_path = Path(config.VIDEO_METADATA_PATH)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)


def trim_video(input_file, output_file, start_time, end_time):
    """
    Trim video using ffmpeg.
    """

    cmd = [
        "ffmpeg",
        "-y",  # overwrite
        "-ss",
        str(start_time),
        "-to",
        str(end_time),
        "-i",
        str(input_file),
        "-c",
        "copy",
        str(output_file),
    ]

    subprocess.run(cmd, check=True)


def download_video(video_url: str) -> str | None:
    """
    Download a YouTube video, trim the required segment,
    and save the metadata.

    Parameters
    ----------
    video_url : str
        URL of the YouTube video.

    Returns
    -------
    str | None
        Path to the trimmed video if successful,
        otherwise None.
    """

    log = get_logger(__name__)

    output_path = Path(config.VIDEO_DOWNLOAD_PATH)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # temporary full video
    full_video = output_path.parent / "full_video.mp4"

    # remove old files
    for f in [output_path, full_video]:
        if f.exists():
            f.unlink()
            log.info("removed old video file before creation.")

    ydl_opts = {
        "format": "bv*+ba/best",
        "merge_output_format": "mp4",
        "outtmpl": str(full_video),
        "overwrites": True,
        "quiet": False,
        "ffmpeg_location": r"C:\Users\DELL\anaconda3\envs\irag\Library\bin",
    }

    log.info("Started downloading video: %s", video_url)
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)

        metadata = {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "channel": info.get("uploader"),
            "description": info.get("description"),
            "video_path": str(output_path),
        }

        save_metadata(metadata)

        log.info("Download completed.")

        # ==============================================
        # Trim only required segment
        # ==============================================

        log.info("Trimming video...")

        trim_video(full_video, output_path, start_time=220, end_time=445)

        # delete full video
        if full_video.exists():
            full_video.unlink()

        if not output_path.exists():
            log.error("Trimmed video not found.")
            return None

        if output_path.stat().st_size == 0:
            log.error("Trimmed video is empty.")
            return None

        log.info("Saved video: %s", output_path)

        log.info(
            "Size: %.2f MB",
            output_path.stat().st_size / (1024 * 1024),
        )

        return str(output_path)

    except Exception as e:
        log.exception("Download failed: %s", e)
        return None
