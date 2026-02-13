"""
1 -> grayscale
2 -> black and whight
3 -> noise remove
4 -> find borde

"""
import io, pytesseract, cv2, requests, base64, os
import numpy as np
from pypdf import PdfReader
from PIL import Image
from pathlib import Path


# ======================================================================================
# =============================== Declare All Funcion ==================================
# ======================================================================================

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# --------------------------------------------------------------------------------
# ---------------------- Rotate the image around its center ---------------------- 
# --------------------------------------------------------------------------------
def getSkewAngle(cvImage) -> float:
    
    # 1 Blur + threshold
    blur = cv2.GaussianBlur(cvImage, (9, 9), 0)
    cv2.imwrite("./../data/outputs/blur_image.png", blur)

    thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )[1]
    cv2.imwrite("./../data/outputs/thresh_image.png", thresh)

    # 2 Dilation to merge text lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # 3 Find Contours
    contours, _ = cv2.findContours(
        dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return 0.0

    h_img, w_img = cvImage.shape[:2]
    image_area = h_img * w_img

    valid_contours = []

    # 4️⃣ Filter contours (THIS IS THE FIX)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < image_area * 0.01:
            continue  # too small (noise)

        x, y, w, h = cv2.boundingRect(cnt)

        # Reject contours touching image border (likely border frame)
        if x <= 5 or y <= 5 or (x + w) >= (w_img - 5) or (y + h) >= (h_img - 5):
            continue

        valid_contours.append(cnt)

    # 5️⃣ Fallback: if everything was rejected, use largest contour
    if not valid_contours:
        valid_contours = contours

    # 6️⃣ Use largest valid contour
    largestContour = max(valid_contours, key=cv2.contourArea)

    # 7️⃣ Compute angle
    (_, (w, h), angle) = cv2.minAreaRect(largestContour)

    if w < h:
        angle += 90

    # Normalize
    if angle < -90:
        angle += 180
    elif angle > 90:
        angle -= 180

    print(f"Detected skew angle === : {angle}")
    return angle

def rotateImage(binary_image, angle: float):
    newImage = binary_image.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

# Deskew image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, angle)

def Deskewing(gray_image):
    # deskewing_coords = cv2.findNonZero(binary_image)
    # deskewing_angle = cv2.minAreaRect(deskewing_coords)[-1]

    # Inverse the image
    # inverse_img = cv2.bitwise_not(gray_image)

    rotated_angle = getSkewAngle(gray_image)

    if rotated_angle == 0:
        print(f"No Needt to Rotat the Image || the image angle is => {rotated_angle}")
        rotated_fixed_image = gray_image
        cv2.imwrite("./../data/outputs/rotated_fixed_image.png", rotated_fixed_image)

        return rotated_fixed_image

    else:
        print(f"Processing for Deskwing | The Image Angle is => {rotated_angle}")

        # Not apply deskew    
        rotated_fixed_image = deskew(gray_image)

        # Save Deskive image
        cv2.imwrite("./../data/outputs/rotated_fixed_image.png", rotated_fixed_image)

        return rotated_fixed_image
# --------------------------------------------------------------------------------
def remove_border(image, draw_debug=False, padding=5, min_area_ratio=0.0001):
    """
    Improved border removal - crops to the tight bounding box around all significant content contours.
    This handles disconnected text/content better by unioning all relevant bounding boxes.
    
    Parameters:
        image           : np.ndarray (BGR or grayscale)
        draw_debug      : bool → return image with drawn contours & final bounding box
        padding         : int → extra pixels around detected content (avoids cutting edges)
        min_area_ratio  : float → min area ratio to consider a contour as content (filters noise)
    
    Returns:
        cropped         : np.ndarray → content without outer borders/margins
        debug_img       : np.ndarray or None
    """
    original = image.copy()
    if len(original.shape) == 2:
        h, w = original.shape
        color = False
    else:
        h, w = original.shape[:2]
        color = True

    # ────────────────────────────────────────────────
    #  1. Preprocessing – get a clean binary image
    # ────────────────────────────────────────────────
    if color:
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    else:
        gray = original.copy()

    # Blur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive threshold for uneven lighting
    binary = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        21,  # blockSize (odd)
        10   # C
    )

    # Fallback to Otsu if adaptive fails (too empty)
    if np.count_nonzero(binary) < 0.05 * binary.size:
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # ────────────────────────────────────────────────
    #  2. Morphology – remove small noise, but don't over-close (we'll union boxes later)
    # ────────────────────────────────────────────────
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)

    # ────────────────────────────────────────────────
    #  3. Find all external contours
    # ────────────────────────────────────────────────
    contours, _ = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return original, None if draw_debug else original

    # ────────────────────────────────────────────────
    #  4. Filter small noise contours
    # ────────────────────────────────────────────────
    min_area = min_area_ratio * w * h
    content_contours = [c for c in contours if cv2.contourArea(c) > min_area]

    if not content_contours:
        # Fallback to largest if all are tiny
        content_contours = [max(contours, key=cv2.contourArea)]

    # ────────────────────────────────────────────────
    #  5. Compute union bounding box over all content contours
    # ────────────────────────────────────────────────
    min_x = w
    min_y = h
    max_x = 0
    max_y = 0

    for cnt in content_contours:
        x, y, bw, bh = cv2.boundingRect(cnt)
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + bw)
        max_y = max(max_y, y + bh)

    # Apply padding and clamp
    min_x = max(0, min_x - padding)
    min_y = max(0, min_y - padding)
    bw = min(w - min_x, max_x - min_x + 2 * padding)
    bh = min(h - min_y, max_y - min_y + 2 * padding)

    # ────────────────────────────────────────────────
    #  6. Crop
    # ────────────────────────────────────────────────
    cropped = original[min_y:min_y + bh, min_x:min_x + bw]

    # ────────────────────────────────────────────────
    #  7. Optional debug visualization
    # ────────────────────────────────────────────────
    debug_img = None
    if draw_debug:
        debug_img = original.copy()
        cv2.drawContours(debug_img, content_contours, -1, (0, 180, 0), 2)
        cv2.rectangle(debug_img, (min_x, min_y), (min_x + bw, min_y + bh), (0, 0, 255), 3)

    return cropped, debug_img

