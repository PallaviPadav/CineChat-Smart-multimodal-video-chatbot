"""
Generates a concise technical summary of a video using the
language model. The module reads the processed video context,
builds a summarization prompt, and returns the generated summary.

"""

from config import config
from Code.model.llm_model import generate_answer
from Code.utils.logger import get_logger

logger = get_logger(__name__)


def summarize_video(context):
    """
    Generate a technical summary of the video.

    Parameters
    ----------
    context : str
        Combined textual context extracted from the video.

    Returns
    -------
    str
        Generated video summary.
    """

    prompt = f"""
You are an expert technical write.

Summarize the following video.

Requirements:
- Write a concise summary.
- easy to understand
- Mention the main concepts.
- Reframe the sentence to make it like technical document i.e dont use words like 'in the slide'.
- Highlight the important technical concepts.
- Avoid repetition.
- Use bullet points where appropriate.
- For summarization please provide the summary within 200 words.
- For chat answere within 70 words

Video Context:

{context}
"""

    return generate_answer(prompt)


def get_summary():
    """
    Generate a summary for the processed video.

    The function loads the chunked video text, removes end-of-chunk
    markers, constructs a summarization prompt, and generates the
    final summary using the language model.

    Returns
    -------
    str
        Generated video summary.
    """

    logger.info("Processing summarization....")
    with open(config.CHUNKKED_TEXT, "r", encoding="utf-8") as f:
        context = f.read()
    logger.info("Creating context for summarization....")
    context = context.replace("[EOC]", "")
    logger.info("context: %s", context)
    result = summarize_video(context)
    return result


"""if __name__ == "__main__":
    summary = get_summary()
    logger.info(f"summary: {summary}")"""
