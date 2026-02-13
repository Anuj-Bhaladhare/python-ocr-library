from docx import Document

# Create document
document = Document()

# Get all sections
sections = document.sections

# Total number of sections
print("Total sections:", len(sections))

# Loop through sections and print start type
for i, section in enumerate(sections, start=1):
    print(f"Section {i} start type:", section.start_type)
