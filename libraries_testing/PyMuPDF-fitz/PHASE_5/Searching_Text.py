"""
    => Searching Text
        - page.search_for()
        - Case sensitivity
        - Partial matches
        
    👉 Practice: Highlight all "Total" words.
"""

import fitz

# -------> 2. Initialize File Path <------------------
file_path = "./../pdf_data/ansible-for-devops.pdf"
output_path = "./output/Searching_Text.pdf"


# -------> 3. Open PDF File Document <-----------------
doc = fitz.open(file_path)
page = doc[23]
    
keyword = "Ansible"
matches = page.search_for(keyword)

for rect in matches:
    highlight = page.add_highlight_annot(rect)
    highlight.update()

doc.save(output_path)

print(f"✅ All '{keyword}' words highlighted.")

