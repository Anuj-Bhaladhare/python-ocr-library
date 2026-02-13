import cv2
import numpy as np
from PIL import Image


class RotateImage():

    def __init__(self):
        pass


    def imageRotation(self):

        self.image_file = "image_data/image_1.jpg"
        image = Image.open(self.image_file)

        image = image.rotate(
            angle=50, 
            expand=True, 
            fillcolor="green", 
            # center=(100, 100),
            resample=Image.BICUBIC
        )

        image.show()


    def getSkewAngle(self, cvImage) -> float:
        
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

        # print(f"Detected skew angle === : {angle}")
        return angle


    def skewAngle(self, rotate_image_path):
        # self.rotate_image_path = "image_data/book_image_1.jpeg"

        self.rotate_image = cv2.imread(rotate_image_path)

        self.gray_image = cv2.cvtColor(self.rotate_image, cv2.COLOR_BGR2GRAY)

        self.rotate_angle = self.getSkewAngle(self.gray_image)

        # print(f"The Angle is ==========> { self.rotate_angle}")
        return self.rotate_angle


    def deskiwImage(self):

        self.rotate_image_path = "image_data/book_image_2.jpeg"

        self.image = Image.open(self.rotate_image_path)

        self.skiw_angle = self.skewAngle(self.rotate_image_path)

        self.image = self.image.rotate(
            angle=self.skiw_angle, 
            expand=True, 
            fillcolor="#ffffff", 
            # center=(100, 100),
            resample=Image.BICUBIC
        )

        self.image.save("image_output/deskiw_image_2.png")

        self.image.show()

