"""
================================================================
SPLITTING A PDF INTO TWO PARTS USING PyMuPDF (fitz)
================================================================

This script demonstrates:

1. Opening a PDF safely
2. Validating page count
3. Splitting the PDF into two parts:
      Part 1 -> Pages 1 to 45
      Part 2 -> Pages 46 to End
4. Saving both parts separately
5. Proper resource management (closing documents)

Author: ANUJ
"""

import os
import fitz  # PyMuPDF


# ==============================================================
# CONFIGURATION
# ==============================================================

INPUT_PDF = "./../pdf_data/ansible-for-devops.pdf"
OUTPUT_DIR = "./output"
SPLIT_AT_PAGE = 45   # Human readable page number (1-based)


# ==============================================================
# UTILITY FUNCTION
# ==============================================================

def split_pdf_into_two(input_path: str, output_dir: str, split_page: int):
    """
    Split a PDF into two parts.

    Parameters:
        input_path (str): Path to input PDF
        output_dir (str): Directory to save output files
        split_page (int): Page number where split occurs (1-based index)

    Output:
        - part_1.pdf (Page 1 to split_page)
        - part_2.pdf (split_page+1 to end)
    """

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Open input PDF safely
    with fitz.open(input_path) as pdf:

        page_count = pdf.page_count
        print(f"Total Pages: {page_count}")

        # -------------------------------
        # Validation
        # -------------------------------
        if split_page >= page_count:
            raise ValueError("Split page must be less than total page count.")

        # Convert to 0-based index
        split_index = split_page - 1

        # -------------------------------
        # Create first part (1 → split_page)
        # -------------------------------
        part1 = fitz.open()
        part1.insert_pdf(
            pdf,
            from_page=0,
            to_page=split_index
        )

        part1_path = os.path.join(output_dir, "splitted_pdf_1_to_45.pdf")
        part1.save(part1_path)
        part1.close()

        print(f"Saved: {part1_path}")

        # -------------------------------
        # Create second part (split_page+1 → end)
        # -------------------------------
        part2 = fitz.open()
        part2.insert_pdf(
            pdf,
            from_page=split_index + 1,
            to_page=page_count - 1
        )

        part2_path = os.path.join(output_dir, "splitted_pdf_46_to_end.pdf")
        part2.save(part2_path)
        part2.close()

        print(f"Saved: {part2_path}")


# ==============================================================
# MAIN EXECUTION
# ==============================================================

if __name__ == "__main__":
    split_pdf_into_two(
        input_path=INPUT_PDF,
        output_dir=OUTPUT_DIR,
        split_page=SPLIT_AT_PAGE
    )

