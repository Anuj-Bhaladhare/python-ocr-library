# Import Libraries and Function in Programm
import cv2   # OpenCV for Computer Vision
import numpy as np
from matplotlib import pyplot as plt

class PreProcessingPhase:
    def __init__(self, data):
        self.data = data

        # Load image (Always required)
        # self.invoice_sample = "./../data/raw/invoice_sample.png"
        # self.invoice_sample = "./../data/raw/noisy_gray.png"
        # self.invoice_sample = "./../data/raw/page_01_rotated_01.jpg"tilt_image.jpeg
        self.invoice_sample = "./../data/raw/page_01.jpg"
        
        self.image = cv2.imread(self.invoice_sample)

    # =================================================================================
    # STEP-I: Convert Image to Grayscale Image | Convert to grayscale (Usually required)
    # =================================================================================
    def Convert_To_Grayscale(self):
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        cv2.imwrite("./../data/outputs/gray_image.png", self.gray_image)

        return self.gray_image
    
    # =================================================================================
    # https://becominghuman.ai/how-to-automatically-deskew-straighten-a-text-image-using-opencv-a0c30aed83df
    # STEP-II: Calculate skew angle of an image
    # =================================================================================
    def getSkewAngle(self, cvImage) -> float:
        # gray = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(cvImage, (9, 9), 0)
        thresh = cv2.threshold(
            blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
        dilate = cv2.dilate(thresh, kernel, iterations=2)


        contours, _ = cv2.findContours(
            dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )

        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        largestContour = contours[0]

        (center, (w, h), angle) = cv2.minAreaRect(largestContour)

        # 🔥 THIS IS THE FIX
        if w < h:
            angle = (angle + 90)

            # 🔥 Normalize angle range
            if angle < -90:
                angle += 180
            elif angle > 90:
                angle -= 180

        print(f"Detected skew angle === : {angle}")
        return -angle
    
    # =================================================================================
    # Rotate the image around its center
    # =================================================================================
    def rotateImage(self, binary_image, angle: float):
        newImage = binary_image.copy()
        (h, w) = newImage.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return newImage
    
    # Deskew image
    def deskew(self, cvImage):
        angle = self.getSkewAngle(cvImage)
        return self.rotateImage(cvImage, -1.0 * angle)
    
    # Deskewing — only if document is skewed
    def Deskewing(self):
        # deskewing_coords = cv2.findNonZero(self.binary_image)
        # deskewing_angle = cv2.minAreaRect(deskewing_coords)[-1]
        self.rotated_angle = self.getSkewAngle(self.gray_image)

        if self.rotated_angle == 0:
            print(f"No Needt to Rotat the Image || the image angle is => {self.rotated_angle}")
            self.rotated_fixed_image = self.gray_image
            cv2.imwrite("./../data/outputs/rotated_fixed_image.png", self.rotated_fixed_image)

            return self.rotated_fixed_image

        else:
            print(f"Processing for Deskwing | The Image Angle is => {self.rotated_angle}")

            # Not apply deskew    
            self.rotated_fixed_image = self.deskew(self.gray_image)

            # Save Deskive image
            cv2.imwrite("./../data/outputs/rotated_fixed_image.png", self.rotated_fixed_image)


    # =================================================================================
    # STEP-III: Remove Border from Grayscale Image
    # =================================================================================
    # def RemoveBorderImage(self):
    #     # 1️⃣ Area Coverage Check (MOST IMPORTANT)
    #     self.img_area = self.rotated_fixed_image.shape[0] * self.rotated_fixed_image.shape[1]
    #     self.contour_area = cv2.contourArea(self.rotated_fixed_image)
    #     self.area_ratio = self.contour_area / self.img_area

    #     # 2️⃣ Touching Image Edges Check

    #     # 3️⃣ Aspect Ratio Similarity

    #     # 4️⃣ Border Thickness (Optional but Strong)

    #     # Add Condition here for applying border Removing or NOT
    #     if case1 and case2 and case3 and case4:
    #         # apply border removing method

    #     else:
    #         # dont apply border removing method

    def RemoveBorderImage(self, image):
        """
        Returns True if a page-like border is detected, else False
        """
        image = self.rotated_fixed_image
        H, W = image.shape[:2]

        # Ensure binary image for contour detection
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        _, binary = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # No contours → no border
        if not contours:
            return image

        # Largest contour (possible border)
        cnt = max(contours, key=cv2.contourArea)

        # ---------------------------
        # 1️⃣ Area Coverage Check
        # ---------------------------
        img_area = H * W
        cnt_area = cv2.contourArea(cnt)
        area_ratio = cnt_area / img_area

        case1 = area_ratio > 0.80

        # ---------------------------
        # 2️⃣ Touching Image Edges
        # ---------------------------
        x, y, w, h = cv2.boundingRect(cnt)

        case2 = (
            x <= 5 or y <= 5 or
            x + w >= W - 5 or
            y + h >= H - 5
        )

        # ---------------------------
        # 3️⃣ Aspect Ratio Similarity
        # ---------------------------
        cnt_ratio = w / h
        img_ratio = W / H

        case3 = abs(cnt_ratio - img_ratio) < 0.20

        # ---------------------------
        # 4️⃣ Border Thickness
        # ---------------------------
        perimeter = cv2.arcLength(cnt, True)
        thickness = cnt_area / (perimeter + 1e-5)

        case4 = thickness < min(H, W) * 0.05

        # ---------------------------
        # Final Decision
        # ---------------------------
        if case1 and case2 and case3 and case4:
            # APPLY BORDER REMOVAL
            cropped = image[y:y+h, x:x+w]
            return cropped

        # NO BORDER → RETURN ORIGINAL
        return image



    def call_remove_border(self):
        output = self.RemoveBorderImage(self.rotated_fixed_image)
        print(f"output output output output ========> {output}")





    # =================================================================================
    # STEP-III: Remove Noise from Gray Image || Noise removal — only if needed
    # =================================================================================
    def Noise_Removal(self):
        self.noise_kernel = np.ones((1, 1), np.uint8)

        self.noise_removed_image = cv2.dilate(self.rotated_fixed_image, self.noise_kernel, iterations=1)

        self.noise_kernel = np.ones((1, 1), np.uint8)

        self.noise_removed_image = cv2.erode(self.noise_removed_image, self.noise_kernel, iterations=1)
        self.noise_removed_image = cv2.morphologyEx(self.noise_removed_image, cv2.MORPH_CLOSE, self.noise_kernel)
        self.noise_removed_image = cv2.medianBlur(self.noise_removed_image, 3)

        # Save image in File
        cv2.imwrite("./../data/outputs/noise_removed_image.png", self.noise_removed_image)

        return (self.noise_removed_image)

        # # Check Noise in image
        # laplacian_var = cv2.Laplacian(self.gray_image, cv2.CV_64F).var()

        # if laplacian_var < 100:
        #     print(f"IF Condition: {laplacian_var}")
        # else:
        #     print(f"Else Condition: {laplacian_var}")


    # =================================================================================
    # STEP-IV: Thresholding / binarization — only if needed
    # =================================================================================
    def Thresholding_binarization(self):

        # ensure grayscale image
        if len(self.noise_removed_image.shape) == 3:
            self.noise_removed_image = cv2.cvtColor(
                self.noise_removed_image, cv2.COLOR_BGR2GRAY
            )

        unique_vals = np.unique(self.noise_removed_image)
        print("Unique values count:", len(unique_vals))

        # IF image is NOT binary → apply binarization
        if len(unique_vals) > 2:
            print("IF Condition: Grayscale image detected → Applying binarization")

            self.binary_image = cv2.adaptiveThreshold(
                self.noise_removed_image,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                31,
                10
            )

        # ELSE image already binary
        else:
            print("ELSE Condition: Image already binary → Skipping binarization")
            self.binary_image = self.noise_removed_image

        cv2.imwrite(
            "./../data/outputs/thresholding_binarization.png",
            self.binary_image
        )


    # =================================================================================
    # STEP-IV: Erosion and Dilation — only if needed
    # =================================================================================
    """
        Erosion:
          - Erosion shrinks the white regions (foreground) in a binary image. It reduces the size of the objects in the image.
        Dilation: 
          - Dilation expands the white regions (foreground) in a binary image. It increases the size of the object in the image.
    """
    def Erosion_Dilation(self):

        # Erosion :- Erosion shrinks the white regions
        self.thin_font_image = cv2.bitwise_not(self.binary_image)
        self.thin_font_kernel = np.ones((2, 2), np.uint8)
        self.thin_font_image = cv2.erode(self.thin_font_image, self.thin_font_kernel, iterations = 1)
        self.thin_font_image = cv2.bitwise_not(self.thin_font_image)
        cv2.imwrite("./../data/outputs/eroded_image.jpg", self.thin_font_image)


        # Dilation :- Dilation expands the white regions
        self.thick_font_image = cv2.bitwise_not(self.thin_font_image)
        self.thick_font_kernel = np.ones((2, 2), np.uint8)
        self.thick_font_image = cv2.dilate(self.thick_font_image, self.thick_font_kernel, iterations = 1)
        self.thick_font_image = cv2.bitwise_not(self.thick_font_image)
        cv2.imwrite("./../data/outputs/dilated_image.jpg", self.thick_font_image)


