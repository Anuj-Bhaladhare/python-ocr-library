"""
================================================================
LINE-LEVEL TEXT EXTRACTION + BOUNDING BOX DRAWING
================================================================

This script demonstrates:

1. Extracting full line text from a PDF
2. Storing line text and bounding boxes in structured format
3. Drawing rectangles around each text line
4. Saving the modified PDF properly

Author: ANUJ
"""

import os
import fitz  # PyMuPDF


# ==============================================================
# CONFIGURATION
# ==============================================================

INPUT_PDF = "./input/ifss_orignal_bill.pdf"
OUTPUT_PDF = "./output/key_value_exact_bbox.pdf"


# ==============================================================
# FUNCTION: Extract Line Data
# ==============================================================

def extract_line_data(page):
    """
    Extract all text lines with their bounding boxes.

    Returns:
        List of dictionaries:
        [
            {
                "text": "Full line text",
                "bbox": (x0, y0, x1, y1)
            }
        ]
    """

    line_text_blocks = []

    # Extract structured text dictionary
    text_data = page.get_text("dict")

    for block in text_data["blocks"]:

        # Process only text blocks
        if block["type"] == 0:

            for line in block["lines"]:

                # Extract full line text by combining spans
                line_text = ""
                for span in line["spans"]:
                    line_text += span["text"]

                # Extract bounding box
                x0, y0, x1, y1 = line["bbox"]

                # Store structured data
                line_text_blocks.append({
                    "text": line_text.strip(),
                    "bbox": (x0, y0, x1, y1)
                })

    return line_text_blocks



# ==============================================================
# FUNCTION: Extract Value by Using Key
# ==============================================================

# Find VALUE from list of array by using the KEY
def find_value_from_lines(line_data, search_key):

    for line in line_data:
        text = line["text"]

        if search_key.lower() in text.lower():
            parts = text.split(":", 1)

            if len(parts) > 1:
                return parts[1].strip()

    return None

# Find VALUE from list of array by using the KEY | Advance KEY and VALUE Extractor
def smart_key_value_extractor(line_data, search_key):
    """
    Try multiple extraction strategies:
    1. Same-line colon split
    2. Same-row neighbor
    3. Below-row neighbor
    """

    # Step 1: Find key line
    for line in line_data:
        if search_key.lower() in line["text"].lower():

            key_line = line
            key_text = line["text"]

            # --------------- Case 1: Colon Based ---------------
            if ":" in key_text:
                return key_text.split(":", 1)[1].strip()

            # --------------- Case 2 & 3: Layout Based ---------------
            key_x0, key_y0, key_x1, key_y1 = key_line["bbox"]

            for candidate in line_data:
                cx0, cy0, cx1, cy1 = candidate["bbox"]

                # Same row (horizontal)
                if abs(cy0 - key_y0) < 5 and cx0 > key_x1:
                    return candidate["text"]

                # Below row (vertical)
                if 0 < (cy0 - key_y1) < 20:
                    return candidate["text"]

    return None

# Find VALUE, KEY Bonding Box, VALUE Bonding Box by Using PAGE and KEY data
def get_key_value_bbox(page, search_key):
    """
    Returns:
        {
            "key_bbox": (x0, y0, x1, y1),
            "value_bbox": (x0, y0, x1, y1),
            "value_text": "31-01-2026"
        }
    """

    words = page.get_text("words")

    # Group words by (block_no, line_no)
    lines = {}

    for w in words:
        x0, y0, x1, y1, text, block_no, line_no, word_no = w
        key = (block_no, line_no)

        if key not in lines:
            lines[key] = []

        lines[key].append(w)

    # Process each line
    for line_words in lines.values():

        # Sort words left to right
        line_words.sort(key=lambda w: w[0])

        full_line = " ".join([w[4] for w in line_words])

        if search_key.lower() in full_line.lower():

            key_words = []
            value_words = []
            colon_found = False

            for w in line_words:
                if ":" in w[4]:
                    colon_found = True
                    key_words.append(w)
                elif not colon_found:
                    key_words.append(w)
                else:
                    value_words.append(w)

            # Combine bbox function
            def combine_bbox(word_list):
                x0 = min(w[0] for w in word_list)
                y0 = min(w[1] for w in word_list)
                x1 = max(w[2] for w in word_list)
                y1 = max(w[3] for w in word_list)
                return (x0, y0, x1, y1)

            key_bbox = combine_bbox(key_words)
            value_bbox = combine_bbox(value_words)

            value_text = " ".join([w[4] for w in value_words])

            return {
                "key_bbox": key_bbox,
                "value_bbox": value_bbox,
                "value_text": value_text
            }

    return None



# ==============================================================
# FUNCTION: Draw Bounding Boxes
# ==============================================================

