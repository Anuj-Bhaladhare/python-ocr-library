# preprocessing.py
import cv2, os   # OpenCV for Computer Vision
import pytesseract
import numpy as np
from matplotlib import pyplot as plt

class PreProcessingPhase:
    def __init__(self, data=None):
        self.data = data
        self.image_file = "./data/bill_sample.png"
        self.img = cv2.imread(self.image_file)

        os.makedirs("./output_data", exist_ok=True)

    # Binarization || Gray Image | Black and White
    def Binarization(self):

        # Convert to Gray
        gray_image = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("./output_data/gray_image.jpg", gray_image)

        # Thresholding
        _, im_bw = cv2.threshold(gray_image, 210, 255, cv2.THRESH_BINARY)
        cv2.imwrite("./output_data/black_and_white.jpg", im_bw)

        # Remove Noise
        kernel = np.ones((1, 1), np.uint8)
        no_noise = cv2.morphologyEx(im_bw, cv2.MORPH_CLOSE, kernel)
        no_noise = cv2.medianBlur(no_noise, 3)
        cv2.imwrite("./output_data/no_noise.jpg", no_noise)

        # Thin Font
        thin_font = cv2.bitwise_not(no_noise)
        kernel = np.ones((2, 2), np.uint8)
        thin_font = cv2.erode(thin_font, kernel, iterations=1)
        thin_font = cv2.bitwise_not(thin_font)
        cv2.imwrite("./output_data/thin_font.jpg", thin_font)

        # Thick Font
        thick_font = cv2.bitwise_not(thin_font)
        thick_font = cv2.dilate(thick_font, kernel, iterations=1)
        thick_font = cv2.bitwise_not(thick_font)
        cv2.imwrite("./output_data/thick_font.jpg", thick_font)

        # OCR TEXT EXTRACTION
        # text = self.extract_text(thick_font)
        text = self.extract_text(im_bw)


        return text
    
    # -------------------------------
    # TEXT EXTRACTION USING TESSERACT
    # -------------------------------
    def extract_text(self, image):

        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)

        with open("./output_data/extracted_text.txt", "w", encoding="utf-8") as f:
            f.write(text)

        print("Extracted Text:\n")
        print(text)

        return text