from PIL import Image
import io

def load_image_from_bytes(image_bytes: bytes):
    return Image.open(io.BytesIO(image_bytes)).convert("RGB")
