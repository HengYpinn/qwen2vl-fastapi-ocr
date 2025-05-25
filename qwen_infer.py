import warnings
import re
import json
import torch
from PIL import Image
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor

warnings.filterwarnings("ignore")

processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-2B-Instruct")
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-2B-Instruct",
    device_map="auto",
    load_in_8bit=True,
    torch_dtype=torch.float16
)

def _normalize_image_for_model(pil_img: Image.Image, max_dim: int = 1200) -> Image.Image:
    w, h = pil_img.size
    if max(w, h) > max_dim:
        pil_img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    return pil_img

def _parse_json_from_string(raw: str) -> dict:
    cleaned = re.sub(r"```json|```", "", raw).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"error": "Failed to parse model output", "raw": raw}

def extract_info_from_image(pil_img: Image.Image, prompt_text: str) -> dict:
    """
    Run Qwen2-VL on a single PIL image plus a text prompt,
    using apply_chat_template to align image tokens and features.
    """
    pil_img = _normalize_image_for_model(pil_img, max_dim=1200)

    # 1) Build a single-user “conversation” with image + text
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": pil_img},
                {"type": "text",  "text": prompt_text}
            ],
        }
    ]

    # 2) Apply the chat template so input_ids include <image> tokens
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    ).to(model.device)

    # 3) Generate the response
    with torch.no_grad():
        output_ids = model.generate(**inputs, max_new_tokens=128)

    # 4) Trim off prompt tokens and decode
    prompt_len  = inputs.input_ids.shape[-1]
    gen_ids     = output_ids[0, prompt_len:]
    decoded     = processor.batch_decode([gen_ids], skip_special_tokens=True)[0]

    # 5) Free memory and parse JSON
    torch.cuda.empty_cache()
    return _parse_json_from_string(decoded)
