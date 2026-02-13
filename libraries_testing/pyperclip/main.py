import cv2, pytesseract
from preprocessing import PreProcessingPhase
from steplogger import StepLogger

preprocess = PreProcessingPhase(data=None)
step_logger = StepLogger()

# Read Image | Load Image
invoice_sample = cv2.imread("./data/invoice_sample.png")
fill_form = cv2.imread("./data/fill_form.jpg")
id_card = cv2.imread("./data/id_card.jpg")

# =======================================================
def compute_metrics(gray):
    print("compute_metrics(gray)")
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    contrast = gray.std()
    edges = cv2.Canny(gray, 50, 150)
    edge_density = edges.sum() / edges.size
    return lap_var, contrast, edge_density

# ========================================================
def process_invoice(img):
    print("rocess_invoice(img)")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap, contrast, edge_density = compute_metrics(gray)
    print(f"\n\nlap => {lap} \n contrast => {contrast} \n edge_density => {edge_density}")

    if lap < 120:
        gray = cv2.GaussianBlur(gray, (5,5), 0)

    if contrast < 45:
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 31, 10)
    else:
        binary = gray

    # Strengthen table lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return binary

# ========================================================
def process_form(img):
    print("process_form(img)")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap, _, _ = compute_metrics(gray)

    if lap < 110:
        gray = cv2.medianBlur(gray, 3)

    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV, 25, 8)

    # Box detection
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return binary

# =========================================================
def process_id(img):
    print("process_id(img)")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Strong denoise
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    # Glare detection
    bright_ratio = (gray > 240).sum() / gray.size

    if bright_ratio < 0.05:
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 31, 10)
    else:
        binary = gray

    return binary

# ===========================================================
def process_document(img, doc_type):
    if doc_type == "invoice":
        return process_invoice(img)
    elif doc_type == "form":
        return process_form(img)
    elif doc_type == "id":
        return process_id(img)
    else:
        raise ValueError("Unsupported document type")

# =======================================================
def extract_layout_features(gray):
    h, w = gray.shape
    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    areas = [cv2.contourArea(c) for c in contours]

    return {
        "num_contours": len(contours),
        "avg_contour_area": sum(areas) / (len(areas) + 1),
        "edge_density": cv2.countNonZero(edges) / edges.size,  # ✅ FIXED
        "aspect_ratio": w / h
    }

# =========================================================
def detect_document_type(features):
    num = features["num_contours"]
    edge = features["edge_density"]
    ar = features["aspect_ratio"]
    area = features["avg_contour_area"]

    # 1️⃣ ID CARD (wide, few contours, moderate edges)
    if (
        ar > 1.3 and
        20 <= num <= 50 and
        0.02 <= edge <= 0.06
    ):
        return "id", 0.92

    # 2️⃣ FORM (many boxes, very high edge density)
    if (
        num >= 120 and
        edge > 0.06
    ):
        return "form", 0.88

    # 3️⃣ INVOICE (tables + text, medium everything)
    if (
        50 <= num <= 120 and
        0.03 <= edge <= 0.06 and
        area < 1500
    ):
        return "invoice", 0.85

    return "unknown", 0.50

# ==========================================================
def denoise_if_needed(gray, logger):
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    if lap_var < 120:
        logger.log(
            "denoise",
            True,
            f"Low sharpness (Laplacian={lap_var:.1f})",
            min(1.0, (120 - lap_var) / 120)
        )
        return cv2.GaussianBlur(gray, (5,5), 0)

    logger.log(
        "denoise",
        False,
        f"Image sharp (Laplacian={lap_var:.1f})",
        0.95
    )
    return gray

# ==========================================================
def threshold_if_needed(gray, logger):
    contrast = gray.std()

    if contrast < 45:
        logger.log(
            "threshold",
            True,
            f"Low contrast ({contrast:.1f})",
            min(1.0, (45 - contrast) / 45)
        )
        return cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 31, 10)

    logger.log(
        "threshold",
        False,
        f"Good contrast ({contrast:.1f})",
        0.9
    )
    return gray

# ===========================================================
def run_tesseract(img):
    config = "--oem 3 --psm 6"
    text = pytesseract.image_to_string(img, config=config)
    data = pytesseract.image_to_data(
        img, output_type=pytesseract.Output.DICT)

    avg_conf = sum(
        int(c) for c in data["conf"] if c != "-1"
    ) / max(1, len(data["conf"]))

    return text, avg_conf / 100


# ----------------------------------------------------------
# --------------- Start Calling the Function ---------------
# ----------------------------------------------------------

gray_image = cv2.cvtColor(id_card, cv2.COLOR_BGR2GRAY)

features = extract_layout_features(gray_image)

print("FEATURES DEBUG:")
for k, v in features.items():
    print(f"{k} => {v}")

doc_type, doc_conf = detect_document_type(features)

print(f"doc_type => {doc_type}")

step_logger.log(
    "doc_type_detection",
    True,
    f"Detected as {doc_type}",
    doc_conf
)

gray = denoise_if_needed(gray_image, step_logger)
processed = threshold_if_needed(gray, step_logger)

text, ocr_conf = run_tesseract(processed)

output = {
    "document_type": doc_type,
    "ocr_text": text,
    "ocr_confidence": round(ocr_conf, 2),
    "steps": step_logger.logs
}

print(f"output => {output}")
