import warnings
import re
import json
import torch
from PIL import Image
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor

warnings.filterwarnings("ignore")

# 1) Load processor + full-precision model
processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-7B-Instruct",
    device_map="auto"
)

def _normalize_image_for_model(pil_img: Image.Image, max_dim: int = 1200) -> Image.Image:
    """Resize largest side to `max_dim` preserving aspect ratio."""
    if max(pil_img.size) > max_dim:
        pil_img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    return pil_img

def _parse_json_from_string(raw: str) -> dict:
    """Strip fences, un-escape if quoted, then JSON-load."""
    cleaned = re.sub(r"```json|```", "", raw).strip()

    # If the model returned a JSON string literal, un-escape it
    if cleaned.startswith('"') and cleaned.endswith('"'):
        inner = cleaned[1:-1]
        try:
            unescaped = bytes(inner, "utf-8").decode("unicode_escape")
            return json.loads(unescaped)
        except json.JSONDecodeError:
            # fall through to normal load
            cleaned = unescaped

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"error": "parse_failed", "raw": raw}

def extract_info_from_image(pil_img: Image.Image, prompt_text: str) -> dict:
    """
    Given a PIL image + text prompt, run Qwen2-VL and return parsed JSON.
    Prompt should demand *raw* JSON (no quotes, no code-blocks).
    """
    img = _normalize_image_for_model(pil_img)

    # 1) Build single-message “chat”
    messages = [{
        "role": "user",
        "content": [
            {"type": "image", "image": img},
            {"type": "text",  "text": prompt_text}
        ],
    }]

    # 2) Inject <image> tokens & get tensors
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt",
        return_dict=True
    ).to(model.device)

    # 3) Generate deterministically to reduce noise
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=128,
            temperature=0.0,
            do_sample=False,
            num_beams=4,
            eos_token_id=processor.tokenizer.eos_token_id
        )

    # 4) Strip prompt tokens, decode only the generated portion
    prompt_len = inputs.input_ids.shape[-1]
    gen_ids    = output_ids[0, prompt_len:]
    raw_txt    = processor.batch_decode([gen_ids], skip_special_tokens=True)[0]

    # 5) Free VRAM & parse into a Python dict
    torch.cuda.empty_cache()
    return _parse_json_from_string(raw_txt)
