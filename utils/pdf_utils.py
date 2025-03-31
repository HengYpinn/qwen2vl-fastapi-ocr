from pdf2image import convert_from_bytes

def convert_pdf_to_images(pdf_bytes: bytes, dpi: int = 300):
    images = convert_from_bytes(pdf_bytes, dpi=dpi)
    return images
