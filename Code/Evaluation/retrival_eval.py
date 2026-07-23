"""
Provides evaluation metrics for retrieval performance.

Currently supports Precision and Recall by comparing retrieved
chunk IDs against ground-truth relevant chunk IDs.
"""

import json
from pathlib import Path

from config import config
from Code.utils.logger import get_logger

logger = get_logger(__name__)


# ----------------------------------------------------
# Load chunk mapping only once
# ----------------------------------------------------
with open(Path(config.CHUNKKED_JSON), "r", encoding="utf-8") as f:
    chunk_data = json.load(f)

TEXT_TO_ID = {item["chunk_text"].strip(): item["chunk_id"] for item in chunk_data}
relevant_id_list: list[int] = []


def precision_recall(retrieved_chunks: list, relevant_chunks: list):
    """
    Calculate Precision and Recall.

    Parameters
    ----------
    retrieved_chunks : list
        Chunks returned by the retriever.

    relevant_chunks : list
        Ground-truth relevant chunk IDs.

    Returns
    -------
    tuple
        (precision, recall)
    """

    # ----------------------------------------
    # Convert retrieved chunks to chunk IDs
    # ----------------------------------------
    retrieved_ids = set()

    for row in retrieved_chunks:
        text = row.get("embedding_text", "").strip()

        chunk_id = TEXT_TO_ID.get(text)
        if chunk_id is not None:
            retrieved_ids.add(chunk_id)

    relevant_ids = set(relevant_chunks)

    # ----------------------------------------
    # Calculate metrics
    # ----------------------------------------
    true_positive = len(retrieved_ids & relevant_ids)
    false_positive = len(retrieved_ids - relevant_ids)
    false_negative = len(relevant_ids - retrieved_ids)

    precision = true_positive / len(retrieved_ids) if retrieved_ids else 0.0

    recall = true_positive / len(relevant_ids) if relevant_ids else 0.0

    logger.info(
        "Retrieved IDs: %s\n" "Relevant IDs: %s\n" "TP=%d, FP=%d, FN=%d",
        retrieved_ids,
        relevant_ids,
        true_positive,
        false_positive,
        false_negative,
    )

    return round(precision, 2), round(recall, 2)


def retriever_check(results: list) -> list[int] | None:
    """
    Prompt the user for ground-truth chunk IDs and evaluate retrieval.
    """

    logger.info("Checking retriever performance...")

    try:
        relevant_ids = list(
            map(int, input("Enter relevant chunk IDs (space separated): ").split())
        )

        precision, recall = precision_recall(results, relevant_ids)

        logger.info(f"Precision: {precision:.2f} | Recall: {recall:.2f}")
        return relevant_ids
    except ValueError:
        logger.error("Please enter only integer chunk IDs.")
        return None


def relevant_chunk_id() -> int:
    """
    Return the first relevant chunk ID.

    Returns
    -------
    int
        First ground-truth chunk ID.
    """
    return relevant_id_list[0]
