"""

Converts a video into text by extracting audio using MoviePy
and transcribing it with the Groq Whisper model.

"""

import os

from dotenv import load_dotenv
from groq import Groq
from moviepy.video.io.VideoFileClip import VideoFileClip

from config import config
from Code.utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

video_path = config.VIDEO_DOWNLOAD_PATH
audio_path = config.AUDIO_PATH
text_path = config.TEXT_PATH


def video_to_audio(video_path, audio_path):
    """Convert video to audio."""

    clip = VideoFileClip(str(video_path))

    try:
        clip.audio.write_audiofile(str(audio_path), logger=None)

    except Exception as e:
        logger.exception(
            "Error during video-to-audio conversion: %s",
            e,
        )
        raise
    finally:
        if clip.audio is not None:
            clip.audio.close()

        clip.close()

        logger.info("Video to audio conversion completed.")


def audio_to_text(audio_path):
    """Convert audio to text using Groq Whisper."""

    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found. Please add it to your .env file.")

    client = Groq(api_key=groq_api_key, timeout=300.0)

    try:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if os.path.getsize(audio_path) == 0:
            raise ValueError("Audio file is empty.")

        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file, model="whisper-large-v3"
            )

        logger.info("Audio transcription completed.")
        return transcription.text

    except Exception as e:
        logger.exception(
            "Error during audio transcription: %s",
            e,
        )
        raise


def video_to_text():
    """Complete pipeline: Video -> Audio -> Text"""

    try:
        logger.info("Starting video-to-audio conversion...")
        video_to_audio(video_path, audio_path)

        logger.info("Starting audio-to-text conversion...")
        text_transcript = audio_to_text(audio_path)

        text_path.parent.mkdir(parents=True, exist_ok=True)

        with open(text_path, "w", encoding="utf-8") as file:
            file.write(text_transcript)

        logger.info(
            "Transcript saved successfully at: %s",
            text_path,
        )

        return text_transcript

    except Exception as e:
        logger.exception(
            "Pipeline failed: %s",
            e,
        )
        raise
