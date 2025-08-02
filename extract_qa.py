import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
from transformers import pipeline
import tkinter as tk
from tkinter import filedialog

# Set up Tesseract path if not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path):
    print("[INFO] Converting PDF to images...")
    images = convert_from_path(pdf_path)
    text = ""
    for i, img in enumerate(images):
        print(f"[INFO] Extracting text from page {i + 1}...")
        text += pytesseract.image_to_string(img)
    return text

def extract_text_from_image(image_path):
    print("[INFO] Extracting text from image...")
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)

def choose_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a PDF or Image File",
        filetypes=[("PDF files", "*.pdf"), ("Image files", "*.png *.jpg *.jpeg")]
    )
    return file_path

def main():
    print("Select a file (PDF or image) to extract text...")
    file_path = choose_file()

    if not file_path:
        print("[ERROR] No file selected.")
        return

    if file_path.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        text = extract_text_from_image(file_path)
    else:
        print("[ERROR] Unsupported file format.")
        return

    print("\n[INFO] Text successfully extracted.\n")

    # Initialize QA model
    print("[INFO] Loading QA model...")
    qa_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

    while True:
        question = input("\nAsk a question about the content (or type 'exit' to quit):\n> ")
        if question.lower() == 'exit':
            print("Exiting...")
            break
        result = qa_model(question=question, context=text)
        print("Answer:", result['answer'])

if __name__ == "__main__":
    main()
