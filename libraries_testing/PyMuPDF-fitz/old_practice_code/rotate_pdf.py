# Rotate the PDF Page

import fitz

# Open the PDF file here
# pdf = fitz.open("./pdf_data/ansible-for-devops.pdf")
pdf = fitz.open("./pdf_data/Unit-14.pdf") 

# Create empty varaible as pdf2
pdf2 = fitz.open()

# page count
pdf_page = pdf.page_count

pdf2.insert_pdf(
    pdf,
    from_page = 0,
    to_page = pdf_page - 1,
    rotate = 180  # PyMuPDF only allows rotation in multiples of 90 degrees - ["0", "90", "180", "270"]
)

pdf2.save("./output_data/pdf_file/rotatade_pdf.pdf")
