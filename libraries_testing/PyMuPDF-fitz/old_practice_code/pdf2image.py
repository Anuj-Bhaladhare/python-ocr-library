# ======================================================
# ===================> PDF to Image <===================
# ======================================================

import fitz  # PyMuPDF

# Open the PDF file
pdf = fitz.open("./pdf_data/Unit-14.pdf")

# Load page 2 (index 1 because pages start at 0)
page = pdf.load_page(1)

# Create pixmap (image of the page)
pix = page.get_pixmap()
print(pix)

# Save as an image
pix.save("./output_data/image_file/page_2.png")

# Close the PDF
pdf.close()

# ======================================================






# # ======================================================
# # ===================> Image to PDF <===================
# # ======================================================
# import img2pdf

# img = "./pdf_data/ben-10-image.png"

# with open("./output_data/pdf_file/ben-10-image.pdf", 'wb') as file:
#     file.write(img2pdf.convert(img))

