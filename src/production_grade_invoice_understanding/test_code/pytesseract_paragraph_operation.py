# STEP-0: Folder & Imports (Foundation)
import cv2
import pytesseract
from pytesseract import Output
import numpy as np
# from production_grade_invoice_understanding.test_code.test_function_classes import TestFunctionClasses

"""
    ChatGPT Documentation Link: https://chatgpt.com/c/69775f51-22dc-8323-b2df-41128353700d
    STEP-> 1️⃣ Read text with OCR
    STEP-> 2️⃣ Draw bounding boxes on every word
    STEP-> 3️⃣ Detect lines & blocks
    STEP-> 4️⃣ Find “Total / Final Total”
    STEP-> 5️⃣ Extract key → value pairs
    STEP-> 6️⃣ Export clean JSON output
"""

if __name__ == "__main__":

    # Classes Initilization
    # test_function = TestFunctionClasses(ocr_data=None)

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



# =====================================================================================
# ========================= Detect Paragraph with help of Line ======================== 
# =====================================================================================



    # # --------------------------------------------------------------
    # # STEP-3: OCR with Structured Data (Core Step)
    # # --------------------------------------------------------------
    # ocr_data = pytesseract.image_to_data(
    #     thick_font_image,
    #     output_type=Output.DICT,
    #     config="--oem 3 --psm 4" # try [--psm 3, 4, 1]
    # )

    # n = len(ocr_data["text"])

    # # ============================================================
    # # STEP-A: Extract ALL LINES (layout atoms)
    # # ============================================================
    # lines = []

    # for i in range(n):
    #     if ocr_data["level"][i] == 4:  # LINE
    #         lines.append({
    #             "bbox": (
    #                 ocr_data["left"][i],
    #                 ocr_data["top"][i],
    #                 ocr_data["width"][i],
    #                 ocr_data["height"][i]
    #             ),
    #             "words": []
    #         })


    # # ============================================================
    # # STEP-B: Attach WORDS to LINES
    # # ============================================================
    # for line in lines:
    #     lx, ly, lw, lh = line["bbox"]

    #     for i in range(n):
    #         if ocr_data["level"][i] == 5:  # WORD's
    #             word = ocr_data["text"][i].strip()
    #             if not word:
    #                 continue

    #             wx = ocr_data["left"][i]
    #             wy = ocr_data["top"][i]

    #             if (lx <= wx <= lx + lw) and (ly <= wy <= ly + lh):
    #                 line["words"].append(word)

    # print(f"lines ===========> {lines}") 

    # # ============================================================
    # # STEP-C: COLUMN CLUSTERING (X-axis based)
    # # ============================================================
    # columns = []
    # X_THRESHOLD = 90

    # for line in sorted(lines, key=lambda l: l["bbox"][0]):
    #     lx, _, _, _ = line["bbox"]
    #     placed = False

    #     for col in columns:
    #         cx = col["x_mean"]

    #         if abs(lx - cx) < X_THRESHOLD:
    #             col["lines"].append(line)
    #             col["x_positions"].append(lx)
    #             col["x_mean"] = int(np.mean(col["x_positions"]))
    #             placed = True
    #             break

    #     if not placed:
    #         columns.append({
    #             "x_positions": [lx],
    #             "x_mean": lx,
    #             "lines": [line]
    #         })

    # print(f"columns ========> {columns}")
    # # ============================================================
    # # STEP-D: SORT LINES VERTICALLY INSIDE EACH COLUMN
    # # ============================================================
    # for col in columns:
    #     col["lines"] = sorted(col["lines"], key=lambda l: l["bbox"][1])



    # # ============================================================
    # # STEP-E: PARAGRAPH GROUPING INSIDE EACH COLUMN
    # # ============================================================
    # paragraphs = []
    # Y_GAP_THRESHOLD = 24     # vertical gap threshold (tune 15–30)

    # for col in columns:
    #     current_para = []

    #     for i, line in enumerate(col["lines"]):
    #         if not current_para:
    #             current_para.append(line)
    #             continue

    #         prev_line = current_para[-1]
    #         _, py, _, ph = prev_line["bbox"]
    #         _, cy, _, _ = line["bbox"]

    #         if (cy - (py + ph)) < Y_GAP_THRESHOLD:
    #             current_para.append(line)
    #         else:
    #             paragraphs.append(current_para)
    #             current_para = [line]

    #     if current_para:
    #         paragraphs.append({
    #             "lines": current_para,
    #             "column": col
    #         })



    # # ============================================================
    # # STEP-F: BUILD PARAGRAPH BBOX + TEXT
    # # ============================================================
    # final_paragraphs = []

    # for para_obj in paragraphs:
    #     para_lines = para_obj["lines"]
    #     column = para_obj["column"]
    #     xs, ys, xe, ye = [], [], [], []
    #     texts = []

    #     for line in para_lines:
    #         x, y, w, h = line["bbox"]
    #         xs.append(x)
    #         ys.append(y)
    #         xe.append(x + w)
    #         ye.append(y + h)

    #         if line["words"]:
    #             texts.append(" ".join(line["words"]))

    #     # Column horizontal bounds
    #     col_xs = [l["bbox"][0] for l in column["lines"]]
    #     col_xe = [l["bbox"][0] + l["bbox"][2] for l in column["lines"]]

    #     col_x1 = min(col_xs)
    #     col_x2 = max(col_xe)

    #     # ---- Y should come ONLY from paragraph lines ----
    #     para_y1 = min(ys)
    #     para_y2 = max(ye)

    #     final_paragraphs.append({
    #         "bbox": (
    #             col_x1,
    #             para_y1,
    #             col_x2 - col_x1,
    #             para_y2 - para_y1
    #         ),
    #         "text": "\n".join(texts)
    #     })



    # print("Total columns:", len(columns))
    # print("Total paragraphs:", len(final_paragraphs))




    # # ============================================================
    # # STEP-G: DRAW FINAL PARAGRAPH BOXES
    # # ============================================================
    # for para in final_paragraphs:
    #     x, y, w, h = para["bbox"]

    #     cv2.rectangle(
    #         original,
    #         (x, y),
    #         (x+w, y+h),
    #         (0, 255, 0),
    #         2
    #     )

    #     cv2.putText(
    #         original,
    #         para["text"].split("\n")[0][:45],
    #         (x, y - 5),
    #         cv2.FONT_HERSHEY_SIMPLEX,
    #         0.45,
    #         (0, 0, 255),
    #         1
    #     )

    # # Save the image
    # cv2.imwrite("./../outputs/para_bonding_box_2nd.png", original)










    ocr_data = pytesseract.image_to_data(
        thick_font_image,
        output_type=Output.DICT,
        config="--oem 3 --psm 3"
    )
    print(f"ocr_data ======> {ocr_data}")

    # STEP 1️⃣ OCR → WORDS
    words = []
    n = len(ocr_data["text"])

    for i in range(n):
        if ocr_data["level"][i] == 5:
            text = ocr_data["text"][i].strip()
            if text:
                words.append({
                    "text": text,
                    "bbox": (
                        ocr_data["left"][i],
                        ocr_data["top"][i],
                        ocr_data["width"][i],
                        ocr_data["height"][i]
                    )
                })

    # print(f"words ======> {words}")


    # STEP 2️⃣ WORDS → LINES (Y clustering)
    LINES_Y_THRESHOLD = 10
    lines = []

    for w in sorted(words, key=lambda x: x["bbox"][1]):
        placed = False
        wx, wy, ww, wh = w["bbox"]

        for line in lines:
            _, ly, _, lh = line["bbox"]
            if abs(wy - ly) < LINES_Y_THRESHOLD:
                line["words"].append(w)
                placed = True
                break

        if not placed:
            lines.append({
                "words": [w],
                "bbox": w["bbox"]
            })
    # print(f"lines ======> {lines}")


    # STEP 3️⃣ NORMALIZE LINE BBOX
    for line in lines:
        xs, ys, xe, ye = [], [], [], []
        for w in line["words"]:
            x, y, w_, h_ = w["bbox"]
            xs.append(x)
            ys.append(y)
            xe.append(x + w_)
            ye.append(x + h_)

        line["bbox"] = (
            min(xs),
            min(ys),
            max(xe) - min(xs),
            max(ye) - min(ys)
        )
            
    # print(f"lines ======> {lines}")


    # STEP 4️⃣ LINES → COLUMNS (X clustering)
    COLUMN_X_THRESHOLD = 80
    columns = []

    for line in sorted(lines, key=lambda l: l["bbox"][0]):
        lx, _, _, _ = line["bbox"]
        placed = False

        for col in columns:
            if abs(lx - col["x_mean"]) < COLUMN_X_THRESHOLD:
                col["lines"].append(line)
                col["x_positions"].append(lx)
                col["x_mean"] = int(np.mean(col["x_positions"]))
                placed = True
                break

        if not placed:
            columns.append({
                "x_positions": [lx],
                "x_mean": lx,
                "lines": [line]
            })


    # print(f"columns ======> {columns}")

    # STEP 5️⃣ LINES → PARAGRAPHS (inside each column)
    PARA_Y_GAP = 25
    paragraphs = []

    for col in columns:
        col_lines = sorted(col["lines"], key=lambda l: l["bbox"][1])
        current = []

        for line in col_lines:
            if not current:
                current.append(line)
                continue

            _, py, _, ph = current[-1]["bbox"]
            _, cy, _, _ = line["bbox"]

            if cy - (py + ph) < PARA_Y_GAP:
                current.append(line)
            else:
                paragraphs.append({
                    "lines": current,
                    "column": col
                })
                current = [line]

        if current:
            paragraphs.append({
                "lines": current,
                "column": col
            })

    # print(f"paragraphs ========> {paragraphs}")


    # STEP 6️⃣ PARAGRAPH BOUNDING BOX (FINAL FIX 🔥)
    final_paragraphs = []

    for p in paragraphs:
        lines = p["lines"]
        col = p["column"]

        # X comes from column
        col_xs = [l["bbox"][0] for l in col["lines"]]
        col_xe = [l["bbox"][0] + l["bbox"][2] for l in col["lines"]]

        x1 = min(col_xs)
        x2 = max(col_xe)

        # Y comes from paragraph lines
        ys, ye = [], []
        text = []

        for l in lines:
            x, y, w, h = l["bbox"]
            ys.append(y)
            ye.append(y + h)
            text.append(" ".join(w["text"] for w in l["words"]))

        final_paragraphs.append({
            "bbox": (x1, min(ys), x2 - x1, max(ye) - min(ys)),
            "text": "\n".join(text)
        })

    # STEP 7️⃣ DRAW PARAGRAPH BOXES
    for p in final_paragraphs:
        x, y, w, h = p["bbox"]
        cv2.rectangle(original, (x,y), (x+w,y+h), (0,255,0), 2)

    cv2.imwrite("./../outputs/AAAAAAAAAAAAAAAAAAAAAAAA.png", original)