def draw_line_boxes(page, line_data):
    """
    Draw rectangles around extracted lines.
    """

    key_x0, key_y0, key_x1, key_y1 = line_data["key_bbox"]
    key_rect = fitz.Rect(key_x0, key_y0, key_x1 - 2.5, key_y1)
    page.draw_rect(
        key_rect,
        color=(1, 0, 0),  # RED color (RGB normalized)
        width=0.5
    )

    value_x0, value_y0, value_x1, value_y1 = line_data["value_bbox"]
    value_rect = fitz.Rect(value_x0, value_y0, value_x1, value_y1)
    page.draw_rect(
        value_rect,
        color=(0, 1, 0),  # Green color (RGB normalized)
        width=0.5
    )


# ==============================================================
# MAIN EXECUTION
# ==============================================================

def main(search_key):

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PDF), exist_ok=True)

    # Open document safely
    with fitz.open(INPUT_PDF) as doc:

        # Process only first page
        page = doc[0]

        # Step 1: Extract line data
        line_data = extract_line_data(page)

        # find_value_from = smart_key_value_extractor(line_data, search_key)
        # print(f"{search_key} = {find_value_from}")

        find_value_from = get_key_value_bbox(page, search_key)
        print(f"{search_key} = {find_value_from}")

        # Step 2: Draw bounding boxes
        draw_line_boxes(page, find_value_from)

        # Step 3: Save modified PDF
        doc.save(
            OUTPUT_PDF,
            garbage=4,
            deflate=True
        )

    print("Bounding boxes added successfully!")


if __name__ == "__main__":

    # Add Your KEY to find VALUE
    search_key = "Bank Branch IFSC"

    main(search_key)


    




































































































































































































































































































































# """
#     => Word-Level Engineering
#         - Keyword search using coordinates
#         - Extract values near keywords
#         - Build invoice field extractor

#         👉 Practice: Extract:
#             - Invoice number
#             - Date
#             - Total amount

#     ==========================================
#     1️⃣ Get word-level data (page.get_text("words"))
#     2️⃣ Convert into structured format
#     3️⃣ Search for keywords
#     4️⃣ Look for words to the RIGHT of keyword (same line)
#     5️⃣ Extract probable value
#     6️⃣ Draw bounding boxes for visualization
#     ==========================================
# """ 

# # ---------------------------------------------------------
# # 1. Import Required Librares
# # ---------------------------------------------------------
# import fitz
# import os
# import re



# # ---------------------------------------------------------
# # 2. Initialize File Path
# # ---------------------------------------------------------
# file_path = "./input/ifss_orignal_bill.pdf"
# output_path = "./output/key_value_bonding_box.pdf"


# # ---------------------------------------------------------
# # 3. Open Document
# # ---------------------------------------------------------
# doc = fitz.open(file_path)
# page = doc[0]     # Assume invoice on first page


# # ---------------------------------------------------------
# # 2️⃣ Extract Line-Level Data (FIXED VERSION)
# # ---------------------------------------------------------

# text_dict = page.get_text("dict")

# line_data = []

# for block in text_dict["blocks"]:
    
#     # Only process text blocks
#     if block["type"] != 0:
#         continue
    
#     for line in block["lines"]:
        
#         line_text = ""
        
#         # Combine all spans to build full line text
#         for span in line["spans"]:
#             line_text += span["text"]
        
#         line_data.append({
#             "text": line_text.strip(),
#             "bbox": fitz.Rect(line["bbox"])   # exact line bbox
#         })



# # ---------------------------------------------------------
# # 3️⃣ Line-Level Key-Value Extraction
# # ---------------------------------------------------------
# # def extract_key_values_line(user_keywords):
# #     """
# #     Extract key-value pairs using line-level matching
# #     but compute exact word-level bounding boxes.

# #     Returns:
# #     [
# #         {
# #             "key": key_text,
# #             "value": value_text,
# #             "key_bbox": key_bbox,
# #             "value_bbox": value_bbox
# #         }
# #     ]
# #     """

# #     results = []

# #     text_dict = page.get_text("dict")

# #     for block in text_dict["blocks"]:

# #         if block["type"] != 0:
# #             continue

# #         for line in block["lines"]:

# #             # Collect words in this line
# #             words_in_line = []
# #             for span in line["spans"]:
# #                 for w in span["text"].split():
# #                     words_in_line.append(w)

# #             # Build full line text
# #             line_text = " ".join(words_in_line)
# #             normalized_line = re.sub(r'[:\.\-]+', ':', line_text)

# #             for keyword in user_keywords:

# #                 pattern = re.compile(rf'({re.escape(keyword)})\s*:\s*(.+)', re.I)
# #                 match = pattern.search(normalized_line)

# #                 if not match:
# #                     continue

# #                 key_text = match.group(1).strip()
# #                 value_text = match.group(2).strip()

