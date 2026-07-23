"""
keyword_retriever.py

Performs Full Text Search (FTS) using LanceDB.

Author : CineChat
"""

import traceback
import lancedb

from config import config
from Code.utils.logger import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------
# Connect to LanceDB
# ---------------------------------------------------------------------

logger.info("Connecting to LanceDB...")

db = lancedb.connect(config.LANCEDB_PATH)

table = db.open_table(config.LANCEDB_TABLE_NAME)

logger.info("Keyword Retriever initialized successfully.")


# ---------------------------------------------------------------------
# Keyword Retrieval
# ---------------------------------------------------------------------


def keyword_retrieve(query, top_k=5):
    """
    Perform keyword search using LanceDB FTS.

    Parameters
    ----------
    query : str
        User query

    top_k : int
        Number of results to return

    Returns
    -------
    list
        Retrieved records
    """

    try:
        logger.info("Keyword Query : %s", query)

        logger.info("Performing Full Text Search...")

        results = table.search(query).limit(top_k).to_list()

        logger.info("%s records retrieved.", len(results))

        return results

    except Exception as e:
        logger.error("Keyword retrieval failed : %s", e)

        logger.error(traceback.format_exc())

        raise


# ---------------------------------------------------------------------
# Print Results
# ---------------------------------------------------------------------


def print_results(results):
    """
    Display retrieved records.
    """

    logger.info("=" * 80)

    for i, row in enumerate(results, start=1):
        logger.info("Rank : %s", i)

        logger.info("ID : %s", row.get("id"))

        logger.info("Embedding Text :")

        logger.info(row.get("embedding_text", ""))

        logger.info("=" * 80)
