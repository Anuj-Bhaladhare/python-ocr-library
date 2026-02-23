"""
    => Annotations
        - Add highlight
        - Add underline
        - Add text annotation
        - Remove annotation

    👉 Practice: Create automated review system.
"""



# -------> 1. Import Required Libraries <-----------------
import os
import re
import fitz
import numpy as np 

# -------> 2. Initialize File Path <------------------
file_path = "./../pdf_data/ansible-for-devops.pdf"
output_path = "./output/font-level-engineering.pdf"


# -------> 3. Open PDF File Document <-----------------
doc = fitz.open(file_path)
page = doc[23]



# # ===================================================================
# # HIGHLIGHT KEYWORD IN PDF
# # ===================================================================

# # -------> 4. Find word and add Hightlight <--------------
# text_for_highlight = []
# text_instances = ["understand", "software", "ANUJ", "lighter", "development and provides"]

# for text in text_instances:
#     find_text_on_pdf = page.search_for(text)
    
#     if len(find_text_on_pdf) != 0:
#         text_for_highlight.append(find_text_on_pdf)
#     else:
#         print(f"\n{text} is NOT Available on Document\n")


# for inst in text_for_highlight:
#     highlight = page.add_highlight_annot(inst)


# # -------> 5. Find word and add Hightlight <--------------
# doc.save("./output/invoice_highlighted.pdf")
# doc.close()

# print("✅ Highlight added and saved.")







# # ===================================================================
# # UNDERLINE KEYWORD IN PDF
# # ===================================================================
# # -------> 4. Find word and add Underline <--------------
# text_for_underline = []
# text_instances = ["understand", "software", "ANUJ", "lighter", "development and provides"]

# for text in text_instances:
#     find_text_on_pdf = page.search_for(text)

#     if len(find_text_on_pdf) != 0:
#         text_for_underline.append(find_text_on_pdf)
#     else:
#         print(f"\n{text} is NOT Available on Document\n")

# for match in text_for_underline:
#     page.add_underline_annot(match)


# # -------> 5. Find word and add Hightlight <--------------
# doc.save("./output/invoice_underlining.pdf")
# doc.close()

# print("✅ Highlight added and saved.")
















# # # ==============================================================
# # # ADD TEXT COMMENT
# # # ==============================================================

# def Extract_Structured_Layout(page):

#     layout = page.get_text("dict")

#     all_font_sizes = []

#     # Collect all font sizes for threshold calculation
#     for block in layout["blocks"]:
#         if block["type"] != 0:
#             continue

#         for line in block["lines"]:
#             for span in line["spans"]:
#                 all_font_sizes.append(span["size"])

#     # Determine heading threshold (bigger than average)
#     average_font_size = sum(all_font_sizes) / len(all_font_sizes)
#     heading_threshold = average_font_size + 2

#     return average_font_size, heading_threshold


# def Process_Spans_and_Detect_Headings(block, heading_threshold):

#     headings = []

#     for line in block["lines"]:
#         for span in line["spans"]:

#             text = span["text"].strip()
#             font_size = span["size"]
#             font_flags = span["flags"]
#             span_bbox = fitz.Rect(span["bbox"])

#             if not text:
#                 continue

#             is_bold = bool(font_flags & 16)

#             if font_size > heading_threshold or is_bold:
#                 headings.append((text, span_bbox))

#     return headings



# # Extract Structured Layout
# average_font_size, heading_threshold = Extract_Structured_Layout(page)




# # ==============================================================
# # SMART COMMENT LOGIC FOR "Complete"
# # ==============================================================

# keyword = "Complete"
# comment_text = f"📌 Review this section carefully.\nPlease verify context. - ANUJ \n || KeyWord = {keyword} ||"

# layout = page.get_text("dict")

# heading_matches = []
# normal_matches = []

# # Detect headings and classify keyword
# for block in layout["blocks"]:

#     if block["type"] != 0:
#         continue

#     headings = Process_Spans_and_Detect_Headings(block, heading_threshold)

#     # Check heading spans
#     for heading_text, heading_span_bbox in headings:
#         if keyword.lower() in heading_text.lower():
#             heading_matches.append(heading_span_bbox)

# # Find all occurrences of keyword (normal search)
# all_keyword_rects = page.search_for(keyword)

# # Separate heading rects from normal rects
# for rect in all_keyword_rects:
#     is_heading = False

#     for heading_bbox in heading_matches:
#         if rect.intersects(heading_bbox):
#             is_heading = True
#             break

#     if not is_heading:
#         normal_matches.append(rect)


