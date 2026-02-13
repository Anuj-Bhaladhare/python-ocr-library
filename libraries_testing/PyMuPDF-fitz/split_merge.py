# split pdf
# merge pdf

import fitz

# # Open the PDF file here
# pdf = fitz.open("./pdf_data/ansible-for-devops.pdf")
# # pdf = fitz.open("./pdf_data/Unit-14.pdf") 
# page_count = pdf.page_count
# # -------------> Split PDF <-------------
# pdf2 = fitz.open()
# pdf3 = fitz.open()

# pdf2.insert_pdf(
#     pdf,
#     from_page = 0,
#     to_page = 45 - 1
# )
# pdf2.save("./output_data/pdf_file/splitted_pdf_1_45.pdf")

# pdf3.insert_pdf(
#     pdf,
#     from_page = 46 - 1,
#     to_page = page_count - 1
# )
# pdf3.save("./output_data/pdf_file/splitted_pdf_46_end.pdf")





# -------------> Merge PDF <-------------
pdf = fitz.open("./output_data/pdf_file/splitted_pdf_1_45.pdf")
pdf2 = fitz.open("./output_data/pdf_file/splitted_pdf_46_end.pdf")

page_count = pdf2.page_count

pdf.insert_pdf(
    pdf2,
    from_page = 0,
    to_page = page_count - 1
)

pdf.save("./output_data/pdf_file/NEW_merged_pdf.pdf")
