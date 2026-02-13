# STEP-0: Folder & Imports (Foundation)
import cv2
import re
import math
import pytesseract
from pytesseract import Output
import numpy as np
import json
from production_grade_invoice_understanding.test_code.test_function_classes import TestFunctionClasses
from collections import defaultdict

# """
#     ChatGPT Documentation Link: https://chatgpt.com/c/697332fc-220c-8323-ade8-230bff1b19bc
#     STEP-> 1️⃣ Read text with OCR
#     STEP-> 2️⃣ Draw bounding boxes on every word
#     STEP-> 3️⃣ Detect lines & blocks
#     STEP-> 4️⃣ Find “Total / Final Total”
#     STEP-> 5️⃣ Extract key → value pairs
#     STEP-> 6️⃣ Export clean JSON output
# """

# if __name__ == "__main__":

#     # Classes Initilization
#     test_function = TestFunctionClasses(ocr_data=None)

#     # --------------------------------------------------------------
#     # STEP-1: Read the Invoice Image
#     # --------------------------------------------------------------
#     image = cv2.imread("./file_data/new_sample_invoice.jpg")
#     # image = cv2.imread("./file_data/scan_invoice.jpg")
#     original = image.copy()


#     # --------------------------------------------------------------
#     # STEP-2: Preprocessing (OCR-Friendly Image)
#     # --------------------------------------------------------------
#     # Convert Image to Gray-Scale
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     cv2.imwrite("./outputs/gray_image.png", gray_image)
    
#     # Add Blur Effect on that Image
#     blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

#     # Convert Image to Binary Image
#     _, thresh_image = cv2.threshold(
#         gray_image,
#         100,     # try 60, 80, 100
#         255,
#         cv2.THRESH_BINARY
#     )
#     cv2.imwrite("./outputs/thresh_image.png", thresh_image)

#     # Remove Noise From Image
#     def noise_removal(gray_image):
#         """
#         OCR-safe noise removal:
#         - Preserves text shape, thickness, and spacing
#         - Removes only background noise and tiny speckles
#         """

#         # 1️⃣ Edge-preserving denoising (SAFE for text)
#         denoised = cv2.fastNlMeansDenoising(
#             gray_image,
#             None,
#             h=10,                  # noise strength (8–12 safe)
#             templateWindowSize=7,
#             searchWindowSize=21
#         )

#         # 2️⃣ Light adaptive threshold (text-safe)
#         binary = cv2.adaptiveThreshold(
#             denoised,
#             255,
#             cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#             cv2.THRESH_BINARY,
#             31,
#             10
#         )

#         # 3️⃣ Remove only tiny isolated noise (no text damage)
#         num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
#             binary,
#             connectivity=8
#         )

#         clean = np.zeros(binary.shape, dtype=np.uint8)

#         MIN_AREA = 30  # keeps characters, removes dots/noise

#         for i in range(1, num_labels):  # skip background
#             if stats[i, cv2.CC_STAT_AREA] > MIN_AREA:
#                 clean[labels == i] = 255

#         return clean
    
#     noise_rm_image = noise_removal(thresh_image)
#     cv2.imwrite("./outputs/noise_rm_image.png", noise_rm_image)

#     # Apply Erosion Effect
#     def thin_font(image):
#         image = cv2.bitwise_not(image)
#         kernel = np.ones((2,2),np.uint8)
#         image = cv2.erode(image, kernel, iterations=1)
#         image = cv2.bitwise_not(image)
#         return (image)
    
#     thin_font_image = thin_font(noise_rm_image)
#     cv2.imwrite("./outputs/thin_font_image.png", thin_font_image)

#     # Apply Dilation on Image
#     def thick_font(image):
#         import numpy as np
#         image = cv2.bitwise_not(image)
#         kernel = np.ones((2,2),np.uint8)
#         image = cv2.dilate(image, kernel, iterations=1)
#         image = cv2.bitwise_not(image)
#         return (image)
    
#     thick_font_image = thick_font(thin_font_image)
#     cv2.imwrite("./outputs/thick_font_image.png", thick_font_image)


#     # --------------------------------------------------------------
#     # STEP-3: OCR with Structured Data (Core Step)
#     # --------------------------------------------------------------
#     ocr_data = pytesseract.image_to_data(
#         # thresh_image,
#         thick_font_image,
#         output_type=Output.DICT,
#         config="--oem 3 --psm 6"
#     )

#     # Extract Lines for OCR Data
#     line_text = test_function.build_lines_from_ocr(ocr_data)
#     # print(f"line_text: {line_text}")


#     # extract key value pairs from line
#     key_value_pair = test_function.extract_key_value_pairs_from_line(line_text)
#     print(f"key_value_pair: {key_value_pair}")






# # =====================================================================================
# # ========================= Detect Paragraph with help of Line ======================== 
# # =====================================================================================
# if __name__ == "__main__":

