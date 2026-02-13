# STEP-0: Folder & Imports (Foundation)
import cv2
import pytesseract
import numpy as np
from pytesseract import Output
from collections import defaultdict

"""
    ChatGPT Documentation Link: https://chatgpt.com/c/697db5af-90e8-8320-89be-37dad076968a
    STEP-> 1️⃣ Read text with OCR
    STEP-> 2️⃣ Draw bounding boxes on every word
    STEP-> 3️⃣ Detect lines & blocks
    STEP-> 4️⃣ Find “Total / Final Total”
    STEP-> 5️⃣ Extract key → value pairs
    STEP-> 6️⃣ Export clean JSON output
"""

if __name__ == "__main__":

    # --------------------------------------------------------------
    # STEP-1: Read the Invoice Image
    # --------------------------------------------------------------
    image = cv2.imread("./../file_data/new_sample_invoice.jpg")
    # image = cv2.imread("./file_data/scan_invoice.jpg")
    original = image.copy()


    # --------------------------------------------------------------
    # STEP-2: Preprocessing (OCR-Friendly Image)
    # --------------------------------------------------------------
    # Convert Image to Gray-Scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("./../outputs/gray_image.png", gray_image)
    
    # Add Blur Effect on that Image
    blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Convert Image to Binary Image
    _, thresh_image = cv2.threshold(
        gray_image,
        100,     # try 60, 80, 100
        255,
        cv2.THRESH_BINARY
    )
    cv2.imwrite("./../outputs/thresh_image.png", thresh_image)

    # Remove Noise From Image
    def noise_removal(gray_image):
        """
        OCR-safe noise removal:
        - Preserves text shape, thickness, and spacing
        - Removes only background noise and tiny speckles
        """

        # 1️⃣ Edge-preserving denoising (SAFE for text)
        denoised = cv2.fastNlMeansDenoising(
            gray_image,
            None,
            h=10,                  # noise strength (8–12 safe)
            templateWindowSize=7,
            searchWindowSize=21
        )

        # 2️⃣ Light adaptive threshold (text-safe)
        binary = cv2.adaptiveThreshold(
            denoised,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            10
        )

        # 3️⃣ Remove only tiny isolated noise (no text damage)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
            binary,
            connectivity=8
        )

        clean = np.zeros(binary.shape, dtype=np.uint8)

        MIN_AREA = 30  # keeps characters, removes dots/noise

        for i in range(1, num_labels):  # skip background
            if stats[i, cv2.CC_STAT_AREA] > MIN_AREA:
                clean[labels == i] = 255

        return clean
    
    noise_rm_image = noise_removal(thresh_image)
    cv2.imwrite("./../outputs/noise_rm_image.png", noise_rm_image)

    # Apply Erosion Effect
    def thin_font(image):
        image = cv2.bitwise_not(image)
        kernel = np.ones((2,2),np.uint8)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.bitwise_not(image)
        return (image)
    
    thin_font_image = thin_font(noise_rm_image)
    cv2.imwrite("./../outputs/thin_font_image.png", thin_font_image)

    # Apply Dilation on Image
    def thick_font(image):
        import numpy as np
        image = cv2.bitwise_not(image)
        kernel = np.ones((2,2),np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.bitwise_not(image)
        return (image)
    
    thick_font_image = thick_font(thin_font_image)
    cv2.imwrite("./../outputs/thick_font_image.png", thick_font_image)


    # --------------------------------------------------------------
    # STEP-1: OCR (same as yours)
    # --------------------------------------------------------------
    ocr_data = pytesseract.image_to_data(
        thick_font_image,
        output_type=Output.DICT,
        config="--oem 3 --psm 3"
    )


    # --------------------------------------------------------------
    # STEP-2: Extract ALL LINES (foundation)
    # --------------------------------------------------------------
    lines = []

    n = len(ocr_data["text"])

    for i in range(n):
        if ocr_data["level"][i] == 4:  # LINE
            x = ocr_data["left"][i]
            y = ocr_data["top"][i]
            w = ocr_data["width"][i]
            h = ocr_data["height"][i]

            if w > 10 and h > 10:
                lines.append({
                    "bbox": [x, y, x + w, y + h],
                    "h": h
                })



    # --------------------------------------------------------------
    # STEP-3: Sort LINES (top → bottom)
    # --------------------------------------------------------------
    lines.sort(key=lambda l: l["bbox"][1])


    line_heights = [l["h"] for l in lines]

    line_gaps = []
    for i in range(len(lines) - 1):
        _, _, _, y2 = lines[i]["bbox"]
        next_y1 = lines[i + 1]["bbox"][1]
        gap = next_y1 - y2
        if gap > 0:
            line_gaps.append(gap)

    median_height = int(np.median(line_heights))
    median_gap = int(np.median(line_gaps))

    # Adaptive threshold
    MAX_LINE_GAP = median_gap + int(0.5 * median_height)




    # --------------------------------------------------------------
    # STEP-4: Group LINES → BLOCKS (core logic)
    blocks = []
    current_block = {
        "bbox": lines[0]["bbox"].copy(),
        "lines": [lines[0]]
    }

    for i in range(1, len(lines)):
        prev = lines[i - 1]
        curr = lines[i]

        prev_x1, prev_y1, prev_x2, prev_y2 = prev["bbox"]
        curr_x1, curr_y1, curr_x2, curr_y2 = curr["bbox"]

        vertical_gap = curr_y1 - prev_y2

        # horizontal overlap
        overlap_x = max(0, min(prev_x2, curr_x2) - max(prev_x1, curr_x1))
        min_width = min(prev_x2 - prev_x1, curr_x2 - curr_x1)
        overlap_ratio = overlap_x / min_width if min_width > 0 else 0

        # ADAPTIVE MERGE CONDITION
        if vertical_gap <= MAX_LINE_GAP and overlap_ratio >= 0.4:
            # same logical block
            current_block["bbox"] = [
                min(current_block["bbox"][0], curr_x1),
                min(current_block["bbox"][1], curr_y1),
                max(current_block["bbox"][2], curr_x2),
                max(current_block["bbox"][3], curr_y2)
            ]
            current_block["lines"].append(curr)
        else:
            blocks.append(current_block)
            current_block = {
                "bbox": curr["bbox"].copy(),
                "lines": [curr]
            }

    blocks.append(current_block)


    # --------------------------------------------------------------
    # STEP-5: Build BLOCKS from LINES
    # --------------------------------------------------------------
    final_blocks = []
    for block in blocks:
        merged = False

        for fb in final_blocks:
            bx1, by1, bx2, by2 = block["bbox"]
            fx1, fy1, fx2, fy2 = fb["bbox"]

            if abs(by1 - fy2) <= MAX_LINE_GAP:
                fb["bbox"] = [
                    min(fx1, bx1),
                    min(fy1, by1),
                    max(fx2, bx2),
                    max(fy2, by2)
                ]
                fb["lines"].extend(block["lines"])
                merged = True
                break

        if not merged:
            final_blocks.append(block)



    # --------------------------------------------------------------
    # STEP-7: Draw ONLY FINAL MAJOR BLOCKS
    # --------------------------------------------------------------
    for i, block in enumerate(final_blocks, 1):
        x1, y1, x2, y2 = block["bbox"]

        cv2.rectangle(
            original,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            original,
            f"BLOCK {i}",
            (x1, y1 - 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1
        )

    cv2.imwrite("./../outputs/production_block_bbox.png", original)

    print(f"Final major blocks detected: {len(final_blocks)}")





















































































    # # --------------------------------------------------------------
    # # STEP 2: OCR with layout data
    # # --------------------------------------------------------------
    # ocr_data = pytesseract.image_to_data(
    #     thick_font_image,
    #     output_type=Output.DICT,
    #     config="--oem 3 --psm 3"       # automatic layout detection
    # )

    # number = len(ocr_data["text"])


    # # --------------------------------------------------------------
    # # STEP 3: Extract BLOCKS (level == 2)
    # # --------------------------------------------------------------
    # blocks = []

    # for i in range(number):
    #     if ocr_data["level"][i] == 2:   # BLOCK level
    #         block_num = ocr_data["block_num"][i]
    #         x1 = ocr_data["left"][i]
    #         y1 = ocr_data["top"][i]
    #         x2 = x1 + ocr_data["width"][i]
    #         y2 = y1 + ocr_data["height"][i]

    #         blocks.append({
    #             "block_num": block_num,
    #             "bbox": [x1, y1, x2, y2]
    #         })
    

    # # --------------------------------------------------------------
    # # STEP 3.1: Extract LINES (level == 4)
    # # --------------------------------------------------------------
    # lines = []

    # for i in range(number):
    #     if ocr_data["level"][i] == 4:  # LINE level
    #         lines.append({
    #             "bbox": (
    #                 ocr_data["left"][i],
    #                 ocr_data["top"][i],
    #                 ocr_data["width"][i],
    #                 ocr_data["height"][i]
    #             ),
    #             "line_num": ocr_data["line_num"][i]
    #         })


    # # --------------------------------------------------------------
    # # STEP 3.2: Attach LINES to BLOCKS
    # # --------------------------------------------------------------
    # for block in blocks:
    #     bx, by, bw, bh = block["bbox"]
    #     block["lines"] = []

    #     for line in lines:
    #         lx, ly, lw, lh = line["bbox"]

    #         # line top-left inside block
    #         if (bx <= lx <= bx + bw) and (by <= ly <= by + bh):
    #             block["lines"].append(line)


    # # --------------------------------------------------------------
    # # STEP 3.3: Tighten BLOCK bbox using LINE geometry
    # # --------------------------------------------------------------
    # refined_blocks = []

    # for block in blocks:
    #     if not block["lines"]:
    #         continue

    #     xs, ys, xe, ye = [], [], [], []

    #     for line in block["lines"]:
    #         x, y, w, h = line["bbox"]
    #         xs.append(x)
    #         ys.append(y)
    #         xe.append(x + w)
    #         ye.append(y + h)

    #     refined_blocks.append({
    #         "bbox": (
    #             min(xs),
    #             min(ys),
    #             max(xe) - min(xs),
    #             max(ye) - min(ys)
    #         ),
    #         "block_num": block["block_num"]
    #     })


    # for block in refined_blocks:
    #     x, y, w, h = block["bbox"]

    #     cv2.rectangle(
    #         original,
    #         (x, y),
    #         (x + w, y + h),
    #         (0, 255, 0),
    #         2
    #     )

    #     cv2.putText(
    #         original,
    #         f"BLOCK {block['block_num']}",
    #         (x, y - 5),
    #         cv2.FONT_HERSHEY_SIMPLEX,
    #         0.5,
    #         (0, 255, 0),
    #         1
    #     )

    # # --------------------------------------------------------------
    # # STEP 5: Save output
    # # --------------------------------------------------------------
    # cv2.imwrite("./../outputs/block_visualization_bbox.png", original)

    # print(f"Total blocks detected: {len(blocks)}")