# # ------------------------------------------------------------
# # APPLY RULES
# # ------------------------------------------------------------

# # CASE 1: If heading version exists → annotate only that
# if heading_matches:
#     for bbox in heading_matches:
#         point = fitz.Point(bbox.x1 + 5, bbox.y0)
#         page.add_text_annot(point, comment_text)

#     print("✅ Comment added to HEADING occurrence only.")

# # CASE 2: No heading match but only one occurrence → annotate it
# elif len(all_keyword_rects) == 1:
#     rect = all_keyword_rects[0]
#     point = fitz.Point(rect.x1 + 5, rect.y0)
#     page.add_text_annot(point, comment_text)

#     print("✅ Single occurrence found (not heading). Comment added.")

# # CASE 3: Multiple non-heading → do nothing
# else:
#     rect = all_keyword_rects[0]
#     point = fitz.Point(rect.x1 + 5, rect.y0)
#     page.add_text_annot(point, comment_text)

#     print(" Multiple non-heading occurrences found. Annotation added on First Keyword.")


# # ------------------------------------------------------------
# # Save
# # ------------------------------------------------------------
# doc.save("./output/text_comment_annotation.pdf")
# doc.close()

# print("🎯 Smart annotation completed.")



















# ==============================================================
# BLOCK LEVEL COMMENT AFTER LAST WORD OF HEADING BLOCK
# ==============================================================

def Extract_Structured_Layout(page):

    layout = page.get_text("dict")

    all_font_sizes = []

    # Collect all font sizes for threshold calculation
    for block in layout["blocks"]:
        if block["type"] != 0:
            continue

        for line in block["lines"]:
            for span in line["spans"]:
                all_font_sizes.append(span["size"])

    # Determine heading threshold (bigger than average)
    average_font_size = sum(all_font_sizes) / len(all_font_sizes)
    heading_threshold = average_font_size + 2

    return average_font_size, heading_threshold




def Process_Spans_and_Detect_Headings(block, heading_threshold):

    headings = []

    for line in block["lines"]:
        for span in line["spans"]:

            text = span["text"].strip()
            font_size = span["size"]
            font_flags = span["flags"]
            span_bbox = fitz.Rect(span["bbox"])

            if not text:
                continue

            is_bold = bool(font_flags & 16)

            if font_size > heading_threshold or is_bold:
                headings.append((text, span_bbox))

    return headings


# Extract Structured Layout
average_font_size, heading_threshold = Extract_Structured_Layout(page)

import re

target_number = "3."
target_keyword = "Complete"

comment_text = "📌 Please review this section carefully. - ANUJ"

layout = page.get_text("dict")

section_start_y = None
section_end_y = None

all_numbered_headings = []

# ------------------------------------------------------------
# Step 1: Find all numbered headings with Y positions
# ------------------------------------------------------------
for block in layout["blocks"]:
    if block["type"] != 0:
        continue

    for line in block["lines"]:

        line_text = ""
        line_bbox = None

        for span in line["spans"]:
            line_text += span["text"]
            line_bbox = fitz.Rect(span["bbox"])

        clean_text = line_text.strip()

        if re.match(r"^\d+\.", clean_text):
            all_numbered_headings.append((clean_text, line_bbox))


# ------------------------------------------------------------
# Step 2: Identify target section start & next section start
# ------------------------------------------------------------
for i, (text, bbox) in enumerate(all_numbered_headings):

    if text.startswith(target_number) and target_keyword in text:
        section_start_y = bbox.y0

        # Next heading defines end boundary
        if i + 1 < len(all_numbered_headings):
            section_end_y = all_numbered_headings[i + 1][1].y0
        else:
            section_end_y = page.rect.height  # till page end

        break


# ------------------------------------------------------------
# Step 3: Collect words only inside vertical boundaries
# ------------------------------------------------------------
if section_start_y is not None:

    words = page.get_text("words")

    section_words = [
        w for w in words
        if section_start_y <= w[1] < section_end_y
    ]

    section_words = sorted(section_words, key=lambda w: (w[1], w[0]))

    if section_words:
        last_word = section_words[-1]
        x0, y0, x1, y1 = last_word[:4]

        point = fitz.Point(x1 + 5, y0)
        page.add_text_annot(point, comment_text)

        print("✅ Comment added at END of section 3 correctly.")

    else:
        print("⚠ No words found in section.")

else:
    print("❌ Target section not found.")


# ------------------------------------------------------------
# Save
# ------------------------------------------------------------
doc.save("./output/block_level_annotation.pdf")
doc.close()

print("🎯 Block-level smart annotation completed.")