#     # Classes Initilization
#     test_function = TestFunction(ocr_data=None)

#     # --------------------------------------------------------------
#     # STEP-1: Read the Invoice Image
#     # --------------------------------------------------------------
#     image = cv2.imread("./file_data/new_sample_invoice.jpg")
#     # image = cv2.imread("./file_data/scan_invoice.jpg")
#     original = image.copy()


#     # --------------------------------------------------------------
#     # STEP-2: Preprocessing (OCR-Friendly Image)
#     # --------------------------------------------------------------
#     # Convert Image to Gray-Scale
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     cv2.imwrite("./outputs/gray_image.png", gray_image)
    
#     # Add Blur Effect on that Image
#     blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

#     # Convert Image to Binary Image
#     _, thresh_image = cv2.threshold(
#         gray_image,
#         100,     # try 60, 80, 100
#         255,
#         cv2.THRESH_BINARY
#     )
#     cv2.imwrite("./outputs/thresh_image.png", thresh_image)

#     # Remove Noise From Image
#     def noise_removal(gray_image):
#         """
#         OCR-safe noise removal:
#         - Preserves text shape, thickness, and spacing
#         - Removes only background noise and tiny speckles
#         """

#         # 1️⃣ Edge-preserving denoising (SAFE for text)
#         denoised = cv2.fastNlMeansDenoising(
#             gray_image,
#             None,
#             h=10,                  # noise strength (8–12 safe)
#             templateWindowSize=7,
#             searchWindowSize=21
#         )

#         # 2️⃣ Light adaptive threshold (text-safe)
#         binary = cv2.adaptiveThreshold(
#             denoised,
#             255,
#             cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#             cv2.THRESH_BINARY,
#             31,
#             10
#         )

#         # 3️⃣ Remove only tiny isolated noise (no text damage)
#         num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
#             binary,
#             connectivity=8
#         )

#         clean = np.zeros(binary.shape, dtype=np.uint8)

#         MIN_AREA = 30  # keeps characters, removes dots/noise

#         for i in range(1, num_labels):  # skip background
#             if stats[i, cv2.CC_STAT_AREA] > MIN_AREA:
#                 clean[labels == i] = 255

#         return clean
    
#     noise_rm_image = noise_removal(thresh_image)
#     cv2.imwrite("./outputs/noise_rm_image.png", noise_rm_image)

#     # Apply Erosion Effect
#     def thin_font(image):
#         image = cv2.bitwise_not(image)
#         kernel = np.ones((2,2),np.uint8)
#         image = cv2.erode(image, kernel, iterations=1)
#         image = cv2.bitwise_not(image)
#         return (image)
    
#     thin_font_image = thin_font(noise_rm_image)
#     cv2.imwrite("./outputs/thin_font_image.png", thin_font_image)

#     # Apply Dilation on Image
#     def thick_font(image):
#         import numpy as np
#         image = cv2.bitwise_not(image)
#         kernel = np.ones((2,2),np.uint8)
#         image = cv2.dilate(image, kernel, iterations=1)
#         image = cv2.bitwise_not(image)
#         return (image)
    
#     thick_font_image = thick_font(thin_font_image)
#     cv2.imwrite("./outputs/thick_font_image.png", thick_font_image)


#     # --------------------------------------------------------------
#     # STEP-3: OCR with Structured Data (Core Step)
#     # --------------------------------------------------------------
#     ocr_data = pytesseract.image_to_data(
#         # thresh_image,
#         thick_font_image,
#         output_type=Output.DICT,
#         config="--oem 3 --psm 3"
#     )

#     # Step 4: Extract paragraph bounding boxes
#     paragraphs = []
#     number_line = len(ocr_data["text"])

#     for i in range(number_line):
#         if ocr_data["level"][i] == 3: # PARA LEVEL ONLY

#             x = ocr_data["left"][i]
#             y = ocr_data["top"][i]
#             w = ocr_data["width"][i]
#             h = ocr_data["height"][i]

#             paragraphs.append({
#                 "bbox": (x, y, w, h),
#                 "text": ""
#             })


#     # Step 5: Fill paragraph text using WORDS inside bbox
#     for para in paragraphs:
#         px, py, pw, ph = para["bbox"]
#         para_text = []

#         for i in range(number_line):
#             if ocr_data["level"][i] == 5:  # WORD LEVEL
#                 wx = ocr_data["left"][i]
#                 wy = ocr_data["top"][i]
#                 ww = ocr_data["width"][i]
#                 wh = ocr_data["height"][i]
#                 word = ocr_data["text"][i]

#                 if word.strip() == "":
#                     continue

#                 # check if word lies inside paragraph bbox
#                 if (px <= wx <= px + pw) and (py <= wy <= py + ph):
#                     para_text.append(word)
        
#         para["text"] = " ".join(para_text)