def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)

def Inverse_image(image):
    inver_img = cv2.bitwise_not(image)
    cv2.imwrite("./../data/outputs/inverse_image.png", inver_img)
    return image

def thin_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

def image_thresolding(image):
    if image is None:
        raise ValueError("Image not loaded")

    # Ensure grayscale (REQUIRED for adaptiveThreshold)
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Adaptive threshold
    binary_image = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )

    return binary_image

def extract_text_from_binary_image(binary_data):
    """
    Accepts either:
    - OpenCV binary image (numpy ndarray)
    - Encoded image bytes (PNG/JPEG)

    Converts to PIL Image and extracts text using pytesseract.
    """
    try:
        import io
        import numpy as np
        import cv2
        from PIL import Image
        import pytesseract

        # Case 1: Input is OpenCV image (ndarray)
        if isinstance(binary_data, np.ndarray):
            # Ensure image is uint8
            if binary_data.dtype != np.uint8:
                binary_data = binary_data.astype(np.uint8)

            # Encode image to PNG (IMPORTANT)
            success, buffer = cv2.imencode(".png", binary_data)
            if not success:
                raise ValueError("Failed to encode image")

            image_bytes = io.BytesIO(buffer.tobytes())

        # Case 2: Input is encoded image bytes
        elif isinstance(binary_data, (bytes, bytearray)):
            image_bytes = io.BytesIO(binary_data)

        else:
            raise TypeError(
                "binary_data must be a numpy ndarray or encoded image bytes"
            )

        # Open image with PIL
        image = Image.open(image_bytes).convert("L")

        # OCR
        text = pytesseract.image_to_string(image)

        return text

    except IOError as e:
        return f"Error opening image: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def extract_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def aiVisionTextExtractor(image_path: str, model: str = "gemma3") -> dict:

    """
        Extract text from an image using Ollama vision model (multimodal).

        Parameters:
            image_path : str or Path - local path to the image file (jpg, png, etc.)
            model      : str         - name of the vision model (e.g. gemma3, llama3.2-vision, llava, etc.)

        Returns:
            dict - the full Ollama /api/generate response (or error info)
                Most useful field is usually response.json()["response"]
    """

    GEMMA3_URL = "http://localhost:11434/api/generate"

    # ────────────────────────────────────────────────
    #  Validate & read image
    # ────────────────────────────────────────────────
    path = Path(image_path)
    if not path.is_file():
        return {"error": f"File not found: {image_path}"}

    try:
        with open(path, "rb") as f:
            image_bytes = f.read()
    except Exception as e:
        return {"error": f"Cannot read image: {str(e)}"}

    # Encode to base64 (required by Ollama REST API)
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # ────────────────────────────────────────────────
    #  Better prompt for text extraction
    # ────────────────────────────────────────────────
    prompt = """
        You are an accurate OCR and document understanding model.
        Extract **all visible text** from the image exactly as it appears.
        Preserve:
        - original line breaks
        - formatting / columns / tables (describe layout if needed)
        - headings, bold/italic words (use markdown if appropriate)
        - numbers, dates, special characters

        Do NOT summarize or interpret — output **only the extracted raw text**.
        If no text is visible, reply only: "No readable text found."
    """.strip()

    payload = {
        "model": model,
        "prompt": prompt,
        "images": [base64_image],          # ← this is the correct key for vision models
        "stream": False,
        "options": {
            "temperature": 0.0,            # lower = more deterministic / accurate OCR
            "num_predict": 2048,           # increase if documents are long
            # "num_ctx": 8192,             # uncomment & increase if context is cut off
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            GEMMA3_URL,
            headers=headers,
            json=payload,
            timeout=120          # longer timeout for large images / slow GPU
        )
        response.raise_for_status()  # raise if 4xx/5xx

        result = response.json()

        # Add extracted text for convenience
        result["extracted_text"] = result.get("response", "").strip()

        return result

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "status_code": getattr(e.response, "status_code", None) if 'response' in locals() else None
        }

