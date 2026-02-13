from pdf2image import convert_from_path

pdf_path = "pdf_data/invoice.pdf"   # put a PDF in the same folder

images = convert_from_path(pdf_path, dpi=200)

for i, image in enumerate(images):
    image.save(f"image_output/page_{i+1}.png", "PNG")

print("Done! Images saved.")



