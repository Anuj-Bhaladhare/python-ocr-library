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
