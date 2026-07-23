"""

Loads and caches the vision-language model and processor used for
answer generation. The model is initialized only once using
Streamlit's resource caching mechanism.
"""

import streamlit as st
import torch
from transformers import AutoModelForImageTextToText, AutoProcessor

from config import config
from Code.utils.logger import get_logger

logger = get_logger(__name__)


@st.cache_resource
def load_model():
    """
    Load and cache the language model and processor.

    Returns
    -------
    tuple
        A tuple containing:

        - processor : AutoProcessor
            Processor used to tokenize and prepare model inputs.

        - model : AutoModelForImageTextToText
            Loaded language model used for text generation.
    """

    logger.info("Loading SmolVLM2...")

    processor = AutoProcessor.from_pretrained(config.LLM_MODEL_NAME)

    model = AutoModelForImageTextToText.from_pretrained(
        config.LLM_MODEL_NAME,
        dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
    )

    # model.eval()
    logger.info("SmolVLM2 loaded successfully.")

    return processor, model
