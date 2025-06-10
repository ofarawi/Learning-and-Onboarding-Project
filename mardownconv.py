import os
import pdfplumber
from markdownify import markdownify as md

# Folder paths
INPUT_FOLDER = "/Users/ofarawi/Desktop/Recent50"
OUTPUT_FOLDER = "/Users/ofarawi/Desktop/PDF2MD"

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Loop through all PDF files in the input folder
for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(INPUT_FOLDER, filename)
        md_filename = os.path.splitext(filename)[0] + ".md"
        md_path = os.path.join(OUTPUT_FOLDER, md_filename)

        full_text = ""

        # Extract text from PDF
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n\n"

        # Convert to markdown and save
        markdown_text = md(full_text)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)

        print(f"Converted: {filename} → {md_filename}")
