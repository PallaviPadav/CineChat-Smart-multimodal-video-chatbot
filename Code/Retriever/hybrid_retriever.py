"""
hybrid_retriever.py

Native LanceDB Hybrid Search

Combines:
1. Dense Vector Search
2. Full Text Search (FTS)
3. Built-in RRF Reranker

Author : CineChat
"""

import lancedb
from sentence_transformers import CrossEncoder, SentenceTransformer
from config import config
from Code.Evaluation.retrival_eval import retriever_check
from Code.utils.logger import get_logger

logger = get_logger(__name__)

# ----------------------------------------------------------
# Load model only once
# ----------------------------------------------------------

embedding_model = None
db = None
table = None


def load_resources():
    """
    Load the embedding model and connect to the LanceDB database.

    Resources are initialized only once and reused for subsequent
    retrieval requests.
    """

    global embedding_model
    global db
    global table

    if embedding_model is None:
        logger.info("Loading embedding model...")
        embedding_model = SentenceTransformer(config.SENTENCE_TRANSFORMER)

    if db is None:
        logger.info("Connecting to LanceDB...")
        db = lancedb.connect(config.LANCEDB_PATH)
        table = db.open_table(config.LANCEDB_TABLE_NAME)

    logger.info("Retriever initialized successfully.")


# ----------------------------------------------------------
# Generate Query Embedding
# ----------------------------------------------------------


def generate_query_embedding(query):
    """
    Function to Generate Query Embedding
    """
    embedding = embedding_model.encode(query, normalize_embeddings=True)

    return embedding.tolist()


# ----------------------------------------------------------
# Hybrid Retrieval
# ----------------------------------------------------------


def hybrid_retrieve(query, top_k=5):
    """
    Native LanceDB Hybrid Search
    """

    try:
        load_resources()

        logger.info("Query : %s", query)

        query_embedding = generate_query_embedding(query)

        logger.info("Running Hybrid Search...")

        results = (
            table.search(query_type="hybrid")
            .vector(query_embedding)
            .text(query)
            .limit(top_k)
            .to_list()
        )

        logger.info(" %s records retrieved.", len(results))

        return results

    except Exception as e:
        logger.exception("Hybrid Retrieval Failed : %s", e)

        raise


# ----------------------------------------------------------
# Print Results
# ----------------------------------------------------------


def print_results(results):
    """
    print the results
    """
    logger.info("=" * 80)

    for i, row in enumerate(results, start=1):
        logger.info("Rank : %s", i)

        logger.info("ID : %s", row.get("id"))

        if "_relevance_score" in row:
            logger.info("Score : %s", row["_relevance_score"])

        logger.info(row.get("embedding_text", ""))

        logger.info("=" * 80)


# ----------------------------------------------------------
# Rerank
# ----------------------------------------------------------


def rerank_results(query, results):
    """
    Rerank retrieved documents using CrossEncoder.
    """
    logger.info("Loading Cross Encoder...")

    try:
        reranker = CrossEncoder(config.RERANKER_MODEL)
        logger.info("Cross Encoder loaded successfully.")
    except Exception as e:
        logger.exception(e)
        raise
    try:
        if not results:
            return []

        logger.info("Reranking retrieved documents...")

        pairs = [(query, row["embedding_text"]) for row in results]

        scores = reranker.predict(pairs)

        for row, score in zip(results, scores):
            row["rerank_score"] = float(score)

        results = sorted(results, key=lambda x: x["rerank_score"], reverse=True)

        logger.info("Reranking completed.")
        # precision, recall, relevant_ids = retriever_check(results)

        return results

    except Exception as e:
        logger.exception("Reranking failed : %s", e)

        raise


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------


# if __name__ == "__main__":
def mrr_testing_purpose():
    """
    Evaluate the hybrid retriever using Mean Reciprocal Rank (MRR).

    This function is intended for testing and evaluation purposes.
    It prompts the user for a query, performs hybrid retrieval,
    reranks the retrieved documents using a CrossEncoder, displays
    the reranked results, and invokes the retriever evaluation.

    Returns
    -------
    tuple
        A tuple containing:

        - rerank_result : list
            Top-k reranked retrieval results.

        - retrieve : tuple
            Retrieval evaluation metrics returned by
            ``retriever_check()``.
    """

    query = input("Enter Query : ")

    results = hybrid_retrieve(query=query, top_k=config.TOP_K)
    rerank = rerank_results(query, results)
    rerank_result = rerank[: config.TOP_K]
    logger.info("reranked result: %s", rerank_result)
    print_results(rerank_result)
    retrive = retriever_check(rerank_result)
    return rerank_result, retrive
