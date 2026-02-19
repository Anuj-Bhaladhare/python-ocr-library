"""
    * Understanding Layout Structure
        - Block structure
        - Line structure
        - Span structure
        - Word structure
        - Reading hierarchy properly

    👉 Practice: Print structured layout tree.
"""

# ------------------------------------------------------------
# 1️⃣ Import Required Library
# ------------------------------------------------------------
import fitz
import os
import json


# ------------------------------------------------------------
# 2️⃣ File Path Initialization
# ------------------------------------------------------------
file_path = "./../pdf_data/ansible-for-devops.pdf"
output_path = "./../output_data/pdf_file/understand_layout_structure.pdf"


# ------------------------------------------------------------
# 3️⃣ Open Document
# ------------------------------------------------------------
doc = fitz.open(file_path)
page = doc[15]       # First page for demonstration

print("\n============== LAYOUT STRUCTURE ANALYSIS ==============\n")



# ------------------------------------------------------------
# 4️⃣ Extract Structured Layout (DICT FORMAT) | key : value pair me data store karta hai
# ------------------------------------------------------------

layout = page.get_text("dict")

block_layout = layout["blocks"]

# print(f"Total Blocks Found: {block_layout}\n")

# # Create folder if not exists
# os.makedirs("./output", exist_ok=True)

# # Save JSON
# with open("./output/understand_layout_structure.json", "w", encoding="utf-8") as f:
#     json.dump(layout, f, indent=4, default=str)


# print("JSON saved successfully!")




# ------------------------------------------------------------
# 5️⃣ Traverse Layout Hierarchy Properly | 
# ------------------------------------------------------------
for block_index, block in enumerate(layout["blocks"]):

    print(f"\n📦 BLOCK {block_index}")
    print("Type:", block["type"])  # 0 = text, 1 = image
    print("Block BBox:", block["bbox"])

    # Skip non-text blocks (images etc.)
    if block["type"] != 0:
        continue

    # -------------------------
    # LINE LEVEL
    # -------------------------
    for line_index, line in enumerate(block["lines"]):

        print(f"   ├── 📝 LINE {line_index}")
        print("   │   Line BBox:", line["bbox"])

        # -------------------------
        # SPAN LEVEL
        # -------------------------
        for span_index, span in enumerate(line["spans"]):

            print(f"   │     ├── 🔤 SPAN {span_index}")
            print("   │     │   Text:", span["text"])
            print("   │     │   Font:", span["font"])
            print("   │     │   Size:", span["size"])
            print("   │     │   Color:", span["color"])
            print("   │     │   Span BBox:", span["bbox"])




# ------------------------------------------------------------
# 6️⃣ Word-Level Structure
# ------------------------------------------------------------
"""
    Word 0:
        - Text: Foreword
        - BBox: (54.0, 115.18182373046875, 172.39613342285156, 140.10079956054688)
        - Block No: 0
        - Line No: 0
        - Word No: 0
"""
print("\n========== WORD LEVEL STRUCTURE ==========\n")

words = page.get_text("words")

for word_index, word in enumerate(words[:20]):  # Limit to first 20 words

    x0, y0, x1, y1, text, block_no, line_no, word_no = word

    print(f"Word {word_index}:")
    print("   Text:", text)
    print("   BBox:", (x0, y0, x1, y1))
    print("   Block No:", block_no)
    print("   Line No:", line_no)
    print("   Word No:", word_no)
    print()



# ------------------------------------------------------------
# 7️⃣ Close Document
# ------------------------------------------------------------
doc.close()

print("\n Layout Structure Analysis Completed Successfully \n")
