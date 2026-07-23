"""

Creates semantic chunks from video transcripts and combines them
with frame descriptions to generate the final chunks used for
embedding and vector database creation.


"""

import json
import re
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from Code.utils.logger import get_logger
from config import config

logger = get_logger(__name__)

# --------------------------------------------------------
# Load embedding model once
# --------------------------------------------------------

logger.info("Loading Sentence Transformer...")

embedding_model = SentenceTransformer("BAAI/bge-base-en-v1.5")

logger.info("Embedding model loaded successfully.")


# --------------------------------------------------------
# Semantic Chunking
# --------------------------------------------------------


def semantic_chunking(transcript, similarity_threshold=0.5, max_sentences=5):
    """
    Semantic chunking using SentenceTransformer.

    Parameters
    ----------
    transcript : str

    similarity_threshold : float

    max_sentences : int

    Returns
    -------
    list[str]
    """

    logger.info("Semantic chunking started")

    # ----------------------------------------------------
    # Sentence Split
    # ----------------------------------------------------

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", transcript) if s.strip()]

    logger.info(f"Total sentences : {len(sentences)}")

    if len(sentences) == 0:
        return []

    if len(sentences) == 1:
        return sentences

    # ----------------------------------------------------
    # Sentence Embeddings
    # ----------------------------------------------------

    embeddings = embedding_model.encode(
        sentences, normalize_embeddings=True, convert_to_numpy=True
    )

    # ----------------------------------------------------
    # Merge similar neighbouring sentences
    # ----------------------------------------------------

    chunks = []

    current_chunk = [sentences[0]]

    current_embedding = embeddings[0]

    for i in range(1, len(sentences)):
        similarity = np.dot(current_embedding, embeddings[i])

        if similarity >= similarity_threshold and len(current_chunk) < max_sentences:
            current_chunk.append(sentences[i])

            current_embedding = current_embedding + embeddings[i]

            current_embedding /= np.linalg.norm(current_embedding)

        else:
            chunks.append(" ".join(current_chunk))

            current_chunk = [sentences[i]]

            current_embedding = embeddings[i]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    logger.info(f"Semantic chunks created : {len(chunks)}")

    return chunks


# --------------------------------------------------------
# Process Metadata
# --------------------------------------------------------


def chunking_metadata() -> list[str]:
    """
    Generate chunks for embedding.

    The function reads frame descriptions and transcript data,
    performs semantic chunking on the transcript, combines all
    chunks, and stores them in both text and JSON formats.

    Returns
    -------
    list[str]
        List of generated chunks.
    """

    try:
        logger.info(
            "Loading %s",
            config.EMBEDDING_INPUT_PATH,
        )

        with open(config.EMBEDDING_INPUT_PATH, "r", encoding="utf-8") as f:
            records = json.load(f)

        chunks = []

        for record in records:
            # ------------------------------------------
            # Frame descriptions
            # ------------------------------------------

            if "frame_name" in record and "description" in record:
                chunks.append(record["description"])

            # ------------------------------------------
            # Transcript
            # ------------------------------------------

            elif "transcript" in record:
                transcript_chunks = semantic_chunking(record["transcript"])

                chunks.extend(transcript_chunks)

        logger.info(
            "Total chunks: %d",
            len(chunks),
        )

        # ------------------------------------------
        # Save chunks
        # ------------------------------------------

        output_path = Path(config.CHUNKKED_TEXT)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_path.exists():
            output_path.unlink()

        with open(output_path, "w", encoding="utf-8") as f:
            for i, chunk in enumerate(chunks, start=1):
                # f.write(f"chunk id: {i}")

                f.write("\n")

                f.write(chunk)
                f.write("[EOC]")

                f.write("\n")

        logger.info(
            "%d chunks saved successfully.",
            len(chunks),
        )

        # -------------------------------------------------------
        # Save JSON file
        # -------------------------------------------------------
        output_path_json = Path(config.CHUNKKED_JSON)

        if output_path_json.exists():
            output_path_json.unlink()

        json_data = []

        for i, chunk in enumerate(chunks, start=1):
            json_data.append({"chunk_id": i, "chunk_text": chunk})

        with open(output_path_json, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

        logger.info(
            "%d chunks saved successfully to JSON.",
            len(json_data),
        )

        return chunks

    except Exception as e:
        logger.exception(
            "Chunking failed: %s",
            e,
        )

        raise


# --------------------------------------------------------
# Main
# --------------------------------------------------------

"""if __name__ == "__main__":
    logger.info("Running chunking")

    chunking_metadata()"""
