import os
import hashlib

def pdf_to_md5(pdf_path):
    md5_hash = hashlib.md5()
    with open(pdf_path, "rb") as f:
        while chunk := f.read(8192):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

# Folder containing the PDFs
PDF_FOLDER = "/Users/ofarawi/Desktop/RagArchAsync"

# Optional: Save output to a file
output_path = os.path.join(PDF_FOLDER, "md5_hashes.txt")
with open(output_path, "w", encoding="utf-8") as out_file:
    for filename in os.listdir(PDF_FOLDER):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(PDF_FOLDER, filename)
            hash_value = pdf_to_md5(full_path)
            line = f"{filename}: {hash_value}"
            print(line)
            out_file.write(line + "\n")
