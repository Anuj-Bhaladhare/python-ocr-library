"""
3️⃣ Working with Pages in PyMuPDF

This script demonstrates:

✔ Access page by index
✔ Iterating through all pages
✔ Reading page properties:
      - rotation
      - mediabox
      - rect
      - cropbox
✔ Printing full page information
"""

# --------------------------------------------------------
# 1️⃣ Import Library
# --------------------------------------------------------
import fitz  # PyMuPDF


# --------------------------------------------------------
# 2️⃣ Initialize File Paths
# --------------------------------------------------------
file_path = "./../pdf_data/ansible-for-devops.pdf"
output_path = "./../output_data/pdf_file/working_with_pages.pdf"


# --------------------------------------------------------
# 3️⃣ Open the PDF Document
# --------------------------------------------------------
pdf_document = fitz.open(file_path)

print("Document opened successfully!")
print("Total Page in Document: ", pdf_document.page_count)



# --------------------------------------------------------
# 4️⃣ Access Page by Index
# --------------------------------------------------------
"""
    Important:
        - Page indexing starting from 0

    Example:
        - Index 0 -> Page 1
        - Index 4 -> Page 5
"""

page_5 = pdf_document[4]    # Access 5th page

print("\n--- Accessing Page by Index (Page 5) ---")
print("Page Number (0-based Index): ", page_5.number)
print("Page Rotation:", page_5.rotation)

# Print text from page 5 (basic preview)
print("\nText Preview from Page 5:\n")
print(page_5.get_text("text"))



# --------------------------------------------------------
# 5️⃣ Iterating Through All Pages
# --------------------------------------------------------
"""
This is the recommended production method
to process every page in a PDF
"""

print("\n--- Iterating Through All Pages ---")
for page_index in range(pdf_document.page_count):

    page = pdf_document[page_index]

    print(f"\nProcessing Page {page_index + 1}")
    print("Page Index: ", page.number)

    # Example: Count number of words
    words = page.get_text("words")
    print("Total Words on Page:", len(words))




# --------------------------------------------------------
# 6️⃣ Page Properties
# --------------------------------------------------------
"""
Each page has multiple geometry-related properties.
These are extremely important for layout engineering.
"""

print("\n--- Page Properties (For Each Page) ---")

for page_index in range(pdf_document.page_count):

    page = pdf_document[page_index]

    print(f"\n===== Page {page_index + 1} =====")

    # 🔹 Rotation
    # 0, 90, 180, 270 degrees
    print("Rotation:", page.rotation)

    # 🔹 MediaBox
    # Defines full physical page size
    print("MediaBox:", page.mediabox)

    # 🔹 Rect
    # Visible page rectangle (commonly used for layout)
    print("Rect:", page.rect)

    # 🔹 CropBox
    # Defines visible region after cropping
    print("CropBox:", page.cropbox)

    # Page width & height (commonly used in production)
    print("Width:", page.rect.width)
    print("Height:", page.rect.height)



# --------------------------------------------------------
# 7️⃣ Save a Copy (Optional Practice)
# --------------------------------------------------------
pdf_document.save(output_path)
print("\nSaved processed copy to:", output_path)


# --------------------------------------------------------
# 8️⃣ Close Document (VERY IMPORTANT)
# --------------------------------------------------------
pdf_document.close()
print("\nDocument closed successfully.")
