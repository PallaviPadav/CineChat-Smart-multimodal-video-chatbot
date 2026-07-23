from PIL import Image
from Code.model.model_frame import model_frame_text
import json
from config import config
from Code.utils.logger import get_logger
import warnings
import os
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise EnvironmentError("HF_TOKEN is not set. Please add it to your .env file.")

os.environ["HF_TOKEN"] = hf_token

warnings.filterwarnings("ignore")  # general

logger = get_logger(__name__)
model_name = config.FRAME_TEXT_MODEL_NAME
model_path = config.FRAME_TEXT_MODEL_PATH


def frame_to_text_conversion():
    logger.info("Frame to text : Conversion started")

    model, processor = model_frame_text()

    OUTPUT_FILE = config.FRAME_OUTPUT_FILE

    results = []

    for frame_path in sorted(config.FRAME_PATH.glob("*.jpg")):
        try:
            image = Image.open(frame_path)
            image.show()
        except Exception as e:
            logger.error(f"Failed to open {frame_path}: {e}")
            continue  # Skip this frame

        logger.info(f"Frame to text : Conversing {frame_path}")
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image,
                    },
                    {
                        "type": "text",
                        "text": """
                            Describe this video frame.

                            Return:

                            - Visible Text
                            - Important Concepts
                            - Diagram Explanation
                            - Summary

                            Ignore page headers and footers.
                            """,
                    },
                ],
            }
        ]

        text = processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = processor(text=[text], images=[image], return_tensors="pt")

        # logger.info(f"Frame to text : {inputs}")

        output_ids = model.generate(
            **inputs,
            max_new_tokens=240,
            pad_token_id=processor.tokenizer.eos_token_id,
        )

        description = processor.batch_decode(
            output_ids[:, inputs.input_ids.shape[1] :], skip_special_tokens=True
        )[0]
        # logger.info(f"Frame to text : Conversing {frame_path} -> {description}")

        results.append({"frame_name": frame_path.name, "description": description})

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    logger.info("Frame to text : Conversion completed")


if __name__ == "__main__":
    frame_to_text_conversion()
