Here is the complete list of **Python libraries** that are used (or recommended) in the professional OCR desktop application project we discussed. These are the exact libraries needed to implement all the features and tasks effectively.

| # | Library Name          | Purpose / Usage in the Project                                                                 | Installation Command                  |
|---|-----------------------|-----------------------------------------------------------------------------------------------|---------------------------------------|
| 1 | **PyQt6** or **PySide6** | Main GUI framework for building the cross-platform desktop interface (windows, buttons, previews, etc.) | `pip install pyqt6` or `pip install pyside6` |
| 2 | **pytesseract**       | Python wrapper for Tesseract OCR engine – core library for performing text recognition       | `pip install pytesseract`            |
| 3 | **opencv-python**     | Image preprocessing (deskewing, binarization, noise reduction, contrast enhancement, etc.)   | `pip install opencv-python`          |
| 4 | **Pillow** (PIL)      | Additional image handling, loading, and conversion (often used alongside OpenCV)             | `pip install pillow`                 |
| 5 | **pdf2image**         | Convert PDF pages to images so they can be processed by OCR                                  | `pip install pdf2image`              |
| 6 | **PyMuPDF** (fitz)     | Alternative/fast PDF handling – extract pages as images or text (faster than pdf2image)      | `pip install pymupdf`                |
| 7 | **python-docx**       | Export OCR results to editable .docx (Word) files                                            | `pip install python-docx`            |
| 8 | **pyperclip**         | Copy extracted text to system clipboard easily                                               | `pip install pyperclip`              |
| 9 | **pyspellchecker**    | Optional spell-checking and text correction during post-processing                           | `pip install pyspellchecker`         |
|10 | **numpy**             | Required by OpenCV for efficient image array operations                                      | `pip install numpy`                  |
|11 | **configparser**      | Built-in – for reading/writing configuration files (no install needed)                       | Built-in                             |
|12 | **logging**           | Built-in – for application logging and error tracking                                        | Built-in                             |
|13 | **threading** / **concurrent.futures** | Built-in – for multi-threading and parallel batch processing                         | Built-in                             |
|14 | **pathlib**           | Built-in – modern file path handling                                                          | Built-in                             |
|15 | **json**              | Built-in – for storing settings or structured output (e.g., JSON export)                     | Built-in                             |

### Additional Optional Libraries (for advanced features)
| Library              | Purpose                                                                 | Command                          |
|----------------------|-------------------------------------------------------------------------|----------------------------------|
| **tabulate**         | Pretty-print tables in console or export to Markdown/CSV                | `pip install tabulate`          |
| **pandas**           | Handle structured data extraction (e.g., tables to DataFrame)           | `pip install pandas`            |
| **requests**         | Check for app updates or optional cloud OCR API integration             | `pip install requests`          |
| **darkdetect**       | Auto-detect system dark/light mode for theme switching                  | `pip install darkdetect`        |
| **pyinstaller**      | Package the app into a standalone executable for distribution           | `pip install pyinstaller`       |

### Important External Dependency (Not a Python library)
- **Tesseract OCR Engine** (the actual executable)  
  Must be installed separately on the system:  
  - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki  
  - macOS: `brew install tesseract`  
  - Linux: `sudo apt install tesseract-ocr`  
  pytesseract needs the path to `tesseract.exe` or `tesseract` command.

This is the **full and exact list** of Python libraries used in the project. You can safely include this in your documentation or requirements.txt file.

If you want, I can generate a complete `requirements.txt` file for you right now! Just say the word. 😊

