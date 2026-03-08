"""
QR Code Generation Service

This module is responsible for creating scannable QR codes that link directly 
to a certificate's verification page. This makes it easy for anyone with a 
smartphone to check the authenticity of a printed or digital certificate.
"""

# 'qrcode' is the primary library used to generate the pixel-based QR code image.
import qrcode
# 'base64' allows us to convert the raw image data into a string format 
# that can be easily sent to a web browser or stored in a database.
import base64
# 'BytesIO' acts like a virtual file in the computer's memory. 
# We use it to 'save' the QR image without actually needing to write a file to the disk.
from io import BytesIO

def generate_qr_base64(verification_url: str) -> str:
    """
    Creates an image of a QR code that encodes a specific URL.
    
    Why this format?
    By returning a Base64 string, the frontend can simply place it inside an 
    <img> tag without needing a separate API call to fetch an image file.
    """
    
    # STEP 1: Configure the QR code generator.
    # We use 'ERROR_CORRECT_M' (Medium), which allows the code to still be 
    # scannable even if up to 15% of the image is damaged or obscured.
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    
    # STEP 2: Add the data (the URL) and prepare the layout.
    qr.add_data(verification_url)
    qr.make(fit=True)

    # STEP 3: Create the actual image object.
    img = qr.make_image(fill_color="black", back_color="white")
    
    # STEP 4: Convert the image to a Base64 string.
    # We 'save' the PNG image into our memory buffer instead of the hard drive.
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    # STEP 5: Read the bytes from the buffer and encode them to text.
    img_bytes = buffer.getvalue()
    base64_img = base64.b64encode(img_bytes).decode('utf-8')
    
    return base64_img
