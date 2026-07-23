"""
Main module for video processing and question answering.

"""

import warnings

from Code.Data_ingesion.video_text_conversion import video_to_text
from Code.DB_creation.vectordb import create_db
from Code.model.pipeline import chat
from Code.utils.logger import get_logger

warnings.filterwarnings("ignore")  # general

logger = get_logger(__name__)


def process_video(video_url):
    """
    Process the uploaded video and create the vector database.

    Parameters
    ----------
    video_url : str
        URL or path of the video.
    """

    logger.info("Starting Video processing")

    logger.info("Starting frame  extraction")
    # is_frame_created = extract_frame()
    video_to_text()
    logger.info("Creating DB")
    create_db()
    logger.info("Video Processing completed")


def ask_question(question):
    """
    Answer a user question using the RAG pipeline.

    Parameters
    ----------
    question : str

    Returns
    -------
    str
    """
    logger.info(f"Question : {question}")

    answer = chat(question)
    logger.info(f"Answer is  : {answer}")
    return answer
