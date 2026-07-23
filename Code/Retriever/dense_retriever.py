"""
Performs semantic (dense vector) retrieval using LanceDB.
The module generates embeddings for user queries using a
SentenceTransformer model and retrieves the most semantically
similar chunks from the vector database.
"""

import traceback
import lancedb
from sentence_transformers import SentenceTransformer
from config import config
from Code.utils.logger import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------
# Load model only once
# ---------------------------------------------------------------------

logger.info("Loading embedding model...")

embedding_model = SentenceTransformer(config.SENTENCE_TRANSFORMER)

logger.info("Connecting to LanceDB...")

db = lancedb.connect(config.LANCEDB_PATH)

table = db.open_table(config.LANCEDB_TABLE_NAME)

logger.info("Dense Retriever initialized successfully.")


def generate_query_embedding(query):
    """
    Generate embedding for user query.

    Parameters
    ----------
    query : str

    Returns
    -------
    list
    """

    try:
        embedding = embedding_model.encode(query, normalize_embeddings=True)

        return embedding.tolist()

    except Exception as e:
        logger.error("Embedding generation failed: %s", e)

        logger.error(traceback.format_exc())

        raise


# ---------------------------------------------------------------------
# Dense Retrieval
# ---------------------------------------------------------------------


def dense_retrieve(query, top_k=5):
    """
    Perform semantic search.

    Parameters
    ----------
    query : str

    top_k : int

    Returns
    -------
    list
    """

    try:
        logger.info(f"User Query : {query}")

        query_embedding = generate_query_embedding(query)

        logger.info("Searching LanceDB...")

        results = table.search(query_embedding).limit(top_k).to_list()

        logger.info(" %s records retrieved.", len(results))
        print_results(results)

        return results

    except Exception as e:
        logger.error("Dense retrieval failed: %s", e)

        logger.error(traceback.format_exc())

        raise


# ---------------------------------------------------------------------
# Print Results
# ---------------------------------------------------------------------


def print_results(results):
    """
    Print retrieved records.
    """

    logger.info("=" * 80)

    for i, row in enumerate(results, start=1):
        logger.info("\n Rank : %s", i)

        logger.info("\n ID : %s", row.get("id", ""))
        logger.info(
            "\n ================*******************************====================="
        )

        logger.info("\n Embedding Text")

        logger.info(row.get("embedding_text", ""))

        logger.info(
            "======================================================================"
        )


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

"""if __name__ == "__main__":
    query = input("Enter your question : ")

    retrieved_data = dense_retrieve(query=query, top_k=config.TOP_K)

    ##logger.info(f"retrieved_data : {retrieved_data} ")"""
