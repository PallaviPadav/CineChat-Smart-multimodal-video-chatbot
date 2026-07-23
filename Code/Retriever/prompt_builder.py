"""
Build prompts for the language model using the retrieved context.
"""

from Code.utils.logger import get_logger

logger = get_logger(__name__)


def build_prompt(query, retrieved_docs):
    """
    Build prompt for the LLM.

    Parameters
    ----------
    query : str

    retrieved_docs : list

    Returns
    -------
    str
    """

    logger.info("Building prompt...")

    context = ""

    for i, row in enumerate(retrieved_docs, start=1):
        context += f"""
    Context {i}
    -------------------------
    {row['embedding_text']}

    """

        prompt = f"""
    You are an intelligent multimodal video assistant.

    Your task is to answer the user's question ONLY using the
    provided video context.

    Instructions:

    1. Use only the information present in the context.
    2. Do not hallucinate.
    3. If the answer is unavailable, say:
    "The information is not available in the retrieved context."
    4. Answer in complete sentences.
    5. Be concise but informative.
    6. Answer in max three sentence.

    =========================
    VIDEO CONTEXT
    =========================

    {context}

    =========================
    QUESTION
    =========================

    {query}

    =========================
    ANSWER
    =========================
    """

    logger.info("Prompt built successfully.")

    return prompt
