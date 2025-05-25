import warnings
import re, json
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

def _normalize_image(img: Image.Image, max_dim=1200) -> Image.Image:
    if max(img.size) > max_dim:
        img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    return img

def _parse_json(raw: str) -> dict:
    cleaned = re.sub(r"```json|```", "", raw).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"error": "parse_failed", "raw": raw}

def extract_info_from_image(img: Image.Image, prompt: str) -> dict:
    img = _normalize_image(img)

    messages = [{
        "role": "user",
        "content": [
            {"type": "image", "image": img},
            {"type": "text",  "text": prompt}
        ]
    }]

    # inject <image> tokens
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt",
        return_dict=True
    ).to(model.device)

    # (optional) debug print
    # print("# image tokens:", (inputs.input_ids == processor.tokenizer.image_token_id).sum().item())

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=128,
            temperature=0.0,
            do_sample=False,
            num_beams=4,
            eos_token_id=processor.tokenizer.eos_token_id
        )

    prompt_len = inputs.input_ids.shape[-1]
    gen_ids    = output_ids[0, prompt_len:]
    raw_txt    = processor.batch_decode([gen_ids], skip_special_tokens=True)[0]

    torch.cuda.empty_cache()
    return _parse_json(raw_txt)
