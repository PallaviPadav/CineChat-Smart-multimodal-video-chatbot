"""

Provides utilities for generating responses using the loaded
language model. The module prepares the prompt, performs text
generation, and decodes the model output into a readable answer.
"""

import torch
from config import config
from Code.model.llm_loader import load_model
from Code.utils.logger import get_logger

logger = get_logger(__name__)


# -------------------------------------------------------
# Generate answer
# -------------------------------------------------------
def generate_answer(prompt: str) -> str:
    """
    Generate an answer for the given prompt using the language model.

    The function loads the cached model and processor, formats the
    prompt using the model's chat template, generates a response,
    and returns the decoded answer.

    Parameters
    ----------
    prompt : str
        Prompt to be sent to the language model.

    Returns
    -------
    str
        Generated response from the language model.

    Raises
    ------
    Exception
        Raised if model loading or text generation fails.
    """

    try:
        processor, model = load_model()

        logger.info("Generating answer...")

        messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]

        prompt_text = processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        logger.info("Created prompt...")

        inputs = processor(text=prompt_text, return_tensors="pt")

        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        logger.info("created input...")

        if config.SUMMARY_FLAG:
            max_new_tokens = 100
            config.SUMMARY_FLAG = False
        else:
            max_new_tokens = 70

        with torch.inference_mode():
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
            )

        # Remove prompt tokens
        generated_ids = generated_ids[:, inputs["input_ids"].shape[1] :]
        logger.info("start  checking for answer...")

        answer = processor.batch_decode(generated_ids, skip_special_tokens=True)[
            0
        ].strip()

        logger.info("Answer generated successfully.")

        return answer

    except Exception as e:
        logger.exception("LLM generation failed: %s", e)
        raise
