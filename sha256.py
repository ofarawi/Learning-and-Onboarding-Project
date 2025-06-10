import os
import hashlib

def pdf_to_sha256(pdf_path):
    sha256_hash = hashlib.sha256()
    with open(pdf_path, "rb") as f:
        while chunk := f.read(8192):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

# Folder containing the PDFs
PDF_FOLDER = "/Users/ofarawi/Desktop/RagArchAsync"

# Optional: Save output to a file
output_path = os.path.join(PDF_FOLDER, "sha256_hashes.txt")
with open(output_path, "w", encoding="utf-8") as out_file:
    for filename in os.listdir(PDF_FOLDER):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(PDF_FOLDER, filename)
            hash_value = pdf_to_sha256(full_path)
            line = f"{filename}: {hash_value}"
            print(line)
            out_file.write(line + "\n")
