"""
    => Block-Level Engineering
        - Extract major blocks only
        - Filter empty blocks
        - Sort blocks by position
        - Merge nearby blocks
        - Remove headers/footers

        👉 Practice: Clean invoice layout.

    ======================================================
    🧠 Engineering Strategy
        Step 1 → Extract raw blocks
        Step 2 → Keep only text blocks
        Step 3 → Remove empty blocks
        Step 4 → Remove header/footer (based on Y threshold)
        Step 5 → Sort by (y, x)
        Step 6 → Merge vertically close blocks
        Step 7 → Visualize cleaned layout
    ======================================================
"""
import fitz


# ------------------------------------------------------------
# 1️⃣ Import Library
# ------------------------------------------------------------
import fitz
import os



# ------------------------------------------------------------
# 2️⃣ Initialize File Paths
# ------------------------------------------------------------
file_path = "./../pdf_data/ansible-for-devops.pdf"
output_path = "./output/block-level-engineering.pdf"


# ------------------------------------------------------------
# 3️⃣ Open Document
# ------------------------------------------------------------
doc = fitz.open(file_path)
page = doc[18]      # First page for demo


page_height = page.rect.height
print("Page Height: ", page_height)



# ------------------------------------------------------------
# 4️⃣ Extract Raw Blocks
# ------------------------------------------------------------
raw_blocks = page.get_text("blocks")

text_blocks = []

for block in raw_blocks:
    x0, y0, x1, y1, text, block_no, block_type = block

    # Keep only TEXT blocks
    if block_type == 0:
        text_blocks.append({
            "bbox": fitz.Rect(x0, y0, x1, y1),
            "text": text.strip()
        })


print("Total Raw Text Blocks:", len(text_blocks))




# ------------------------------------------------------------
# 5️⃣ Filter Empty Blocks
# ------------------------------------------------------------
filtered_blocks = [
    b for b in text_blocks
    if b["text"] != ""
]

print("After Removing Empty Blocks: ", len(filtered_blocks))




# ------------------------------------------------------------
# 6️⃣ Remove Header & Footer
# ------------------------------------------------------------
"""
Simple heuristic:
Remove blocks within top 5% and bottom 5% of page 
"""

header_limit = page_height * 0.05
footer_limit = page_height * 0.95

clean_blocks = []

for block in filtered_blocks:
    y0 = block["bbox"].y0
    y1 = block["bbox"].y1

    if y0 > header_limit and y1 < footer_limit:
        clean_blocks.append(block)

print("After Removing Header/Footer:", len(clean_blocks))




# ------------------------------------------------------------------
# 7️⃣ Sort Blocks by Reading Order (Top → Bottom, Left → Right)
# ------------------------------------------------------------------
clean_blocks.sort(key = lambda b: (b["bbox"].y0, b["bbox"].x0))

print("Block Sorted by Position.")




# ------------------------------------------------------------
# 8️⃣ Merge Nearby Blocks (Vertical Distance Based)
# ------------------------------------------------------------
"""
If vertical gap between two blocks is small,
merge them into one large block.
"""

merged_blocks = []
vertical_threshold = 10  # Adjust based on layout

for block in clean_blocks:
    if not merged_blocks:
        merged_blocks.append(block)
        continue

    last_block = merged_blocks[-1]

    vertical_gap = block["bbox"].y0 - last_block["bbox"].y1

    if vertical_gap < vertical_threshold:
        # Merge rectangles
        new_rect = last_block["bbox"] | block["bbox"]

        merged_blocks[-1] = {
            "bbox": new_rect,
            "text": last_block["text"] + " " + block["text"]
        }
    else:
        merged_blocks.append(block)

print("After Merging Nearby Blocks:", len(merged_blocks))




# ------------------------------------------------------------
# 9️⃣ Draw Final Cleaned Blocks
# ------------------------------------------------------------
for block in merged_blocks:
    page.draw_rect(block["bbox"], color=(1, 0, 0), width=1.5)




# ------------------------------------------------------------
# 🔟 Save Cleaned Layout PDF
# ------------------------------------------------------------
doc.save(output_path)
doc.close()



print("\nClean Layout PDF Saved At:", output_path)
print("Block-Level Engineering Completed Successfully.")

