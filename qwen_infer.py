from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
import torch
from qwen_vl_utils import process_vision_info  # Make sure this is installed
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Load model and processor once during startup
processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-2B-Instruct")
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-2B-Instruct",
    torch_dtype="auto",
    device_map="auto"
)

def extract_info_from_image(image):
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {
                    "type": "text",
                    "text": "Analyze the image and respond with key information in RESTful API JSON format. If the image is a Malaysian IC, extract: fullName, icNumber, address, nationality, and gender. If it is a receipt, extract: date, referenceNumber, totalAmount, and any other relevant fields. For any other image type, intelligently identify and return any important fields you find useful."
                }
            ]
        }
    ]

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
    generated_ids = model.generate(**inputs, max_new_tokens=128)
    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]

    decoded_output = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )

    return decoded_output[0]
