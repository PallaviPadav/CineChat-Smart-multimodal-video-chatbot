from pathlib import Path

VIDEO_DOWNLOAD_PATH = Path(
    "F:/AgenticAI/Workplace/CineChat-Smart-multimodal-video-chatbot/Data/video/input_video.mp4"
)

DOWNLOAD_FORMAT = "mp4"

VIDEO_METADATA_PATH = Path(
    "F:/AgenticAI/Workplace/CineChat-Smart-multimodal-video-chatbot/Data/Metadata/input_video.json"
)

FRAME_PATH = Path(
    "F:/AgenticAI/Workplace/CineChat-Smart-multimodal-video-chatbot/Data/image"
)
MULTIMODAL_DATASET_PATH = Path(
    "F:/AgenticAI/Workplace/CineChat-Smart-multimodal-video-chatbot/Data/Metadata/multimodal_meta.json"
)

# FRAME_TEXT_MODEL_NAME = "Qwen/Qwen3-VL-2B-Instruct"
FRAME_TEXT_MODEL_NAME = "HuggingFaceTB/SmolVLM2-500M-Video-Instruct"
# FRAME_TEXT_MODEL_NAME = "HuggingFaceTB/SmolVLM2-2.2B-Instruct"
FRAME_TEXT_MODEL_PATH = Path("SmolVLM2")

FRAME_METADATA_PATH = Path(
    "F:/AgenticAI/Workplace/CineChat-Smart-multimodal-video-chatbot/Data/Metadata/frame_meta.json"
)
OCR_METADATA_PATH = Path(
    "F:/AgenticAI/Workplace/CineChat-Smart-multimodal-video-chatbot/Data/Metadata/OCR_meta.json"
)

AUDIO_PATH = Path(
    "F:/AgenticAI/Workplace/CineChat-Smart-multimodal-video-chatbot/Data/Audio/output_audio.mp3"
)

TEXT_PATH = Path(
    "F:/AgenticAI/Workplace/CineChat-Smart-multimodal-video-chatbot/Data/Text/Audio_text.txt"
)
FRAME_OUTPUT_FILE = Path(
    "F:/AgenticAI/Workplace/CineChat-Smart-multimodal-video-chatbot/Data/Metadata/frame_descriptions.json"
)

EMBEDDING_INPUT_PATH = Path(
    "F:/AgenticAI/Workplace/CineChat-Smart-multimodal-video-chatbot/Data/Metadata/embedding_text_input.txt"
)
CHUNKKED_TEXT = Path(
    "F:/AgenticAI/Workplace/CineChat-Smart-multimodal-video-chatbot/Data/Metadata/chunked_text.txt"
)
CHUNKKED_JSON = Path(
    "F:/AgenticAI/Workplace/CineChat-Smart-multimodal-video-chatbot/Data/Metadata/chunked_json.json"
)
interval_sec = 30

SENTENCE_TRANSFORMER = "BAAI/bge-base-en-v1.5"
TOP_K = 3
NUMBER_OF_QUERY_MRR = 5

LANCEDB_PATH = "Data/vectordb"

LANCEDB_TABLE_NAME = "cinechat"

RERANKER_MODEL = "BAAI/bge-reranker-base"

# LLM_MODEL_NAME = "HuggingFaceTB/SmolVLM2-2.2B-Instruct"
LLM_MODEL_NAME = "HuggingFaceTB/SmolVLM2-500M-Video-Instruct"

SUMMARY_FLAG = False
