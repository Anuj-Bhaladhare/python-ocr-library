import pytesseract
import cv2

# Read Image 
image = cv2.imread("./../data/ocr_image_data/index_02.JPG")

# Convert to Gray Scale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
cv2.imwrite("./../data/ocr_image_data/temp/index_gray.png", gray_image)

# Apply blur Effect
blur_image = cv2.GaussianBlur(gray_image, (7, 7), 0)
cv2.imwrite("./../data/ocr_image_data/temp/index_blur.png", blur_image)

# Image Thresh the Image
thresh_image = cv2.threshold(blur_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cv2.imwrite("./../data/ocr_image_data/temp/index_thresh.png", thresh_image)

kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
cv2.imwrite("./../data/ocr_image_data/temp/index_kernal.png", kernal)

dilate = cv2.dilate(thresh_image, kernal, iterations=1)
cv2.imwrite("./../data/ocr_image_data/temp/index_dilate.png", dilate)

# Find the Contor
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])

results = []
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if h > 200 and w > 20:
        roi = image[y:y+h, x:x+h]
        cv2.imwrite("./../data/ocr_image_data/temp/index_roi.png", roi)

        cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)
        ocr_result = pytesseract.image_to_string(roi)

        ocr_result = ocr_result.split("\n")
        for item in ocr_result:
            results.append(item)

        # print(results)

entities = []
for item in results:
    item = item.strip().replace("\n", "")
    item = item.split(" ")[0]
    if len(item) > 0:
        if item[0] == "A" and "-" not in item:
            item = item.split(".")[0].replace(",", "").replace(";", "")
            entities.append(item)

print(f"{entities} \n\n")
entities.sort()
print(entities)





# cv2.imwrite("./../data/ocr_image_data/temp/index_bbox.png", image)
# cv2.imwrite("./../data/ocr_image_data/temp/index_roi.png", roi)
