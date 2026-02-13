# STEP-0: Folder & Imports (Foundation)
import cv2
import pytesseract
from pytesseract import Output
import numpy as np
from production_grade_invoice_understanding.test_code.test_function_classes import TestFunctionClasses

"""
    ChatGPT Documentation Link: https://chatgpt.com/c/697332fc-220c-8323-ade8-230bff1b19bc
    STEP-> 1️⃣ Read text with OCR
    STEP-> 2️⃣ Draw bounding boxes on every word
    STEP-> 3️⃣ Detect lines & blocks
    STEP-> 4️⃣ Find “Total / Final Total”
    STEP-> 5️⃣ Extract key → value pairs
    STEP-> 6️⃣ Export clean JSON output
"""

if __name__ == "__main__":

    # Classes Initilization
    test_function = TestFunctionClasses(ocr_data=None)

    # --------------------------------------------------------------
    # STEP-1: Read the Invoice Image
    # --------------------------------------------------------------
    image = cv2.imread("./../file_data/new_sample_invoice.jpg")
    # image = cv2.imread("./../file_data/scan_invoice.jpg")
    original = image.copy()


    # --------------------------------------------------------------
    # STEP-2: Preprocessing (OCR-Friendly Image)
    # --------------------------------------------------------------
    # Convert Image to Gray-Scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("./../outputs/gray_image.png", gray_image)
    
    # Add Blur Effect on that Image
    blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Convert Image to Binary Image
    _, thresh_image = cv2.threshold(
        gray_image,
        100,     # try 60, 80, 100
        255,
        cv2.THRESH_BINARY
    )
    cv2.imwrite("./../outputs/thresh_image.png", thresh_image)

    # Remove Noise From Image
    def noise_removal(gray_image):
        """
        OCR-safe noise removal:
        - Preserves text shape, thickness, and spacing
        - Removes only background noise and tiny speckles
        """

        # 1️⃣ Edge-preserving denoising (SAFE for text)
        denoised = cv2.fastNlMeansDenoising(
            gray_image,
            None,
            h=10,                  # noise strength (8–12 safe)
            templateWindowSize=7,
            searchWindowSize=21
        )

        # 2️⃣ Light adaptive threshold (text-safe)
        binary = cv2.adaptiveThreshold(
            denoised,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            10
        )

        # 3️⃣ Remove only tiny isolated noise (no text damage)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
            binary,
            connectivity=8
        )

        clean = np.zeros(binary.shape, dtype=np.uint8)

        MIN_AREA = 30  # keeps characters, removes dots/noise

        for i in range(1, num_labels):  # skip background
            if stats[i, cv2.CC_STAT_AREA] > MIN_AREA:
                clean[labels == i] = 255

        return clean
    
    noise_rm_image = noise_removal(thresh_image)
    cv2.imwrite("./../outputs/noise_rm_image.png", noise_rm_image)

    # Apply Erosion Effect
    def thin_font(image):
        image = cv2.bitwise_not(image)
        kernel = np.ones((2,2),np.uint8)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.bitwise_not(image)
        return (image)
    
    thin_font_image = thin_font(noise_rm_image)
    cv2.imwrite("./../outputs/thin_font_image.png", thin_font_image)

    # Apply Dilation on Image
    def thick_font(image):
        import numpy as np
        image = cv2.bitwise_not(image)
        kernel = np.ones((2,2),np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.bitwise_not(image)
        return (image)
    
    thick_font_image = thick_font(thin_font_image)
    cv2.imwrite("./../outputs/thick_font_image.png", thick_font_image)


    # --------------------------------------------------------------
    # STEP-3: OCR with Structured Data (Core Step)
    # --------------------------------------------------------------
    ocr_data = pytesseract.image_to_data(
        # thresh_image,
        thick_font_image,
        output_type=Output.DICT,
        config="--oem 3 --psm 6"
    )

    # Extract Lines for OCR Data
    line_text = test_function.build_lines_from_ocr(ocr_data)
    # print(f"line_text: {line_text}")


    # extract key value pairs from line
    key_value_pair = test_function.extract_key_value_pairs_from_line(line_text)
    print(f"key_value_pair: {key_value_pair}")

