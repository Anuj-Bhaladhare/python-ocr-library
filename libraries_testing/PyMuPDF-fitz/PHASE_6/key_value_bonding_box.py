# --------------------------------------------------------------------
# |                                                                  |
# |         Properlly Working Code for Single Word KEY               |
# |                                                                  |
# --------------------------------------------------------------------

"""
    => Word-Level Engineering
        - Keyword search using coordinates
        - Extract values near keywords
        - Build invoice field extractor

        👉 Practice: Extract:
            - Invoice number
            - Date
            - Total amount

    ==========================================
    1️⃣ Get word-level data (page.get_text("words"))
    2️⃣ Convert into structured format
    3️⃣ Search for keywords
    4️⃣ Look for words to the RIGHT of keyword (same line)
    5️⃣ Extract probable value
    6️⃣ Draw bounding boxes for visualization
    ==========================================
""" 

# ---------------------------------------------------------
# 1. Import Required Librares
# ---------------------------------------------------------
import fitz
import os
import re



# ---------------------------------------------------------
# 2. Initialize File Path
# ---------------------------------------------------------
file_path = "./input/ifss_orignal_bill.pdf"
output_path = "./output/key_value_bonding_box.pdf"


# ---------------------------------------------------------
# 3. Open Document
# ---------------------------------------------------------
doc = fitz.open(file_path)
page = doc[0]     # Assume invoice on first page



# ---------------------------------------------------------
# 4. Extract Word-Level Data
# ---------------------------------------------------------
words = page.get_text("words")

# print(f"words => {words}")

# Structure words into dictionaries for easier handling
word_data = []

for w in words:
    x0, y0, x1, y1, text, block_no, line_no, word_no = w

    word_data.append({
        "text": text.strip(),
        "bbox": fitz.Rect(x0, y0, x1, y1),
        "block": block_no,
        "line": line_no
    })


# print(f"word_data => {word_data}")


def extract_key_values_with_bbox(user_keywords):
    """
    Extract key-value pairs and their bounding boxes from PDF.
    Returns list of dicts: key, value, key_bbox, value_bbox
    """

    results = []

    # Group words by line
    lines = {}
    for w in word_data:
        lines.setdefault(w["line"], []).append(w)

    for line_no, line_words in lines.items():
        # Sort left to right
        line_words.sort(key=lambda w: w["bbox"].x0)
        # Merge line text
        full_line = " ".join([w["text"] for w in line_words])
        # Normalize separators
        normalized_line = re.sub(r'[:\.\-]+', ':', full_line)

        for keyword in user_keywords:

            # Regex to capture value
            pattern = re.compile(
                rf'({re.escape(keyword)})\s*:\s*([\S ]+?)(?=\s+[A-Z]|$)',
                re.I
            )

            match = pattern.search(normalized_line)

            if match:
                value_text = match.group(2).strip()
                key_text = match.group(1).strip()

                # Find words in line that belong to key
                key_words = [w for w in line_words if key_text.lower() in w["text"].lower()]

                # Find words in line that belong to value
                value_words = []
                # split value text into words
                value_tokens = value_text.split()
                idx = 0
                for w in line_words:
                    if idx < len(value_tokens) and w["text"].strip() == value_tokens[idx]:
                        value_words.append(w)
                        idx += 1

                # Merge bounding boxes
                if key_words:
                    key_bbox = key_words[0]["bbox"]
                    for w in key_words[1:]:
                        key_bbox |= w["bbox"]  # union of rects
                else:
                    key_bbox = None

                if value_words:
                    value_bbox = value_words[0]["bbox"]
                    for w in value_words[1:]:
                        value_bbox |= w["bbox"]
                else:
                    value_bbox = None

                results.append({
                    "key": key_text,
                    "value": value_text,
                    "key_bbox": key_bbox,
                    "value_bbox": value_bbox
                })

    return results


# -----------------------------------------------------------------
# 6. Extract Invoice Fields
# -----------------------------------------------------------------
invoice_number = extract_key_values_with_bbox(["State", "Invoice Date"])
# date_value = extract_value_near_keyword(["date", "marker"])
# total_amount = extract_value_near_keyword(["total", "amount", "Make"])

print(f"invoice_number => {invoice_number}")

key_rect = invoice_number[0]["key_bbox"]
value_rect = invoice_number[0]["value_bbox"]

page.draw_rect(
    key_rect,
    color = (1, 0, 0),
    width = 1
)

page.draw_rect(
    value_rect,
    color = (0, 1, 0),
    width = 1
)
print("✅ Rectangle drawn.")



# ------------------------------------------------------------
# 7️⃣ Save Output
# ------------------------------------------------------------
doc.save(output_path)
doc.close()

print("🎯 Drawing demo completed successfully.")


first understand the function of extract_key_values_with_bbox -> IMP / Verry IMP



































































































































































































































































































































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
