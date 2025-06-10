import os
import re

# === Configuration ===
FOLDER_PATH = "/Users/ofarawi/Desktop/PDF2MD"
CALLSIGN = "K4GWA"

# === Regex setup (case-insensitive search) ===
pattern = re.compile(re.escape(CALLSIGN), re.IGNORECASE)

# === Loop through each Markdown file ===
total_matches = 0

for filename in os.listdir(FOLDER_PATH):
    if filename.lower().endswith(".md"):
        file_path = os.path.join(FOLDER_PATH, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        match_found = False
        for line_num, line in enumerate(lines, start=1):
            if pattern.search(line):
                if not match_found:
                    print(f"\nFile: {filename}")
                    match_found = True
                print(f"  Line {line_num}: {line.strip()}")
                total_matches += len(pattern.findall(line))

# === Summary ===
print(f"\nTotal occurrences of '{CALLSIGN}' across all files: {total_matches}")