# #                 key_tokens = key_text.split()
# #                 value_tokens = value_text.split()

# #                 key_bbox = None
# #                 value_bbox = None

# #                 key_index = 0
# #                 value_index = 0

# #                 # Iterate spans again for accurate bbox
# #                 for span in line["spans"]:

# #                     span_words = span["text"].split()
# #                     span_bbox = fitz.Rect(span["bbox"])

# #                     for word in span_words:

# #                         # --- Match key tokens ---
# #                         if key_index < len(key_tokens) and word.lower() == key_tokens[key_index].lower():
# #                             if key_bbox is None:
# #                                 key_bbox = span_bbox
# #                             else:
# #                                 key_bbox |= span_bbox
# #                             key_index += 1
# #                             continue

# #                         # --- Match value tokens ---
# #                         if value_index < len(value_tokens) and word == value_tokens[value_index]:
# #                             if value_bbox is None:
# #                                 value_bbox = span_bbox
# #                             else:
# #                                 value_bbox |= span_bbox
# #                             value_index += 1

# #                 results.append({
# #                     "key": key_text,
# #                     "value": value_text,
# #                     "key_bbox": key_bbox,
# #                     "value_bbox": value_bbox
# #                 })

# #     return results

# def extract_key_value_by_words(page, user_keywords):
#     """
#     Extract key-value pairs using word-level matching.
    
#     Supports:
#         - Single-word keys
#         - Multi-word keys
#         - Exact bounding boxes for key and value
    
#     Returns:
#     [
#         {
#             "key": key_text,
#             "value": value_text,
#             "key_bbox": fitz.Rect,
#             "value_bbox": fitz.Rect
#         }
#     ]
#     """

#     results = []

#     # Get word-level data
#     words = page.get_text("words")
    
#     # Structure words
#     word_data = []
#     for w in words:
#         x0, y0, x1, y1, text, block_no, line_no, word_no = w
#         word_data.append({
#             "text": text.strip(),
#             "bbox": fitz.Rect(x0, y0, x1, y1),
#             "line": line_no
#         })

#     # Group words by line
#     lines = {}
#     for w in word_data:
#         lines.setdefault(w["line"], []).append(w)


#     # Process each line
#     for line_words in lines.values():

#         print(f"sadfsdasd ====================> {line_words}")

#         # Sort words left to right
#         line_words.sort(key=lambda w: w["bbox"].x0)

#         for keyword in user_keywords:

#             key_tokens = keyword.split()
#             token_len = len(key_tokens)

#             # Slide window over words to detect multi-word key
#             for i in range(len(line_words) - token_len + 1):

#                 match = True
#                 for j in range(token_len):
#                     if line_words[i + j]["text"].lower() != key_tokens[j].lower():
#                         match = False
#                         break

#                 if not match:
#                     continue

#                 # -------------------
#                 # KEY FOUND
#                 # -------------------

#                 key_words = line_words[i:i + token_len]

#                 # Merge key bounding boxes
#                 key_bbox = key_words[0]["bbox"]
#                 for w in key_words[1:]:
#                     key_bbox |= w["bbox"]

#                 # -------------------
#                 # FIND VALUE (RIGHT SIDE WORDS)
#                 # -------------------

#                 value_words = []

#                 for k in range(i + token_len, len(line_words)):

#                     word_text = line_words[k]["text"]

#                     # Skip separators like ":" or "-"
#                     if word_text in [":", "-", "–"]:
#                         continue

#                     value_words.append(line_words[k])

#                 if not value_words:
#                     continue

#                 # Merge value bounding boxes
#                 value_bbox = value_words[0]["bbox"]
#                 for w in value_words[1:]:
#                     value_bbox |= w["bbox"]

#                 value_text = " ".join([w["text"] for w in value_words])

#                 results.append({
#                     "key": keyword,
#                     "value": value_text.strip(),
#                     "key_bbox": key_bbox,
#                     "value_bbox": value_bbox
#                 })

#     return results


# ---------------------------------------------------------
# 4️⃣ Example Usage
# ---------------------------------------------------------
# invoice_number = extract_key_value_by_words(page, ["State"])
# state_value = extract_key_values_line(["State"])


# print(f"invoice_number => {invoice_number}")
# print(f"state_value => {state_value}")


# key_rect = invoice_number[0]["key_bbox"]
# value_rect = invoice_number[0]["value_bbox"]

# page.draw_rect(
#     key_rect,
#     color = (1, 0, 0),
#     width = 1
# )

# page.draw_rect(
#     key_rect,
#     color = (1, 0, 0),
#     width = 1
# )

# print("✅ Rectangle drawn.")



# # ------------------------------------------------------------
# # 7️⃣ Save Output
# # ------------------------------------------------------------
# doc.save(output_path)
# doc.close()

# print("🎯 Drawing demo completed successfully.")
