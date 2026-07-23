"""
Evaluates the Retrieval-Augmented Generation (RAG) pipeline using
the Ragas evaluation framework.

The module retrieves relevant contexts, generates answers using
the language model, and computes RAG metrics such as faithfulness,
answer relevancy, context precision, and context recall.
"""

from datasets import Dataset
from dotenv import load_dotenv
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import (
    answer_relevancy,
    context_precision,
    context_recall,
    faithfulness,
)

from config import config

from Code.Retriever.hybrid_retriever import hybrid_retrieve
from Code.model.llm_model import generate_answer
from Code.utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


def build_sample(question: str, ground_truth: str) -> dict:
    """
    Build a single evaluation sample for Ragas.

    Parameters
    ----------
    question : str
        User query.

    ground_truth : str
        Expected reference answer.

    Returns
    -------
    dict
        Dictionary containing the question, generated answer,
        retrieved contexts, and ground-truth answer.
    """

    retrieved_chunks = hybrid_retrieve(question, top_k=config.TOP_K)

    logger.info("retrieved_chunks : %s", retrieved_chunks)

    contexts = [row["embedding_text"] for row in retrieved_chunks]

    # -----------------------------
    # Generate Answer
    # -----------------------------
    logger.info("Start to retrieve ans")
    answer = generate_answer(f"""
        Context:

        {chr(10).join(contexts)}

        Question:
        {question}
        """)

    logger.info(
        "Question: %s\n" "Answer: %s\n" "Contexts: %s\n" "Ground Truth: %s",
        question,
        answer,
        contexts,
        ground_truth,
    )

    return {
        "question": question,
        "answer": answer,
        "contexts": contexts,
        "ground_truth": ground_truth,
    }


def evaluate_rag(samples: list) -> object:
    """
    Evaluate the RAG pipeline using Ragas.

    Parameters
    ----------
    samples : list
        Evaluation samples.

    Returns
    -------
    EvaluationResult
        Ragas evaluation scores.
    """

    dataset = Dataset.from_list(samples)
    logger.info("Start evaluation ")
    result = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=llm,
    )
    logger.info("Result of evaluation: %s", result)
    return result


if __name__ == "__main__":
    llm = LangchainLLMWrapper("meta-llama/Llama-3.2-1B-Instruct")

    samples = [
        build_sample(
            question="What is Retrieval Augmented Generation?",
            ground_truth=(
                "Retrieval Augmented Generation combines "
                "retrieval with an LLM to answer questions."
            ),
        ),
        build_sample(
            question="Which embedding model is used?",
            ground_truth="nomic-ai/nomic-embed-text-v1.5",
        ),
        build_sample(
            question="List the LLM models discussed.",
            ground_truth=("The video discusses SmolVLM2, Qwen VL and Gemini."),
        ),
    ]

    result = evaluate_rag(samples)

    logger.info(f"result : {result}")

    scores = result.to_pandas()

    scores.to_csv("Artifacts/ragas_scores.csv", index=False)
