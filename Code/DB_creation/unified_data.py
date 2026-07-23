import json
from pathlib import Path
from config import config
from Code.utils.logger import get_logger
from Code.DB_creation.chunking_text import chunking_metadata

logger = get_logger(__name__)


def create_unified_data():

    # Load frame descriptions
    with open(config.FRAME_OUTPUT_FILE, "r", encoding="utf-8") as f:
        frame_descriptions = json.load(f)

    # Load transcript
    with open(config.TEXT_PATH, "r", encoding="utf-8") as f:
        transcript = f.read().strip()

    embedding_data = []

    for frame in frame_descriptions:

        record = {
            "frame_name": frame["frame_name"],
            "description": frame["description"],
        }
        embedding_data.append(record)

    text = {"transcript": transcript}

    embedding_data.append(text)

    # Save combined file
    output_path = Path(config.EMBEDDING_INPUT_PATH)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        logger.info(f"Deleting existing output unified file: {output_path}")
        output_path.unlink()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(embedding_data, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(embedding_data)} records to {output_path}")
    chunking_metadata()
    return embedding_data


"""if __name__ == "__main__":
    create_embedding_input()"""
