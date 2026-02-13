# Reading pdf metadata
# get total number of pdf page
# get table of contents

import fitz

# print the version of PyMuPDF
print(f" \n Version of PyMuPDF:===>\n {fitz.__doc__} \n ")

# Open the PDF file here
# pdf = fitz.open("./pdf_data/ansible-for-devops.pdf")
pdf = fitz.open("./pdf_data/Unit-14.pdf") 

# Get Page  Number of PDF
print(f"\n Page Number of PDF file: '{pdf.page_count}' \n")

# Get MetaData of PDF file
print(f"\n Meta-Data of PDF file:===>\n {pdf.metadata} \n")

# Get Author Name of PDF file
print(f"\n Author Name of PDF file: '{pdf.metadata['author']}' \n")

# Get First 10 Element of List
print(f"\n First 10 Element of List from PDF file:===> \n {pdf.get_toc()[:10]} \n")

# Close the PDF File
pdf.close()
