"""
Extracts representative frames from a video at fixed intervals.

The module filters blank and duplicate frames, stores metadata,
and triggers frame-to-text conversion for the extracted frames.
"""

import json
import shutil

import cv2
import numpy as np

from config import config

from Code.DB_creation.frame_text_conversion import frame_to_text_conversion
from Code.utils.logger import get_logger

logger = get_logger(__name__)


def is_empty_frame(frame: np.ndarray):
    """Detect black/empty frames"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return np.mean(gray) < 8  # threshold for blank frame


def is_duplicate(
    frame1: np.ndarray,
    frame2: np.ndarray,
):
    """Simple duplicate detection using pixel similarity"""
    diff = cv2.absdiff(frame1, frame2)
    return np.mean(diff) < 1.5  # very similar frames


def extract_frame() -> bool:
    """
    Extract representative frames from the input video.

    The function removes blank and duplicate frames, stores
    frame metadata, and performs frame-to-text conversion.

    Returns
    -------
    bool
        True if frame extraction succeeds, otherwise False.
    """
    try:
        logger.info("Frame extraction started")

        output_dir = config.FRAME_PATH
        metadata_path = config.FRAME_METADATA_PATH

        if output_dir.exists():
            logger.info(f"Clearing existing frames from: {output_dir}")
            shutil.rmtree(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        if metadata_path.exists():
            logger.info(f"Deleting existing metadata: {metadata_path}")
            metadata_path.unlink()

        metadata_path.parent.mkdir(parents=True, exist_ok=True)

        cap = cv2.VideoCapture(str(config.VIDEO_DOWNLOAD_PATH))

        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        frame_interval = int(video_fps * config.interval_sec)

        logger.info(
            "FPS: %.2f, Total frames: %d",
            video_fps,
            total_frames,
        )

        current_frame = 0
        saved_count = 0

        metadata_list = []
        last_saved_frame = None

        while True:
            success, frame = cap.read()

            if not success:
                break

            # skip empty frames
            if is_empty_frame(frame):
                current_frame += 1
                continue

            # save only at interval
            if current_frame % frame_interval == 0:
                # duplicate check
                if last_saved_frame is not None and is_duplicate(
                    frame, last_saved_frame
                ):
                    logger.info("Duplicate frame skipped")
                    current_frame += 1
                    continue

                timestamp = current_frame / video_fps

                frame_name = f"frame_{saved_count:04d}.jpg"
                frame_path = output_dir / frame_name

                cv2.imwrite(str(frame_path), frame)

                metadata_list.append(
                    {
                        "frame_id": saved_count,
                        "frame_name": frame_name,
                        "timestamp_sec": round(timestamp, 2),
                    }
                )

                last_saved_frame = frame.copy()
                saved_count += 1

                logger.info(
                    "Saved %s at %.2fs",
                    frame_name,
                    timestamp,
                )

            current_frame += 1

        cap.release()

        # =====================================================
        # SAVE METADATA (FULL LIST)
        # =====================================================
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata_list, f, indent=4)

        logger.info(f"Metadata saved: {metadata_path}")
        logger.info(f"Total clean frames: {saved_count}")

        # Run  text conversion
        frame_to_text_conversion()

        logger.info("Frame extraction completed")

        return True

    except Exception as e:
        logger.error(f"Frame extraction failed: {str(e)}")
        return False
