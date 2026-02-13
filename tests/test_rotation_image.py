import cv2   # OpenCV for Computer Vision
import numpy as np
from matplotlib import pyplot as plt

def getSkewAngle(cvImage) -> float:
    
    # 1 Blur + threshold
    blur = cv2.GaussianBlur(cvImage, (9, 9), 0)
    cv2.imwrite("./blur_image.png", blur)

    thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )[1]
    cv2.imwrite("./thresh_image.png", thresh)

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
        cv2.imwrite("./rotated_fixed_image.png", rotated_fixed_image)

        return rotated_fixed_image

    else:
        print(f"Processing for Deskwing | The Image Angle is => {rotated_angle}")

        # Not apply deskew    
        rotated_fixed_image = deskew(gray_image)

        # Save Deskive image
        cv2.imwrite("./rotated_fixed_image.png", rotated_fixed_image)

        return rotated_fixed_image

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ================================================================
# ================================================================

# Load and process image
# raw_image = cv2.imread("./../data/raw/page_01_rotated.JPG")
# raw_image = cv2.imread("./../data/raw/page_01_rotated_01.jpg")
# raw_image = cv2.imread("./../data/raw/book_rotated_image.jpg")

raw_image = cv2.imread("./../data/book_image/book_image_1.jpeg")
# raw_image = cv2.imread("./../data/book_image/book_image_2.jpeg")
# raw_image = cv2.imread("./../data/book_image/book_image_3.jpeg")

gray_img = grayscale(raw_image)

rotation_fix = Deskewing(gray_img)
cv2.imwrite("./rotation_fix.png", rotation_fix)















































# ==========================================================
# ================= Working Code Properlly =================
# ==========================================================
# import cv2   # OpenCV for Computer Vision
# import numpy as np
# from matplotlib import pyplot as plt

# def getSkewAngle(cvImage) -> float:
#     # gray = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(cvImage, (9, 9), 0)
#     thresh = cv2.threshold(
#         blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
#     )[1]
    
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
#     dilate = cv2.dilate(thresh, kernel, iterations=2)


#     contours, _ = cv2.findContours(
#         dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
#     )

#     contours = sorted(contours, key=cv2.contourArea, reverse=True)
#     largestContour = contours[0]

#     (center, (w, h), angle) = cv2.minAreaRect(largestContour)

#     # 🔥 THIS IS THE FIX
#     if w < h:
#         angle = (angle + 90)

#         # 🔥 Normalize angle range
#         if angle < -90:
#             angle += 180
#         elif angle > 90:
#             angle -= 180

#     print(f"Detected skew angle === : {angle}")
#     return -angle
    
# def rotateImage(binary_image, angle: float):
#     newImage = binary_image.copy()
#     (h, w) = newImage.shape[:2]
#     center = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)
#     newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
#     return newImage

# # Deskew image
# def deskew(cvImage):
#     angle = getSkewAngle(cvImage)
#     return rotateImage(cvImage, -1.0 * angle)

# def Deskewing(gray_image):
#     # deskewing_coords = cv2.findNonZero(binary_image)
#     # deskewing_angle = cv2.minAreaRect(deskewing_coords)[-1]

#     # Inverse the image
#     # inverse_img = cv2.bitwise_not(gray_image)

#     rotated_angle = getSkewAngle(gray_image)

#     if rotated_angle == 0:
#         print(f"No Needt to Rotat the Image || the image angle is => {rotated_angle}")
#         rotated_fixed_image = gray_image
#         cv2.imwrite("./rotated_fixed_image.png", rotated_fixed_image)

#         return rotated_fixed_image

#     else:
#         print(f"Processing for Deskwing | The Image Angle is => {rotated_angle}")

#         # Not apply deskew    
#         rotated_fixed_image = deskew(gray_image)

#         # Save Deskive image
#         cv2.imwrite("./rotated_fixed_image.png", rotated_fixed_image)

#         return rotated_fixed_image

# def grayscale(image):
#     return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # ================================================================
# # ================================================================

# # Load and process image
# # raw_image = cv2.imread("./../data/raw/page_01_rotated.JPG")
# raw_image = cv2.imread("./../data/raw/page_01_rotated_01.jpg")


# gray_img = grayscale(raw_image)

# rotation_fix = Deskewing(gray_img)
# cv2.imwrite("./rotation_fix.png", rotation_fix)
