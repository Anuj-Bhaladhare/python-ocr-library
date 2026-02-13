import os, requests, json, fitz, re
from dotenv import load_dotenv
from fastapi import FastAPI
from pypdf import PdfReader
from pydantic import BaseModel, Field, ValidationError
from typing import List

load_dotenv()

# ---------------------------------------
# ----------- Pydantic Models -----------
# ---------------------------------------
class BoundingBoxField(BaseModel):
    bounding_box: list[int] = Field(..., description='The bounding box where the information was found [y_min, x_min, y_max, x_max]')  # Stores bounding box coordinates
    page: int = Field(..., description='Page number where the information was found. Start counting with 1.')  # Page number of the detected field

class TotalAmountField(BoundingBoxField):
    value: float = Field(..., description='The total amount of the invoice.')  # Total invoice amount

class RecipientField(BoundingBoxField):
    name: str = Field(..., description='The name of the recipient.')  # Recipient/customer name

class TaxAmountField(BoundingBoxField):
    value: float = Field(..., description='The total amount of the tax.')  # Tax amount on invoice

class SenderField(BoundingBoxField):
    name: str = Field(..., description='The name of the sender.')  # Sender/company name

class AccountNumberField(BoundingBoxField):
    account_no: str = Field(..., description='The number of the account.')  # Bank or account number


class InvoiceModel(BaseModel):
    total: TotalAmountField
    recipient: RecipientField


# -----------------------------------------
# -------------- API CALL -----------------
# -----------------------------------------
GEMMA3_URL = "http://localhost:11434/api/generate"

headers = {
    "Content-Type": "application/json"
}
def extract_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

pdf_text = extract_pdf_text("./invoice.pdf")

prompt = f"""
    Extract the invoice recipient name and invoice total.
    Return ONLY JSON that matches the provided schema.
    If a field is missing, set it to null (and bounding_box to [0,0,0,0]).

    Rules:
    - Return ONLY valid JSON that matches this schema exactly:
    - Return ONLY valid JSON — no explanation, no markdown, no extra text
    - Use null when value is missing / not found
    - Do NOT invent values
    - Format MUST match this schema exactly:

    {{
        "total": {{
            "value": float or null,
            "bounding_box": [0,0,0,0],
            "page": 0
        }},
        "recipient": {{
            "name": string or null,
            "bounding_box": [0,0,0,0],
            "page": 0
        }}
    }}

    Invoice Text:
    {pdf_text}

    Return ONLY the JSON object above.
"""

payload = {
    "model": "gemma3",
    "prompt": prompt,
    "stream": False
}

response = requests.post(GEMMA3_URL, headers=headers, json=payload, timeout=90) 

# response.raise_for_status()

raw = response.json()
result_text = raw.get("response", "").strip()

def extract_json(text):
    # Remove ```json and ``` fences
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)

invoice = extract_json(result_text)

print(invoice)

items_to_draw = [
    ('TOTAL', invoice['total']['bounding_box'], invoice['total']['page']),
    ('RECIPIENT', invoice['recipient']['bounding_box'], invoice['recipient']['page'])
]

doc = fitz.open("./invoice.pdf")             # Open original PDF for annotation

for label, box, page_no in items_to_draw:
    if not box or box == [0, 0, 0, 0] or page_no is None:
        continue                     # Skip missing or invalid bounding boxes

    page = doc[page_no - 1]          # Convert 1-based page number to 0-based index
    y0, x0, y1, x1 = box              # Unpack bounding box coordinates

    # From Gemini 2.0 onwards, models are further trained to detect objects in an image and get their bounding box coordinates.
    # The coordinates, relative to image dimensions, scale to [0, 1000]. You need to descale these coordinates based on your original image size.

    r = page.rect                    # Get page dimensions

    rect = fitz.Rect(
        (x0 / 1000) * r.width,       # Scale x_min to PDF width
        (y0 / 1000) * r.height,      # Scale y_min to PDF height
        (x1 / 1000) * r.width,       # Scale x_max to PDF width
        (y1 / 1000) * r.height,      # Scale y_max to PDF height
    )

    page.draw_rect(rect, color=(1,0,0), width=2)  # Draw red rectangle around detected field
    page.insert_text((rect.x0, rect.y0 - 2), label, fontsize=6, color=(1,0,0))  # Add label text above rectangle

doc.save("invoice_annotated.pdf")                   # Save annotated PDF
doc.close()                          # Close PDF document

