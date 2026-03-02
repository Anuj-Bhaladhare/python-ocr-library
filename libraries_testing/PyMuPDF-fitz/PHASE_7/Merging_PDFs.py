"""
================================================================
MERGING TWO PDFs USING PyMuPDF (fitz)
================================================================

This script demonstrates:

1. Opening multiple PDFs safely
2. Merging second PDF into first PDF
3. Saving merged output properly
4. Handling resources correctly
5. Basic validation

Author: ANUJ
"""

import os
import fitz  # PyMuPDF


# ==============================================================
# CONFIGURATION
# ==============================================================

PDF_PART_1 = "./output/splitted_pdf_1_to_45.pdf"
PDF_PART_2 = "./output/splitted_pdf_46_to_end.pdf"
OUTPUT_PATH = "./output/NEW_merged_pdf.pdf"


# ==============================================================
# UTILITY FUNCTION
# ==============================================================

def merge_two_pdfs(pdf_path_1: str, pdf_path_2: str, output_path: str):
    """
    Merge two PDF files into a single PDF.

    Parameters:
        pdf_path_1 (str): First PDF (base document)
        pdf_path_2 (str): Second PDF (to be appended)
        output_path (str): Output merged PDF path
    """

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Open both PDFs safely
    with fitz.open(pdf_path_1) as base_pdf, \
         fitz.open(pdf_path_2) as append_pdf:

        # Validate that second PDF has pages
        if append_pdf.page_count == 0:
            raise ValueError("Second PDF has no pages to merge.")

        print(f"Base PDF pages: {base_pdf.page_count}")
        print(f"Append PDF pages: {append_pdf.page_count}")

        # ------------------------------------------------------
        # Insert all pages of second PDF into first PDF
        # ------------------------------------------------------
        base_pdf.insert_pdf(
            append_pdf,
            from_page=0,
            to_page=append_pdf.page_count - 1
        )

        # ------------------------------------------------------
        # Save merged PDF
        # IMPORTANT: Save to new file (not same input file)
        # ------------------------------------------------------
        base_pdf.save(
            output_path,
            garbage=4,     # Clean unused objects
            deflate=True   # Compress streams
        )

        print(f"Merged PDF saved at: {output_path}")


# ==============================================================
# MAIN EXECUTION
# ==============================================================

if __name__ == "__main__":
    merge_two_pdfs(
        pdf_path_1=PDF_PART_1,
        pdf_path_2=PDF_PART_2,
        output_path=OUTPUT_PATH
    )
