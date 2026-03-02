"""
================================================================
ROTATE FULL PDF USING PyMuPDF (fitz)
================================================================

This script demonstrates:

1. Opening a PDF safely
2. Rotating all pages by a given angle
3. Saving to a new file
4. Proper resource management
5. Validation of rotation angle

Author: ANUJ
"""

import os
import fitz  # PyMuPDF


# ==============================================================
# CONFIGURATION
# ==============================================================

INPUT_PDF = "./../pdf_data/ansible-for-devops.pdf"
OUTPUT_PDF = "./output/rotated_180_output.pdf"
ROTATION_ANGLE = 180  # Allowed: 0, 90, 180, 270


# ==============================================================
# UTILITY FUNCTION
# ==============================================================

def rotate_pdf(input_path: str, output_path: str, angle: int):
    """
    Rotate all pages of a PDF by a given angle.

    Parameters:
        input_path (str): Path to input PDF
        output_path (str): Path to save rotated PDF
        angle (int): Rotation angle (0, 90, 180, 270)

    Notes:
        PyMuPDF only supports rotation in multiples of 90 degrees.
    """

    # ----------------------------------------------------------
    # Validate rotation angle
    # ----------------------------------------------------------
    if angle not in (0, 90, 180, 270):
        raise ValueError("Rotation angle must be 0, 90, 180, or 270.")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # ----------------------------------------------------------
    # Open PDF safely
    # ----------------------------------------------------------
    with fitz.open(input_path) as pdf:

        page_count = pdf.page_count
        print(f"Total Pages: {page_count}")
        print(f"Applying rotation: {angle} degrees")

        # ------------------------------------------------------
        # Rotate each page individually
        # ------------------------------------------------------
        for page in pdf:
            page.set_rotation(angle)

        # ------------------------------------------------------
        # Save rotated PDF
        # ------------------------------------------------------
        pdf.save(
            output_path,
            garbage=4,     # Clean unused objects
            deflate=True   # Compress streams
        )

        print(f"Rotated PDF saved at: {output_path}")


# ==============================================================
# MAIN EXECUTION
# ==============================================================

if __name__ == "__main__":
    rotate_pdf(
        input_path=INPUT_PDF,
        output_path=OUTPUT_PDF,
        angle=ROTATION_ANGLE
    )

