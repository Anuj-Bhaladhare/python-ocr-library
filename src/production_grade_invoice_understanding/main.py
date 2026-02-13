# STEP-0: Folder & Imports (Foundation)
import cv2
import re
import math
import pytesseract
from pytesseract import Output
import numpy as np
import json

from collections import defaultdict

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
    ocr_data = pytesseract.image_to_data(
        # thresh_image,
        thick_font_image,
        output_type=Output.DICT,
        config="--oem 3 --psm 6"
    )
    print(f"STEP-3: OCR with Structured Data => \n {ocr_data}")



    # --------------------------------------------------------------
    # STEP-4: Draw Bounding Box on EACH WORD
    # --------------------------------------------------------------
    # for i in range(len(ocr_data["text"])):

    #     if int(ocr_data["left"][i] > 60):
    #         if ocr_data["level"][i] == 5: # WORD LEVEL ONLY

    #             x = ocr_data["left"][i]
    #             y = ocr_data["top"][i]
    #             w = ocr_data["width"][i]
    #             h = ocr_data["height"][i]
    #             text = ocr_data["text"][i]

    #             cv2.rectangle(original, (x, y), (x+w, y+h), (0, 255, 0), 2)
    #             cv2.putText(
    #                 original,
    #                 text,
    #                 (x, y-5),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1
    #             )
    # cv2.imwrite("./outputs/bbox_on_word_image.png", original)



    # --------------------------------------------------------------
    # STEP-5: Extract LINES (Important for Totals)
    # --------------------------------------------------------------
    lines = []
    for i in range(len(ocr_data["text"])):
        if ocr_data["level"][i] == 4:   # LINE LEVEL
            line_text = ocr_data["text"][i]
            x = ocr_data["left"][i]
            y = ocr_data["top"][i]
            w = ocr_data["width"][i]
            h = ocr_data["height"][i]

            cv2.rectangle(original, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(
                original,
                line_text,
                (x, y-5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1
            )

            lines.append({
                "text": line_text,
                "bbox": [x, y, x+w, y+h]
            })
    cv2.imwrite("./outputs/bbox_on_line_image.png", original)
    print(f"lines:=> {lines}")



    # --------------------------------------------------------------
    # STEP-6: Find "Final Total/Total" (KEY LOGIC)
    # --------------------------------------------------------------
    # def extract_value_right_of_key(ocr_data, key_bbox):
    #     key_x1, key_y1, key_x2, key_y2 = key_bbox
    #     key_center_y = (key_y1 + key_y2) // 2

    #     candidates = []

    #     for i in range(len(ocr_data["text"])):
    #         text = ocr_data["text"][i].strip()

    #         if not text:
    #             continue

    #         # Skip non-numeric words
    #         if not re.search(r"\d", text):
    #             continue

    #         x = ocr_data["left"][i]
    #         y = ocr_data["top"][i]
    #         w = ocr_data["width"][i]
    #         h = ocr_data["height"][i]

    #         # Must be to the right of the key
    #         if x <= key_x2:
    #             continue

    #         # Must be on the same line (Y overlap)
    #         word_center_y = y + h // 2
    #         if abs(word_center_y - key_center_y) > max(h, key_y2 - key_y1):
    #             continue

    #         # Distance scoring (closer is better)
    #         distance = math.hypot(x - key_x2, word_center_y - key_center_y)

    #         candidates.append({
    #             "text": text,
    #             "bbox": [x, y, x + w, y + h],
    #             "distance": distance,
    #             "conf": int(ocr_data["conf"][i])
    #         })

    #     if not candidates:
    #         return None

    #     # Best candidate = closest
    #     best = sorted(candidates, key=lambda x: x["distance"])[0]
    #     return best

    # def extract_invoice_keys(ocr_data, KEYS):
    #     """
    #     Extract invoice-related keywords and bounding boxex from Tesseract OCR data.
    #     """

    #     invoice_keys_data = []

    #     # Pre-normalize keywords
    #     normalized_keys = {
    #         key_type: [k.lower() for k in key_list]
    #         for key_type, key_list in KEYS.items()
    #     }

    #     n = len(ocr_data["text"])

    #     for i in range(n):
    #         # We only care about word-level OCR results
    #         if ocr_data["level"][i] != 5:
    #             continue

    #         word = ocr_data["text"][i].strip()
    #         if not word:
    #             continue

    #         word_lower = word.lower()

    #         # Check against all key categories
    #         for key_type, keywords in normalized_keys.items():
    #             for keyword in keywords:

    #                 # Match keyword inside OCR word
    #                 if keyword in word_lower:
    #                     invoice_keys_data.append({
    #                         "field": key_type,
    #                         "matched_keyword": keyword,
    #                         "text": word,
    #                         "bbox": [
    #                             ocr_data["left"][i],
    #                             ocr_data["top"][i],
    #                             ocr_data["left"][i] + ocr_data["width"][i],
    #                             ocr_data["top"][i] + ocr_data["height"][i]
    #                         ],
    #                         "confidence": ocr_data.get("conf", [None])[i]
    #                     })

    #                     # Stop checking more keywords once matched
    #                     break

    #     return invoice_keys_data

    # KEYS = {
    #     "invoice_no": [
    #         "Invoice", "Bill No", "Reference Number", "Invoice ID", "Invoice No",
    #         "Inv No", "Invoice Num", "Bill Number"
    #     ],
    #     "date": [
    #         "Date", "Invoice Date", "Bill Date", "Dated", "Date of Issue",
    #         "Invoice Dt", "Bill Dt"
    #     ],
    #     "total": [
    #         "Total", "Grand Total", "Net Total", "Amount Payable", "Payable Amount",
    #         "Total Amount", "Gross Total", "Round Off Total", "Final Total"
    #     ],
    #     "gstin": [
    #         "GSTIN", "GST No", "GST Number", "GSTIN/Unique ID",
    #         "Recipient GSTIN", "Supplier GSTIN", "GST Identification Number"
    #     ]
    #     # You can add more categories later: "cgst", "sgst", "subtotal", "taxable_value", etc.
    # }

   
    # invoice_keys_data = extract_invoice_keys(ocr_data, KEYS)
    # print(f"invoice_keys_data:----> {invoice_keys_data}")


    # for item in invoice_keys_data:
    #     print(f"invoice_keys_data:----> {item}")

    # x, y, w, h = total_candidates["bbox"]

    # cv2.rectangle(original, (ocr_data["left"][i], ocr_data["top"][i]), (ocr_data["left"][i] + ocr_data["width"][i], ocr_data["top"][i] + ocr_data["height"][i]), (0, 255, 0), 2)
    # cv2.putText(
    #     original,
    #     word,
    #     (ocr_data["left"][i], ocr_data["top"][i]-5),
    #     cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1
    # )
    # cv2.imwrite("./outputs/AA_bbox_on_word_image.png", original)
                    




    # final_total = sorted(
    #     total_candidates,
    #     key=lambda x: x["bbox"][1],
    #     reverse=True
    # )[0]

    # # Find Exat Value of Key
    # value_data = extract_value_right_of_key(ocr_data, final_total["bbox"])

    # # key_x1, key_y1, key_x2, key_y2 = final_total["bbox"]          # KEY Cordinate of Bounding Box
    # # value_x1, value_y1, value_x2, value_y2 = value_data["bbox"]   # VALUE Cordinate of Bounding Box

    # # Create the JSON Object
    # invoice_json = {
    #     "total": {
    #         "key": final_total["text"],
    #         "value": value_data["text"] if value_data else None,
    #         "bbox": {
    #             "key": final_total["bbox"],
    #             "value": value_data["bbox"] if value_data else None
    #         },
    #         "confidence": value_data["conf"] / 100 if value_data else 0
    #     }
    # }

    # print(f"Final-Print: {invoice_json}")

    # # Extract KEY and VALUE Co-Ordinate for Bounding Box
    # key_x1, key_y1, key_x2, key_y2 = invoice_json["total"]["bbox"]["key"]               # KEY Cordinate of Bounding Box
    # value_x1, value_y1, value_x2, value_y2 = invoice_json["total"]["bbox"]["value"]     # VALUE Cordinate of Bounding Box

    # # Draw bounding box
    # cv2.rectangle(original, (key_x1, key_y1), (key_x2, key_y2), (0, 255, 0), 2)
    # cv2.rectangle(original, (value_x1, value_y1), (value_x2, value_y2), (0, 255, 0), 2)

    # # Draw label on KEY
    # cv2.putText(
    #     original,
    #     invoice_json["total"]["key"],
    #     (key_x1, key_y1-5),
    #     cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1
    # )

    # # Draw label on VALUE
    # cv2.putText(
    #     original,
    #     invoice_json["total"]["value"],
    #     (value_x1, value_y1-5),
    #     cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1
    # )

    # print(f"Final Print: {invoice_json}")

    # cv2.imwrite("./outputs/final_bbox_line_image.png", original)
