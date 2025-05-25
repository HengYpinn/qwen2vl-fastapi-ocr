import warnings
import re
import json
import torch
from PIL import Image
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor

# suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# 1. Load processor and model once at import time, in 8-bit to save GPU memory
processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-2B-Instruct")
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-2B-Instruct",
    device_map="auto",
    load_in_8bit=True,
    torch_dtype=torch.float16
)

def _normalize_image_for_model(pil_img: Image.Image, max_dim: int = 1200) -> Image.Image:
    """
    Downscale any dimension above max_dim, preserving aspect ratio.
    This keeps incoming images at or above the model’s native resolution
    but avoids huge GPU allocations.
    """
    w, h = pil_img.size
    if max(w, h) > max_dim:
        pil_img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    return pil_img

def _parse_json_from_string(raw: str) -> dict:
    """
    Strip Markdown fences and parse JSON. On failure, return an error structure.
    """
    cleaned = re.sub(r"```json|```", "", raw).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"error": "Failed to parse model output", "raw": raw}

def extract_info_from_image(pil_img: Image.Image, prompt_text: str) -> dict:
    """
    Run the vision-language model on a single PIL image with a custom prompt.
    Handles resizing, inference, and memory cleanup to avoid OOM.
    """
    # 1) Downscale large images to save memory
    pil_img = _normalize_image_for_model(pil_img, max_dim=1200)

    # 2) Prepare the inputs
    inputs = processor(
        text=[prompt_text],
        images=[pil_img],
        padding=True,
        return_tensors="pt"
    ).to(model.device)

    # 3) Generate with a reasonable token limit
    with torch.no_grad():
        generated = model.generate(**inputs, max_new_tokens=128)

    # 4) Trim off the prompt’s tokens and decode
    prompt_len = inputs.input_ids.shape[-1]
    gen_ids = generated[0][prompt_len:]
    decoded = processor.batch_decode([gen_ids], skip_special_tokens=True)[0]

    # 5) Free up GPU memory immediately
    torch.cuda.empty_cache()

    # 6) Parse JSON from the model’s output
    return _parse_json_from_string(decoded)
