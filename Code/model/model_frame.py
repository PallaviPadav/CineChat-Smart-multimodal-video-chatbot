"""
Loads and caches the vision-language model used for extracting
descriptions from video frames.

The model and processor are loaded only once using Streamlit's
resource caching mechanism.
"""

# from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from transformers import AutoProcessor, AutoModelForImageTextToText
import streamlit as st
from config import config
from Code.utils.logger import get_logger

logger = get_logger(__name__)

model_name = config.FRAME_TEXT_MODEL_NAME
model_path = config.FRAME_TEXT_MODEL_PATH


@st.cache_resource
def model_frame_text():
    """
    Load and cache the frame-to-text model and processor.

    Returns
    -------
    tuple
        A tuple containing:

        - model : AutoModelForImageTextToText
            Vision-language model used for image captioning.

        - processor : AutoProcessor
            Processor used for preparing image and text inputs.
    """

    logger.info(" Set the model")
    processor = AutoProcessor.from_pretrained(model_name)
    model = AutoModelForImageTextToText.from_pretrained(
        model_name,
        attn_implementation="sdpa",
        device_map="cpu",
    )

    return model, processor