#     print(f"paragraphs ====> {paragraphs}")
#     # Step 6: Draw paragraph bounding boxes
#     for para in paragraphs:
#         x, y, w, h = para["bbox"]
#         text = para["text"]

#         cv2.rectangle(original, (x, y), (x+w, y+h), (0, 255, 0), 2)

#         cv2.putText(
#             original,
#             text[:40] + "...",
#             (x, y - 5),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.4,
#             (0, 0, 255),
#             1
#         )

#     # Step 7: Save output
#     cv2.imwrite("./outputs/paragraph_detected.png", original)








# =====================================================================================
# ========================= Detect Paragraph with help of Line ======================== 
# =====================================================================================
if __name__ == "__main__":

    # Classes Initilization
    test_function = TestFunction(ocr_data=None)

    # --------------------------------------------------------------
    # STEP-1: Read the Invoice Image
    # --------------------------------------------------------------
    image = cv2.imread("./file_data/new_sample_invoice.jpg")
    # image = cv2.imread("./file_data/scan_invoice.jpg")
    original = image.copy()


    # --------------------------------------------------------------
    # STEP-2: Preprocessing (OCR-Friendly Image)
    # --------------------------------------------------------------
    # Convert Image to Gray-Scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("./outputs/gray_image.png", gray_image)
    
    # Add Blur Effect on that Image
    blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Convert Image to Binary Image
    _, thresh_image = cv2.threshold(
        gray_image,
        100,     # try 60, 80, 100
        255,
        cv2.THRESH_BINARY
    )
    cv2.imwrite("./outputs/thresh_image.png", thresh_image)

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
    cv2.imwrite("./outputs/noise_rm_image.png", noise_rm_image)

    # Apply Erosion Effect
    def thin_font(image):
        image = cv2.bitwise_not(image)
        kernel = np.ones((2,2),np.uint8)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.bitwise_not(image)
        return (image)
    
    thin_font_image = thin_font(noise_rm_image)
    cv2.imwrite("./outputs/thin_font_image.png", thin_font_image)

    # Apply Dilation on Image
    def thick_font(image):
        import numpy as np
        image = cv2.bitwise_not(image)
        kernel = np.ones((2,2),np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.bitwise_not(image)
        return (image)
    
    thick_font_image = thick_font(thin_font_image)
    cv2.imwrite("./outputs/thick_font_image.png", thick_font_image)


    # --------------------------------------------------------------
    # STEP-3: OCR with Structured Data (Core Step)
    # --------------------------------------------------------------
    ocr = pytesseract.image_to_data(
        thick_font_image,
        output_type=Output.DICT,
        config="--oem 3 --psm 4" # try [--psm 3, 4, 1]
    )

    n = len(ocr["text"])

    # STEP 3: Extract PARAGRAPH bounding boxes
    paragraphs = []

    for i in range(n):
        if ocr["level"][i] == 3:  # PARAGRAPH
            paragraphs.append({
                "bbox": (
                    ocr["left"][i],
                    ocr["top"][i],
                    ocr["width"][i],
                    ocr["height"][i]
                ),
                "lines": [],
                "text": ""
            })

    # STEP 4: Attach LINES to each paragraph
    for para in paragraphs:
        px, py, pw, ph = para["bbox"]

        for i in range(n):
            if ocr["level"][i] == 4:  # LINE
                lx = ocr["left"][i]
                ly = ocr["top"][i]
                lw = ocr["width"][i]
                lh = ocr["height"][i]

                if (px <= lx <= px + pw) and (py <= ly <= py + ph):
                    para["lines"].append({
                        "bbox": (lx, ly, lw, lh),
                        "words": []
                    })

    # STEP 5: Attach WORDS to their respective lines
    for para in paragraphs:
        for line in para["lines"]:
            lx, ly, lw, lh = line["bbox"]

            for i in range(n):
                if ocr["level"][i] == 5:  # WORD
                    word = ocr["text"][i].strip()
                    if not word:
                        continue

                    wx = ocr["left"][i]
                    wy = ocr["top"][i]

                    if (lx <= wx <= lx + lw) and (ly <= wy <= ly + lh):
                        line["words"].append(word)

    # STEP 6: Build final paragraph text (LINE-WISE)
    for para in paragraphs:
        para_lines_text = []

        for line in para["lines"]:
            line_text = " ".join(line["words"])
            if line_text.strip():
                para_lines_text.append(line_text)

        para["text"] = "\n".join(para_lines_text)

    # STEP 7: Draw paragraph bounding boxes
    for para in paragraphs:
        x, y, w, h = para["bbox"]

        cv2.rectangle(original, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.putText(
            original,
            para["text"].split("\n")[0][:40],
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0, 0, 255),
            1
        )

    # STEP 8: Save output
    cv2.imwrite("./outputs/paragraph_detected_2nd_type.png", original)
