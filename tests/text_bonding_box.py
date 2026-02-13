import cv2
import pytesseract
from pytesseract import Output


if __name__ == "__main__":

    # Read Image
    image = cv2.imread("./../data/book_image/clear_book_page.png")

    # STEP 1: Convert to Grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # STEP 2: Noise Removal (Choose ONE, not all)
    blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # STEP 3: Thresholding
    thresh_image = cv2.threshold(
        blur_image, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    # STEP 4: OCR WITH WORD-LEVEL DATA
    ocr_data = pytesseract.image_to_data(
        thresh_image,
        output_type=Output.DICT,
        config="--oem 3 --psm 6"
    )

    # STEP 5: DRAW BOUNDING BOX ON EACH WORD
    n_boxes = len(ocr_data["text"])

    for i in range(n_boxes):
        text = ocr_data["text"][i]
        conf = int(ocr_data["conf"][i])

        # Filter weak OCR results (industry practice)
        if conf > 60 and text.strip() != "":
            x = ocr_data["left"][i]
            y = ocr_data["top"][i]
            w = ocr_data["width"][i]
            h = ocr_data["height"][i]

            # Draw bounding box
            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # Optional: draw word text
            cv2.putText(
                image,
                text,
                (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1
            )

    # STEP 6: SAVE OUTPUT
    cv2.imwrite("./../data/outputs/word_level_bounding_boxes.png", image)
