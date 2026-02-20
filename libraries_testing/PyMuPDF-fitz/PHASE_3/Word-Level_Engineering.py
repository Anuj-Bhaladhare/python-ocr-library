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
file_path = "./../pdf_data/ansible-for-devops.pdf"
output_path = "./output/word-level-engineering.pdf"



# ---------------------------------------------------------
# 3. Open Document
# ---------------------------------------------------------
doc = fitz.open(file_path)
page = doc[15]     # Assume invoice on first page



# ---------------------------------------------------------
# 4. Extract Word-Level Data
# ---------------------------------------------------------
words = page.get_text("words")

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

print("Total Words Found: ", len(word_data))



# --------------------------------------------------------
# 5. Utility: Find Value Near Keyword 
# --------------------------------------------------------
def extract_value_near_keyword(keyword_list):
    """
    Search for keyword and return word(s) to the right on same line.
    """

    for word in word_data:

        if word["text"].lower() in keyword_list:

            keyword_bbox = word["bbox"]
            keyword_line = word["line"]

            # Look for words on same line and to the right
            candidate_words = []

            for other_word in word_data:

                if (
                    other_word["line"] == keyword_line
                    and other_word["bbox"].x0 > keyword_bbox.x1
                ):
                    candidate_words.append(other_word)

            # Sort by x coordinate (left to right)
            candidate_words.sort(key=lambda w: w["bbox"].x0)

            if candidate_words:
                return candidate_words[0]  # Return closest right-side word

    return None




# -----------------------------------------------------------------
# 6. Extract Invoice Fields
# -----------------------------------------------------------------
invoice_number = extract_value_near_keyword(["invoice", "invoice no", "inv"])
date_value = extract_value_near_keyword(["date"])
total_amount = extract_value_near_keyword(["total", "amount"])




# ------------------------------------------------------------
# 7️⃣ Print Extracted Results
# ------------------------------------------------------------
print("\n========== EXTRACTED FIELDS ==========")

if invoice_number:
    print("Invoice Number:", invoice_number["text"])
else:
    print("Invoice Number: Not Found")

if date_value:
    print("Date:", date_value["text"])
else:
    print("Date: Not Found")

if total_amount:
    print("Total Amount:", total_amount["text"])
else:
    print("Total Amount: Not Found")



# -------------------------------------------------------------
# 8. Draw Bounding Boxes Around Extracted Values
# -------------------------------------------------------------
for field in [invoice_number, date_value, total_amount]:
    if field:
        page.draw_rect(field["bbox"], color=(1, 0, 0), width = 2)




# ------------------------------------------------------------
# 9️⃣ Save Output PDF
# ------------------------------------------------------------
doc.save(output_path)
doc.close()

print("\nInvoice Field Extraction Completed.")
print("Output Saved At:", output_path)

