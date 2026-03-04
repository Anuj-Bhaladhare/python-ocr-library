"""
    => Everything about Drawing Bounding Boxes in PDF using PyMuPDF

    => 1️⃣ What is a Bounding Box in PDF?
        - A bounding box is simply a rectangle defined by 4 coordinates:
            * (x0, y0)  → Top-left corner  
            * (x1, y1)  → Bottom-right corner
        - It represents the area occupied by:
            * A block
            * A line
            * A word
            * An image
            * Any object
"""

# Import Library 
import fitz     # PyMuPDF
import os       # Operating System

pdf_path = "./pdf_data/orignal_bill_ifss.pdf"
# pdf_path = "./pdf_data/invoice.pdf"


# # ===================================================
# # ===================> Example 1 <===================
# # ===================================================
# # open the PDF
# doc = fitz.open(pdf_path)
# # Select the page (e. g. first page)
# page = doc[0]
# # Create rectangle
# rect = fitz.Rect(20, 50, 100, 300)
# # Drow rectengle on page
# page.draw_rect(
#     rect,
#     color = (1, 0, 0),   # Red border
#     # width = 2  
#     fill=(1, 1, 0),
#     fill_opacity=0.3
# )
# # Save the new PDF
# doc.save("./output_data/pdf_file/bounding_box.pdf")
# # Closed Document
# doc.close()






# ===================================================
# ===================> Example 2 <===================
# ===================================================
"""
    => Drawing Words Instead of Blocks
        - Open a PDF file
        - Read text from it
        - Get the position (coordinates) of each word
        - Draw a rectangle (bounding box) around each word
        - Save a new PDF with those boxes drawn
"""

# open the PDF
doc = fitz.open(pdf_path)

# Select the page (e. g. first page)
page = doc[0]

# --------------> Draw rectangle around each word <--------------
# Extract words with coordinates
words = page.get_text("words")

# Create New Object of word and bonding box
word_object = []
for word in words:
    x0, y0, x1, y1 = word[:4]

    word_object.append({
        "text": word[4],
        "bbox": [x0, y0, x1, y1]
    })

# Create Bounding Box for Specific Word
word_input_for_box = input(
    "Enter Your Word to Create Bounding Box (if available in PDF): \n"
)

word_flag = False

for w_obj in word_object:
    if w_obj["text"] == word_input_for_box:
        w_x0, w_y0, w_x1, w_y1 = w_obj["bbox"]

        rect = fitz.Rect(w_x0, w_y0, w_x1, w_y1)

        page.draw_rect(
            rect, 
            color=(0, 1, 0), 
            width=0.5   # Green Box
        )
        word_flag = True


# Print only once after loop
if word_flag == True:
    print("Bonding Box Created Successfully...!")
else:
    print("Your Word NOT Found...!")


# Save the new PDF
doc.save("./output_data/pdf_file/world_level_bounding_box.pdf")


# # --------------> Draw rectangle around Text Blocks <--------------
# # Extract Text Blocks with coordinates
# text_blocks = page.get_text("blocks")

# for blocks in text_blocks:
#     x0, y0, x1, y1 = blocks[:4]
#     # print(f"=============== \n x0 = {x0}, \n y0 = {y0}, \n x1 = {x1}, \n y1 = {y1} \n =============== ")
#     rect = fitz.Rect(x0, y0, x1, y1)
#     page.draw_rect(
#         rect, 
#         color=(0, 1, 0), 
#         width=0.5   # Green Box
#     )
# # Save the new PDF
# doc.save("./output_data/pdf_file/blocks_level_bounding_box.pdf")


# # --------------> Draw rectangle around each Dictionary Structure [key : value] <--------------
# # Extract Dictionary is a data structure that stores [key : value] with coordinates
# dictionary = page.get_text("dict")

# # Loop through blocks
# for block in dictionary["blocks"]:
    
#     # Only text blocks (type 0 = text, type 1 = image)
#     if block["type"] == 0:
        
#         x0, y0, x1, y1 = block["bbox"]
#         rect = fitz.Rect(x0, y0, x1, y1)
        
#         page.draw_rect(
#             rect,
#             color=(0, 1, 0),  # Green
#             width=0.5
#         )
    
# # Save the new PDF
# doc.save("./output_data/pdf_file/dictionary_level_bounding_box.pdf")



# --------------> Draw rectangle around Text Line <--------------
# Extract Line Blocks with coordinates
text_blocks = page.get_text("dict")

for block in text_blocks["blocks"]:
    if block["type"] == 0:
        for line in block["lines"]:
            x0, y0, x1, y1 = line["bbox"]
            # print(line["bbox"])
            # print(f"=============== \n x0 = {x0}, \n y0 = {y0}, \n x1 = {x1}, \n y1 = {y1} \n =============== ")
            rect = fitz.Rect(x0, y0, x1, y1)
            page.draw_rect(
                rect, 
                color=(0, 1, 0), 
                width=0.5   # Green Box
            )
        # Save the new PDF
        doc.save("./output_data/pdf_file/line_level_bounding_box.pdf")


# Closed Document
doc.close()

print("Bonding boxex added successfully!")

