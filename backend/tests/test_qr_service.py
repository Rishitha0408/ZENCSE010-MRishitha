import unittest
import base64
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

if __name__ == '__main__':
    unittest.main()
