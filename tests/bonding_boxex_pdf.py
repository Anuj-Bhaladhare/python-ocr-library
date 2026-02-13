import cv2, fitz, numpy as np
# import 

if __name__ == "__main__":

    # Open PDF
    pdf_file = fitz.open("./../data/raw/invoice.pdf")

    # Select a page (0 = first page)
    page_1 = pdf_file[0]

    # Create Rectangle: (x0, y0, x1, y1)
    rectangle = fitz.Rect(100, 200, 400, 350)

    # Draw Rectangle
    page_1.draw_rect(
        rect=rectangle,
        color=(0, 1, 0),
        width=2
    )

    # Save output
    pdf_file.save("./output.pdf")
    pdf_file.close()
