import ollama
import cv2
import json
import re
import cv2
# from pdf2image import convert_from_path, convert_from_bytes

# images = convert_from_path('./../data/raw/invoice.pdf', dpi=300)

# # Save each page
# for i, page in enumerate(images):
#     page.save(f"page_{i+1}.png", "PNG")

image_path = "./page_1.png"

# Read Image from Computer Vision Library
cvImage = cv2.imread(image_path)

response = ollama.chat(
    model="llava:7b",
    messages=[
        {
            "role": "user",
            "content": (
                "Look at the image and return ONLY JSON.\n"
                "Extract the Details from the Document"
                "Return Invoice No, Date, Total in pixels. \n"
                "Format:\n"
                "{ \"Invoice No\": , \"Date\": , \"Total\":  }"
            ),
            "images": [image_path]
        }
    ]
)

llm_output = response["message"]["content"]
print("RAW LLM OUTPUT:\n", llm_output)

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in LLM output")
    return json.loads(match.group())

invoice_bbox = extract_json(llm_output)

print("Extracted Bounding Box: ", invoice_bbox)

# # Access values using keys
# x = invoice_bbox["x"]
# y = invoice_bbox["y"]
# w = invoice_bbox["w"]
# h = invoice_bbox["h"]

# image_with_box = cv2.rectangle(cvImage, (x, y), (x + w, y + h), (0, 255, 0), 2)

# cv2.imwrite("./putput_bbox.jpg", image_with_box)






















# import ollama
# import base64

# def image_to_base64(image_path):
#     with open(image_path, "rb") as img_file:
#         return base64.b64encode(img_file.read()).decode("utf-8")

# image_base64 = image_to_base64("../data/outputs/binary_image.jpg")
# print(f"image_base64: {image_base64}")

# response = ollama.chat(
#     model="llama3.1:8b",
#     messages=[
#         {
#             "role": "user",
#             "content": "Extract exact text from this image",
#             "images": [image_base64]   # ✅ Base64 goes HERE
#         }
#     ]
# )

# print(response["message"]["content"])


















