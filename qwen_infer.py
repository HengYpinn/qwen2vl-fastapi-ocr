import warnings
import re
import json
import torch
from PIL import Image
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
warnings.filterwarnings("ignore")

# 1) Load processor + full-precision model
processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-2B-Instruct")
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-2B-Instruct",
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

    # Apply prompt template
    prompt_text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    # Prepare inputs for vision model
    image_inputs, video_inputs = process_vision_info(messages)

    inputs = processor(
        text=[prompt_text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt"
    ).to("cuda")

    # Generate output
    generated_ids = model.generate(**inputs, do_sample=False, num_beams=8, max_new_tokens=256)
    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]

    decoded_output = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )

    raw_text = decoded_output[0]


    # 5) Free VRAM & parse into a Python dict
    torch.cuda.empty_cache()
    return _parse_json_from_string(raw_text)
