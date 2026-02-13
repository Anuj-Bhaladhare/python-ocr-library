# Extract pdf pages

import fitz

# Open the PDF file here
# pdf = fitz.open("./pdf_data/ansible-for-devops.pdf")
pdf = fitz.open("./pdf_data/Unit-14.pdf") 
pdf2 = fitz.open()

# page number where you wan to break page
from_page = 2 - 1
to_page = 2 - 1

pdf2.insert_pdf(
    pdf, 
    from_page = from_page,
    to_page = to_page
)

pdf2.save(f"./output_data/pdf_file/page_num_{from_page + 1}_to_{to_page + 1}.pdf")
