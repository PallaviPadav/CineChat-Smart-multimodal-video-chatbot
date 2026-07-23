import json
import lancedb
from config import config
from sentence_transformers import SentenceTransformer
from Code.utils.logger import get_logger

logger = get_logger(__name__)


def embedding_lancedb():
    try:
        logger.info("Embedding generation started.")

        # Load embedding model
        logger.info("Loading embedding model...")
        embedding_model = SentenceTransformer("BAAI/bge-base-en-v1.5")

        # Connect to LanceDB
        logger.info("Connecting to LanceDB...")
        db = lancedb.connect("Data/vectordb")

        # Load input records
        logger.info(f"Loading records from {config.CHUNKKED_TEXT}...")
        with open(config.CHUNKKED_TEXT, "r", encoding="utf-8") as f:
            records = f.read()

        if not records:
            logger.warning("No records found in the input file.")
            return

        data = []
        id_counter = 0

        logger.info(f"Generating embeddings for {len(records)} records...")

        for text in records.split("[EOC]"):
            id_counter += 1
            text = text.replace("\n", " ").strip()
            embedding = embedding_model.encode(text, normalize_embeddings=True)

            data.append(
                {"id": id_counter, "embedding_text": text, "vector": embedding.tolist()}
            )

        # Create/overwrite LanceDB table
        logger.info("Creating LanceDB table...")
        table = db.create_table("cinechat", data=data, mode="overwrite")

        logger.info("Creating Full Text Search (FTS) index...")

        table.create_fts_index(field_names="embedding_text", replace=True)

        logger.info("FTS index created successfully.")

        logger.info(
            f"Embedding generation completed successfully. "
            f"Rows inserted: {table.count_rows()}"
        )
        df = table.to_pandas()

        logger.info(df)

    except FileNotFoundError:
        logger.exception(f"Input file not found: {config.CHUNKKED_TEXT}")
        raise

    except json.JSONDecodeError:
        logger.exception("Invalid JSON format in the embedding input file.")
        raise

    except KeyError as e:
        logger.exception(f"Missing required key in input record: {e}")
        raise

    except Exception as e:
        logger.exception(f"Unexpected error while creating embeddings: {e}")
        raise


if __name__ == "__main__":
    embedding_lancedb()
