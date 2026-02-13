import os                          # Used to access environment variables (API key)
import fitz                        # PyMuPDF library for reading, editing, and annotating PDFs
from google import genai           # Google Generative AI (Gemini) SDK
from dotenv import load_dotenv     # Loads variables from .env file into environment
from pydantic import BaseModel, Field  # Used for data validation and structured schemas
from fastapi import FastAPI, UploadFile, File, HTTPException

load_dotenv()                      # Load environment variables from .env file


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
    total: TotalAmountField          # Structured total amount data
    recipient: RecipientField        # Structured recipient data
    tax: TaxAmountField              # Structured tax data
    sender: SenderField              # Structured sender data
    account_no: AccountNumberField   # Structured account number data


client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))  # Initialize Gemini client using API key

file_in = 'invoice.pdf'             # Input PDF file path
file_out = 'invoice_annotated.pdf'  # Output PDF with annotations
pdf = client.files.upload(file=file_in)  # Upload PDF to Gemini for processing

prompt = """
Extract the invoice recipient name and invoice total.
Return ONLY JSON that matches the provided schema.
If a field is missing, set it to null (and bounding_box to [0,0,0,0]).
"""                                # Prompt instructing Gemini how to extract data

response = client.models.generate_content(
    model="gemini-2.5-flash",       # Gemini model used for fast multimodal extraction
    contents=[pdf, prompt],         # PDF + text prompt as input
    config={
        "response_mime_type": "application/json",  # Force JSON output
        "response_schema": InvoiceModel             # Enforce output schema
    },
)

invoice = InvoiceModel.model_validate_json(response.text)  # Validate Gemini JSON output with Pydantic
print(invoice.model_dump())          # Print validated invoice data as dict


items_to_draw = [
    ("TOTAL", invoice.total.bounding_box, invoice.total.page),          # Label + bounding box + page for total
    ("RECIPIENT", invoice.recipient.bounding_box, invoice.recipient.page),  # Recipient annotation data
    ("TAX", invoice.tax.bounding_box, invoice.tax.page),                # Tax annotation data
    ("SENDER", invoice.sender.bounding_box, invoice.sender.page),       # Sender annotation data
    ("ACCOUNT_NO", invoice.account_no.bounding_box, invoice.account_no.page) # Account number annotation data
]

doc = fitz.open(file_in)             # Open original PDF for annotation

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

doc.save(file_out)                   # Save annotated PDF
doc.close()                          # Close PDF document


