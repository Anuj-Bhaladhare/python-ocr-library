"""
2️⃣ Opening & Managing Documents in PyMuPDF (fitz)

This script demonstrates:

✔ Opening document using file path
✔ Opening document using bytes
✔ Opening document using stream
✔ Checking supported formats
✔ Reading metadata
✔ Handling encrypted PDFs
✔ Properly closing documents
"""

# --------------------------------------------------------------
# 1️⃣ Import Required Library
# --------------------------------------------------------------
import fitz  # PyMuPDF


# --------------------------------------------------------------
# 2️⃣ Define File Paths
# --------------------------------------------------------------
file_path = "./../pdf_data/orignal_bill_ifss.pdf"
output_path = "./../output_data/pdf_file/opening_management_document.pdf"


# --------------------------------------------------------------
# 3️⃣ Open PDF from File Path
# --------------------------------------------------------------
# fitz.open() automatically detects file type
doc = fitz.open(file_path)

print("Document Opened Successfully!")
print("Total Pages:", doc.page_count)
print("File Format:", doc.name)


# --------------------------------------------------------------
# 4️⃣ Check Supported Formats
# --------------------------------------------------------------
"""
PyMuPDF supports:

- PDF
- XPS
- EPUB
- CBZ (Comic book ZIP)
- Image formats (PNG, JPG, TIFF, etc.)

fitz.open() automatically detects type.
"""

print("Document is PDF:", doc.is_pdf)


# --------------------------------------------------------------
# 5️⃣ Check Metadata
# --------------------------------------------------------------
"""
Metadata contains information like:
- Author
- Title
- Creator
- Creation date
- Producer
"""

metadata = doc.metadata

print("\n--- Document Metadata ---")
for key, value in metadata.items():
    print(f"{key}: {value}")


# --------------------------------------------------------------
# 6️⃣ Handling Encrypted PDFs
# --------------------------------------------------------------
"""
If a PDF is password protected,
doc.is_encrypted will return True.
"""

if doc.is_encrypted:
    print("\nDocument is encrypted!")

    # Try to authenticate with password
    password = "your_password_here"

    if doc.authenticate(password):
        print("Password Correct! Document Unlocked.")
    else:
        print("Incorrect Password! Cannot access document.")
else:
    print("\nDocument is NOT encrypted.")


# --------------------------------------------------------------
# 7️⃣ Open PDF from Bytes
# --------------------------------------------------------------
"""
Useful when:
- PDF comes from API
- Database storage
- Network stream
"""

with open(file_path, "rb") as f:
    pdf_bytes = f.read()

doc_from_bytes = fitz.open(stream=pdf_bytes, filetype="pdf")

print("\nOpened document from bytes.")
print("Pages (bytes):", doc_from_bytes.page_count)


# --------------------------------------------------------------
# 8️⃣ Open PDF from Stream (Binary File Object)
# --------------------------------------------------------------
"""
Alternative method:
"""

with open(file_path, "rb") as f:
    doc_from_stream = fitz.open(stream=f.read(), filetype="pdf")

print("Opened document from stream.")


# --------------------------------------------------------------
# 9️⃣ Save a Copy (Optional Example)
# --------------------------------------------------------------
doc.save(output_path)
print("\nSaved copy to:", output_path)


# --------------------------------------------------------------
# 🔟 Properly Close Documents (VERY IMPORTANT)
# --------------------------------------------------------------
"""
Always close documents to:
✔ Free memory
✔ Avoid file locks
✔ Production safety
"""

doc.close()
doc_from_bytes.close()
doc_from_stream.close()

print("\nAll documents closed properly.")
