# Extract Text

# Imports Libraries
import fitz

# Open the PDF file here
# pdf = fitz.open("./pdf_data/ansible-for-devops.pdf")
pdf = fitz.open("./pdf_data/Unit-14.pdf") 

# Count PDF file page
page_counter = pdf.page_count

# # Get Text from All Pages
# for page_num in range(page_counter):
#     page_load = pdf.load_page(page_num)
#     page_text = page_load.get_text("text")

#     print(f"""\n ===== 'Page Number: {page_num + 1}' ===== \n {page_text} \n ========== \n""")


putput_file_path = "./output_data/txt_file"
for page_num in range(page_counter):
    # Load Page 
    page_load = pdf.load_page(page_num)
    # Get text from loaded page
    page_text = page_load.get_text("text")
    # Save text in txt file
    with open(f"{putput_file_path}/pdf_page_{page_num + 1}.txt", 'w') as file:
        file.write(page_text.replace('\t', ' '))


# Closed the PDF file
pdf.close()
