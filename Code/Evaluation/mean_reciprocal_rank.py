"""
mean_reciprocal_rank.py

Computes the Mean Reciprocal Rank (MRR) of the retriever.

For each query, the reciprocal rank of the first relevant
retrieved chunk is calculated. The final MRR is the average
of the reciprocal ranks across all evaluation queries.
"""

from config import config

from Code.Retriever.hybrid_retriever import mrr_testing_purpose
from Code.utils.logger import get_logger

logger = get_logger(__name__)


query_counter = config.NUMBER_OF_QUERY_MRR
reciprocal_ranks: list[float] = []


def mean_reciprocal_rank() -> float:
    """
    Calculate the Mean Reciprocal Rank (MRR).

    For each evaluation query, the reciprocal rank of the first
    relevant retrieved chunk is computed. If no relevant chunk is
    retrieved, a reciprocal rank of 0 is assigned.

    Returns
    -------
    float
        Mean Reciprocal Rank rounded to two decimal places.
    """
    for query in range(query_counter):
        rank_order, relevant_id_list = mrr_testing_purpose()
        # relevant_id_list = relevant_chunk_id()

        for rank, value in enumerate(rank_order, start=1):
            if value["id"] == relevant_id_list[0]:
                rr = 1 / rank
                logger.info(f"First relevant chunk found at query {query}  is {rr}")
                reciprocal_ranks.append(rr)
                break
            elif rank == len(rank_order) and value["id"] != relevant_id_list:
                rr = 0
                reciprocal_ranks.append(rr)
    logger.info(
        "Reciprocal ranks: %s",
        reciprocal_ranks,
    )
    return round(sum(reciprocal_ranks) / len(reciprocal_ranks), 2)


if __name__ == "__main__":
    mrr = mean_reciprocal_rank()
    logger.info(f"MRR = {mrr}")
