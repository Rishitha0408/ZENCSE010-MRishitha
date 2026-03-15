import unittest
import base64
import cv2
import numpy as np
from app.services.qr_service import generate_qr_base64

class TestQRService(unittest.TestCase):
    def test_generate_qr_base64_valid_png(self):
        """Test that the generated QR code string encodes a valid PNG file."""
        test_url = "https://certishield.example.com/verify/12345"
        
        # Generate the base64 string
        base64_str = generate_qr_base64(test_url)
        self.assertIsNotNone(base64_str)
        self.assertIsInstance(base64_str, str)
        
        # Decode the string back to bytes
        try:
            image_bytes = base64.b64decode(base64_str)
        except Exception as e:
            self.fail(f"Failed to decode base64 string: {e}")
            
        # Verify the bytes start with the PNG magic number
        # PNG signature: b'\x89PNG\r\n\x1a\n'
        png_magic_number = b'\x89PNG\r\n\x1a\n'
        self.assertTrue(
            image_bytes.startswith(png_magic_number),
            "Decoded bytes do not form a valid PNG image (missing magic number)."
        )

    def test_generate_qr_decodes_correctly(self):
        """Test that the generated QR code can be decoded back to the original URL."""
        test_url = "https://certishield.example.com/verify/unique-id"
        
        # 1. Generate QR base64
        base64_str = generate_qr_base64(test_url)
        
        # 2. Convert base64 to image bytes
        image_bytes = base64.b64decode(base64_str)
        
        # 3. Use OpenCV to decode the QR code
        # Convert bytes to a numpy array that OpenCV can read
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Initialize the QRCode detector
        detector = cv2.QRCodeDetector()
        
        # Detect and decode
        data, vertices, binary_qrcode = detector.detectAndDecode(img)
        
        self.assertEqual(data, test_url, f"Decoded QR data '{data}' does not match original URL '{test_url}'")

if __name__ == '__main__':
    unittest.main()
