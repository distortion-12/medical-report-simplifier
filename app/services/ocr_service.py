from PIL import Image
import pytesseract
import io

# For extracting raw text from an image using OCR.
async def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Performs OCR on an image to extract text.
    Args:
        image_bytes: The image file in bytes.
    Returns:
        The extracted raw text as a string.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise ValueError(f"Failed to process image: {e}")