"""
BLOCK LEVEL DRAWING IN PDF
---------------------------
Draw bounding boxes around cleaned text blocks
and save annotated PDF.
"""

import fitz
from typing import List, Tuple


# ==========================================================
# CONFIGURATION
# ==========================================================

INPUT_PDF = "./pdf_data/orignal_bill_ifss.pdf"
OUTPUT_PDF = "./output_data/pdf_file/block_level_output.pdf"

MIN_TEXT_LENGTH = 3


# ==========================================================
# TYPE DEFINITION
# ==========================================================

Block = Tuple[float, float, float, float, str, int, int]


# ==========================================================
# STEP 1 — Extract Text Blocks
# ==========================================================

def extract_text_blocks(page) -> List[Block]:
    blocks = page.get_text("blocks")
    return [b for b in blocks if b[6] == 0]  # Only text blocks


# ==========================================================
# STEP 2 — Filter Empty Blocks
# ==========================================================

def filter_blocks(blocks: List[Block]) -> List[Block]:
    clean = []
    for b in blocks:
        if len(b[4].strip()) >= MIN_TEXT_LENGTH:
            clean.append(b)
    return clean


# ==========================================================
# STEP 3 — Sort Blocks
# ==========================================================

def sort_blocks(blocks: List[Block]) -> List[Block]:
    return sorted(blocks, key=lambda b: (b[1], b[0]))


# ==========================================================
# STEP 4 — Draw Blocks on PDF
# ==========================================================

def draw_blocks(page, blocks: List[Block]):
    """
    Draw rectangle for each block
    """
    for block in blocks:
        x0, y0, x1, y1, text, _, _ = block

        rect = fitz.Rect(x0, y0, x1, y1)

        # Draw rectangle (red border)
        page.draw_rect(
            rect,
            color=(1, 0, 0),      # Red (RGB: 0-1 scale)
            width=1.5
        )


# ==========================================================
# MAIN PIPELINE
# ==========================================================

def process_and_draw(input_pdf: str, output_pdf: str):

    doc = fitz.open(input_pdf)

    for page in doc:

        # Extract
        blocks = extract_text_blocks(page)

        # Clean
        blocks = filter_blocks(blocks)

        # Sort
        blocks = sort_blocks(blocks)

        # Draw
        draw_blocks(page, blocks)

    # Save annotated file
    doc.save(output_pdf)
    doc.close()


# ==========================================================
# EXECUTION
# ==========================================================

if __name__ == "__main__":

    process_and_draw(INPUT_PDF, OUTPUT_PDF)

    print("\n✅ Block-level drawing completed.")
    print(f"📄 Output saved to: {OUTPUT_PDF}")








































































































































































# """
# PHASE 3 — Layout Engineering (Advanced Extraction)
# --------------------------------------------------
# Goal:
#     Clean invoice layout using block-level engineering.

# Steps:
#     1. Extract text blocks
#     2. Filter empty blocks
#     3. Sort blocks
#     4. Merge nearby blocks
#     5. Remove header/footer
# """

# import fitz
# from typing import List, Tuple


# # ==========================================================
# # CONFIGURATION
# # ==========================================================

# PDF_FILE_PATH = "./pdf_data/orignal_bill_ifss.pdf"

# MIN_TEXT_LENGTH = 3          # Remove tiny text junk
# MERGE_VERTICAL_THRESHOLD = 15  # Pixel gap for merging
# HEADER_PERCENTAGE = 0.08     # Remove top 8%
# FOOTER_PERCENTAGE = 0.92     # Remove bottom 8%


# # ==========================================================
# # TYPE DEFINITION
# # ==========================================================

# Block = Tuple[float, float, float, float, str, int, int]


# # ==========================================================
# # STEP 1 — Extract Major Text Blocks
# # ==========================================================

# def extract_major_blocks(page) -> List[Block]:
#     """
#     Extract only text blocks (block_type == 0)
#     """
#     blocks = page.get_text("blocks")
#     return [b for b in blocks if b[6] == 0]


# # ==========================================================
# # STEP 2 — Filter Empty / Junk Blocks
# # ==========================================================

# def filter_empty_blocks(blocks: List[Block]) -> List[Block]:
#     """
#     Remove blocks with empty or very small text
#     """
#     clean_blocks = []

#     for b in blocks:
#         text = b[4].strip()
#         if len(text) >= MIN_TEXT_LENGTH:
#             clean_blocks.append(b)

#     return clean_blocks


# # ==========================================================
# # STEP 3 — Sort Blocks by Reading Order
# # ==========================================================

# def sort_blocks(blocks: List[Block]) -> List[Block]:
#     """
#     Sort blocks top-to-bottom, then left-to-right
#     """
#     return sorted(blocks, key=lambda b: (b[1], b[0]))


# # ==========================================================
# # ============== STEP 4 — Merge Nearby Blocks ==============
# # ==========================================================

# def merge_nearby_blocks(blocks: List[Block]) -> List[Block]:
#     """
#     Merge vertically close blocks to form logical sections
#     """
#     if not blocks:
#         return []

#     merged = []
#     current = list(blocks[0])

#     for b in blocks[1:]:
#         prev_y1 = current[3]
#         curr_y0 = b[1]

#         vertical_gap = curr_y0 - prev_y1

#         # If blocks are close vertically → merge
#         if vertical_gap <= MERGE_VERTICAL_THRESHOLD:
#             current[4] += " " + b[4]
#             current[3] = b[3]  # extend bottom
#         else:
#             merged.append(tuple(current))
#             current = list(b)

#     merged.append(tuple(current))

#     return merged


# # ==========================================================
# # STEP 5 — Remove Header and Footer
# # ==========================================================

# def remove_header_footer(blocks: List[Block], page_height: float) -> List[Block]:
#     """
#     Remove blocks located in header and footer regions
#     """
#     final_blocks = []

#     for b in blocks:
#         y0 = b[1]
#         y1 = b[3]

#         if y0 > page_height * HEADER_PERCENTAGE and y1 < page_height * FOOTER_PERCENTAGE:
#             final_blocks.append(b)

#     return final_blocks


# # ==========================================================
# # MAIN PIPELINE
# # ==========================================================

# def process_invoice_layout(pdf_path: str):
#     """
#     Complete layout cleaning pipeline
#     """

#     # Open PDF
#     doc = fitz.open(pdf_path)
#     page = doc[0]

#     # 1️⃣ Extract
#     major_blocks = extract_major_blocks(page)

#     # 2️⃣ Filter
#     clean_blocks = filter_empty_blocks(major_blocks)

#     # 3️⃣ Sort
#     sorted_blocks = sort_blocks(clean_blocks)

#     # 4️⃣ Merge
#     merged_blocks = merge_nearby_blocks(sorted_blocks)

#     # 5️⃣ Remove header/footer
#     final_blocks = remove_header_footer(
#         merged_blocks,
#         page.rect.height
#     )

#     return final_blocks


# # ==========================================================
# # EXECUTION
# # ==========================================================

# if __name__ == "__main__":

#     final_layout = process_invoice_layout(PDF_FILE_PATH)

#     print("\n ====== CLEANED INVOICE BLOCKS ====== \n")

#     for i, block in enumerate(final_layout):
#         x0, y0, x1, y1, text, _, _ = block
#         print(f"\nBlock {i+1}")
#         print(f"Bounding Box: ({x0:.2f}, {y0:.2f}, {x1:.2f}, {y1:.2f})")
#         print("Text:")
#         print(text.strip())
#         print("-" * 50)
