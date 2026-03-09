"""
    ================================================================
    BLOCK-LEVEL TEXT EXTRACTION + BOUNDING BOX DRAWING ON BLOCK
    ================================================================

    This script demonstrates:

    1. Extracting full Block text from a PDF
    2. Storing Block text and bounding boxes in structured format
    3. Drawing rectangles around each text line
    4. Saving the modified PDF properly

"""

import os
import fitz  # PyMuPDF


# ==============================================================
# CONFIGURATION
# ==============================================================

INPUT_PDF = "./input/ifss_orignal_bill.pdf"
OUTPUT_PDF = "./output/block_level_bonding_bbox.pdf"


# ==============================================================
# FUNCTION: Extract Line Data
# ==============================================================

def extract_line_data(page):
    """
    Extract all text lines with their bounding boxes.

    Returns:
        List of dictionaries:
        [
            {
                "text": "Full line text",
                "bbox": (x0, y0, x1, y1)
            }
        ]
    """

    line_text_blocks = []

    # Extract structured text dictionary
    text_data = page.get_text("dict")

    for block in text_data["blocks"]:

        # Process only text blocks
        if block["type"] == 0:

            for line in block["lines"]:

                # Extract full line text by combining spans
                line_text = ""
                for span in line["spans"]:
                    line_text += span["text"]

                # Extract bounding box
                x0, y0, x1, y1 = line["bbox"]

                # Store structured data
                line_text_blocks.append({
                    "text": line_text.strip(),
                    "bbox": (x0, y0, x1, y1)
                })

    return line_text_blocks



# ==============================================================
# FUNCTION: Extract Value by Using Key
# ==============================================================

# Find VALUE from list of array by using the KEY
def find_value_from_lines(line_data, search_key):

    for line in line_data:
        text = line["text"]

        if search_key.lower() in text.lower():
            parts = text.split(":", 1)

            if len(parts) > 1:
                return parts[1].strip()

    return None

# Find VALUE from list of array by using the KEY | Advance KEY and VALUE Extractor
def smart_key_value_extractor(line_data, search_key):
    """
    Try multiple extraction strategies:
    1. Same-line colon split
    2. Same-row neighbor
    3. Below-row neighbor
    """

    # Step 1: Find key line
    for line in line_data:
        if search_key.lower() in line["text"].lower():

            key_line = line
            key_text = line["text"]

            # --------------- Case 1: Colon Based ---------------
            if ":" in key_text:
                return key_text.split(":", 1)[1].strip()

            # --------------- Case 2 & 3: Layout Based ---------------
            key_x0, key_y0, key_x1, key_y1 = key_line["bbox"]

            for candidate in line_data:
                cx0, cy0, cx1, cy1 = candidate["bbox"]

                # Same row (horizontal)
                if abs(cy0 - key_y0) < 5 and cx0 > key_x1:
                    return candidate["text"]

                # Below row (vertical)
                if 0 < (cy0 - key_y1) < 20:
                    return candidate["text"]

    return None

# Find VALUE, KEY Bonding Box, VALUE Bonding Box by Using PAGE and KEY data
def get_key_value_bbox(page, search_key):
    """
    Returns:
        {
            "key_bbox": (x0, y0, x1, y1),
            "value_bbox": (x0, y0, x1, y1),
            "value_text": "31-01-2026"
        }
    """

    words = page.get_text("words")

    # Group words by (block_no, line_no)
    lines = {}

    for w in words:
        x0, y0, x1, y1, text, block_no, line_no, word_no = w
        key = (block_no, line_no)

        if key not in lines:
            lines[key] = []

        lines[key].append(w)

    # Process each line
    for line_words in lines.values():

        # Sort words left to right
        line_words.sort(key=lambda w: w[0])

        full_line = " ".join([w[4] for w in line_words])

        if search_key.lower() in full_line.lower():

            key_words = []
            value_words = []
            colon_found = False

            for w in line_words:
                if ":" in w[4]:
                    colon_found = True
                    key_words.append(w)
                elif not colon_found:
                    key_words.append(w)
                else:
                    value_words.append(w)

            # Combine bbox function
            def combine_bbox(word_list):
                x0 = min(w[0] for w in word_list)
                y0 = min(w[1] for w in word_list)
                x1 = max(w[2] for w in word_list)
                y1 = max(w[3] for w in word_list)
                return (x0, y0, x1, y1)

            key_bbox = combine_bbox(key_words)
            value_bbox = combine_bbox(value_words)

            value_text = " ".join([w[4] for w in value_words])

            return {
                "key_bbox": key_bbox,
                "value_bbox": value_bbox,
                "value_text": value_text
            }

    return None



# ==============================================================
# FUNCTION: Draw Bounding Boxes
# ==============================================================

def draw_line_boxes(page, line_data):
    """
    Draw rectangles around extracted lines.
    """

    key_x0, key_y0, key_x1, key_y1 = line_data["key_bbox"]
    key_rect = fitz.Rect(key_x0, key_y0, key_x1 - 2.5, key_y1)
    page.draw_rect(
        key_rect,
        color=(1, 0, 0),  # RED color (RGB normalized)
        width=0.5
    )

    value_x0, value_y0, value_x1, value_y1 = line_data["value_bbox"]
    value_rect = fitz.Rect(value_x0, value_y0, value_x1, value_y1)
    page.draw_rect(
        value_rect,
        color=(0, 1, 0),  # Green color (RGB normalized)
        width=0.5
    )


# ==============================================================
# MAIN EXECUTION
# ==============================================================

def main(search_key):

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PDF), exist_ok=True)

    # Open document safely
    with fitz.open(INPUT_PDF) as doc:

        # Process only first page
        page = doc[0]

        # Step 1: Extract line data
        line_data = extract_line_data(page)

        # find_value_from = smart_key_value_extractor(line_data, search_key)
        # print(f"{search_key} = {find_value_from}")

        find_value_from = get_key_value_bbox(page, search_key)
        print(f"{search_key} = {find_value_from}")

        # Step 2: Draw bounding boxes
        draw_line_boxes(page, find_value_from)

        # Step 3: Save modified PDF
        doc.save(
            OUTPUT_PDF,
            garbage=4,
            deflate=True
        )

    print("Bounding boxes added successfully!")


if __name__ == "__main__":

    # Add Your KEY to find VALUE
    search_key = "Supplier MSME Udyam No"

    main(search_key)

