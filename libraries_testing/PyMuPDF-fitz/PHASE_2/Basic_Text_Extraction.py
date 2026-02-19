"""
Basic Text Extraction using PyMuPDF

This script demonstrates:

✔ page.get_text()
✔ Output types:
      - "text"
      - "blocks"
      - "words"
      - "dict"
      - "rawdict"
      - "html"
      - "markdown"

👉 Practice: Compare outputs of all types.
"""

# ----------------------------------------------------------
# 1️⃣ Import Required Libraries
# ----------------------------------------------------------
import fitz          # PyMuPDF
import json          # For saving dict & rawdict as JSON
import os


# ----------------------------------------------------------
# 2️⃣ Initialize File Paths
# ----------------------------------------------------------
file_path = "./../pdf_data/ansible-for-devops.pdf"

# Create Directory "output" if not exist
output_directory = "./output/"
os.makedirs(output_directory, exist_ok=True)

output_path_text = os.path.join(output_directory, "Basic_Text_Extraction_text.txt")
output_path_blocks = os.path.join(output_directory, "Basic_Text_Extraction_blocks.txt")
output_path_words = os.path.join(output_directory, "Basic_Text_Extraction_words.txt")
output_path_dict = os.path.join(output_directory, "Basic_Text_Extraction_dict.json")
output_path_rawdict = os.path.join(output_directory, "Basic_Text_Extraction_rawdict.json")
output_path_html = os.path.join(output_directory, "Basic_Text_Extraction_html.html")
# output_path_markdown = os.path.join(output_directory, "Basic_Text_Extraction_markdown.md")


# ----------------------------------------------------------
# 3️⃣ Open PDF Document
# ----------------------------------------------------------
pdf_doc = fitz.open(file_path)

print("Document Opened Successfully!")
print("Total Pages:", pdf_doc.page_count)


# ----------------------------------------------------------
# 4️⃣ Access Specific Page (7th Page)
# ----------------------------------------------------------
# Index starts from 0 → Page 7 = index 6
page = pdf_doc[52]

print("\nExtracting content from Page 7...\n")


# ----------------------------------------------------------
# 5️⃣ Extract Different Output Types
# ----------------------------------------------------------

# 1. Plain Text
text_output = page.get_text("text")

# 2. Blocks (Grouped layout blocks)
blocks_output = page.get_text("blocks")

# 3. Words (Each word with bounding box)
words_output = page.get_text("words")

# 4. Dictionary (Structured layout tree)
dict_output = page.get_text("dict")

# 5. Raw Dictionary (More detailed internal structure)
rawdict_output = page.get_text("rawdict")

# 6. HTML Output
html_output = page.get_text("html")

# # 7. Markdown Output
# markdown_output = page.get_text("markdown")


# ----------------------------------------------------------
# 6️⃣ Save Outputs to Files
# ----------------------------------------------------------

# Save Text
with open(output_path_text, "w", encoding="utf-8") as f:
    f.write(text_output)

# Save Blocks
with open(output_path_blocks, "w", encoding="utf-8") as f:
    f.write(str(blocks_output))

# Save Words
with open(output_path_words, "w", encoding="utf-8") as f:
    f.write(str(words_output))

# Save Dict
with open(output_path_dict, "w", encoding="utf-8") as f:
    json.dump(dict_output, f, indent=4)

# Save RawDict
with open(output_path_rawdict, "w", encoding="utf-8") as f:
    json.dump(rawdict_output, f, indent=4)

# Save HTML
with open(output_path_html, "w", encoding="utf-8") as f:
    f.write(html_output)

# # Save Markdown
# with open(output_path_markdown, "w", encoding="utf-8") as f:
#     f.write(markdown_output)


print("All extraction formats saved successfully!")



# ----------------------------------------------------------
# 7️⃣ Close Document (IMPORTANT)
# ----------------------------------------------------------
pdf_doc.close()
print("Document closed properly.")

