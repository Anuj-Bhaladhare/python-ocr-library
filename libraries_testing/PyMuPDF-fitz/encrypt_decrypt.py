# Open password protected pdf files
# Decrypt pdf file
# Encrypt pdf file

import fitz


# ===================================================================
# ======================> Decryption PDF File <======================
# ===================================================================

# # Check if file is encrypted
# def is_encrypted(file_path):
#     pdf = fitz.open(file_path)
#     status = pdf.is_encrypted
#     pdf.close()
#     return status

# # file_path = fitz.open("./pdf_data/ansible-for-devops.pdf")
# file_path = fitz.open("./pdf_data/protected_doc.pdf") 


# # Check encryption status
# is_file_encrypted = is_encrypted(file_path)
# print(f"Encryption Status: {is_file_encrypted}")

# # Open the PDF
# pdf = fitz.open(file_path)
# # Open Encrypted PDF File || How to Remove Password from PDF File  
# if pdf.is_encrypted:
#     password = input("Enter PDF password: ")

#     if pdf.authenticate(password):
#         print("Correct password!\n")

#         page = pdf.load_page(5)  # first page (index 0)
#         print(page.get_text("text"))

#         # Save the Decrypted PDF file
#         pdf.save("./output_data/pdf_file/decrypted_pdf.pdf")

#     else:
#         print("Incorrect Password")
#         pdf.close()
#         exit()

# else:
#     print("PDF is not encrypted.")
#     page = pdf.load_page(0)
#     print(page.get_text("text"))

# pdf.close()












# ===================================================================
# ======================> Encryption PDF File <======================
# ===================================================================

def encrypt_pdf(input_path, password, output_path):
    # Open PDF
    pdf = fitz.open(input_path)

    # Permissions (allow selected actions)
    permissions = (
        fitz.PDF_PERM_ACCESSIBILITY |
        fitz.PDF_PERM_PRINT |
        fitz.PDF_PERM_COPY |
        fitz.PDF_PERM_ANNOTATE
    )

    # Save encrypted file
    pdf.save(
        output_path,
        encryption=fitz.PDF_ENCRYPT_AES_256,  # Strongest algorithm
        owner_pw=password,                    # Owner password
        user_pw=password,                     # User password
        permissions=permissions
    )

    pdf.close()
    print("PDF successfully encrypted!")


input_path = "./output_data/pdf_file/ben-10-image.pdf"
password = "ANUJ2000"
output_path = "./output_data/pdf_file/ben-10-encrypt.pdf"
# Call Encrypt Function for PDF Encryption
encrypt_pdf(input_path, password, output_path)
