import pytesseract
from PIL import Image
import shutil
import os
import cv2
import numpy as np

class OCREngine:
    def __init__(self, tesseract_cmd=None):
        self.tesseract_cmd = tesseract_cmd or self._find_tesseract()
        if self.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
        else:
            print("Warning: Tesseract executable not found. OCR will not work.")

    def _find_tesseract(self):
        # Check specific paths on Windows
        paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            shutil.which("tesseract")
        ]
        for path in paths:
            if path and os.path.exists(path):
                return path
        return None

    def extract_text(self, image_path):
        """
        Extracts text from an image using Tesseract OCR.
        Preprocesses image for better results.
        """
        if not self.tesseract_cmd:
            return None

        try:
            # Preprocessing using OpenCV
            img = on_img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Apply thresholding
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            
            # Temporary file for Tesseract
            temp_filename = f"{image_path}_temp.png"
            cv2.imwrite(temp_filename, gray)

            text = pytesseract.image_to_string(Image.open(temp_filename))
            
            # Clean up
            os.remove(temp_filename)
            return text
        except Exception as e:
            print(f"Error extracting text: {e}")
            return None

    def extract_address(self, text):
        """
        Parses raw text to find address-like patterns.
        """
        # Simple heuristic: Look for lines with digits (house number) and text (street)
        # Verify it's not just a barcode number
        lines = text.split('\n')
        candidates = []
        for line in lines:
            clean_line = line.strip()
            if len(clean_line) > 5 and any(c.isdigit() for c in clean_line) and any(c.isalpha() for c in clean_line):
                candidates.append(clean_line)
        
        # Return the longest candidate for now, assuming it's the full address
        if candidates:
            return max(candidates, key=len)
        return text.strip()