def extract_text_only(image_path: str, model: str = "gemma3") -> str:
    result = aiVisionTextExtractor(image_path, model)
    if "error" in result:
        return f"ERROR: {result['error']}"
    return result.get("extracted_text", "No response from model")











# ==================================================================================================
# ======================================= Working Code Flow ========================================
# ==================================================================================================

# Load and process image
# raw_image = cv2.imread("./../data/raw/page_01_rotated.JPG")
# raw_image = cv2.imread("./../data/raw/page_01_rotated_01.jpg")
# raw_image = cv2.imread("./../data/raw/book_rotated_image.jpg")

raw_image = cv2.imread("./../data/book_image/book_image_1.jpeg")
# raw_image = cv2.imread("./../data/book_image/book_image_2.jpeg")
# raw_image = cv2.imread("./../data/book_image/book_image_3.jpeg")

# Step-1: Convert image to Gray Image
gray_image = grayscale(raw_image)
cv2.imwrite("./../data/outputs/gray_image.png", gray_image)

# =====================================================
rotated_fix_image = Deskewing(gray_image)
cv2.imwrite("./../data/outputs/rotated_fix_image.png", rotated_fix_image)

# =====================================================
cropped, debug = remove_border(rotated_fix_image, draw_debug=True, padding=3)
cv2.imwrite("./../data/outputs/border_cropped.png", cropped)



# # Step-3: Border detection/removal | No Border
# no_border_images = RemoveBorderImage(rotated_fixed_image)
# cv2.imwrite("./../data/outputs/bordered_image.jpg", no_border_images)

# # ============================================================
# # No Border black and white image
# # ============================================================
# no_border_black_and_white = cv2.bitwise_not(no_border_images)
# cv2.imwrite("./../data/outputs/no_border_black_and_white.jpg", no_border_black_and_white)

# Step-4: apply thresolding on image
binary_image = image_thresolding(cropped)
cv2.imwrite("./../data/outputs/binary_image.jpg", binary_image)

# # Step-5: Inverse the Image 
# inverse_img = Inverse_image(binary_image)
# cv2.imwrite("./../data/outputs/black_and_white.jpg", inverse_img)


# no_noise_image = noise_removal(binary_image)
# cv2.imwrite("./../data/outputs/no_noise_image.jpg", no_noise_image)

# Erosion :- Erosion shrinks the white regions
thin_font_image = thin_font(binary_image)
cv2.imwrite("./../data/outputs/erodade_image.jpg", thin_font_image)

# Dilation :- Dilation expands the white regions
thick_font_image = thick_font(thin_font_image)
cv2.imwrite("./../data/outputs/dilated_image.jpg", thick_font_image)

text = extract_text_only("./../data/outputs/dilated_image.jpg", model="gemma3")
print(text)




# ================================ Usage Example ================================
# Extract text from binary image
# try:
#     extracted_text = extract_text_from_binary_image(inverse_img)
#     print("Extracted Text:")
#     print(extracted_text)

# except FileNotFoundError as e:
#     print("Please create or specify a valid image file named 'example_image.png' to test this script.: ", e)


# ================================ Usage Example ================================
# pdf_text = extract_pdf_text("./no_border_black_and_white.jpg")
# print(pdf_text)

