from config import config
from Code.utils.logger import get_logger
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

nltk.download("punkt")

model = SentenceTransformer("BAAI/bge-base-en-v1.5")
logger = get_logger(__name__)


def semantic_cohesion(chunk):

    sentences = nltk.sent_tokenize(chunk)

    if len(sentences) < 2:
        return 1.0

    embeddings = model.encode(sentences, normalize_embeddings=True)

    scores = []

    for i in range(len(sentences) - 1):

        score = cosine_similarity([embeddings[i]], [embeddings[i + 1]])[0][0]

        scores.append(score)

    return sum(scores) / len(scores)


def chunk_size_eval():
    logger.info("checking chunk size...")

    with open(config.CHUNKKED_TEXT, "r", encoding="utf-8") as f:
        chunks = f.read()
    logger.info(chunks)
    chunks = chunks.split("[EOC]")
    length = [len(c) for c in chunks]
    logger.info(f" Length of chunks are {length}")
    logger.info(f"Max chunk size: {max(length)}")
    logger.info(f"Min chunk size: {min(length)}")
    cosin_sim = []
    for c in chunks:
        logger.info(f" Length of chunks are {len(c)}: {c}")
        similarity = semantic_cohesion(c)
        cosin_sim.append(similarity)
        logger.info(f" Cosin similarity : {similarity}")

    cosin_sim = list(map(lambda x: round(float(x), 2), cosin_sim))

    logger.info(f"cosin_sim is : {cosin_sim}")
    plt.hist(length, bins=20)

    plt.xlabel("Words per Chunk")
    plt.ylabel("Frequency")
    plt.title("Chunk Size Distribution")
    plt.show()

    return


if __name__ == "__main__":
    chunk_size_eval()
