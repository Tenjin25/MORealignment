
import csv
import re
import os

input_path = r"C:/Users/Shama/OneDrive/Documents/Course_Materials/CPT-236/Side_Projects/MORealignments/Data/tabula_all_tables.csv"
output_path = r"C:/Users/Shama/OneDrive/Documents/Course_Materials/CPT-236/Side_Projects/MORealignments/Data/tabula_all_tables_grouped_cleaned.csv"

# Helper to flatten multiline headers and candidate names
def flatten_header(header):
    # Remove newlines, quotes, and extra spaces
    header = header.replace('\n', ' ').replace('"', '').strip()
    # Collapse multiple spaces
    header = re.sub(r'\s+', ' ', header)
    return header

# Helper to detect contest header
def is_contest_header(line):
    return bool(re.match(r'^[A-Za-z].*', line)) and not line.startswith(('Adair', 'Total', 'District', 'St. ', 'St. Louis', 'Kansas City'))

# Read all lines
with open(input_path, encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

contests = []
current_contest = None
header = None
rows = []

for line in lines:
    if is_contest_header(line):
        if current_contest and header and rows:
            contests.append((current_contest, header, rows))
        current_contest = flatten_header(line)
        header = None
        rows = []
    elif current_contest:
        if header is None:
            header = flatten_header(line)
        else:
            if re.match(r'^[A-Z][a-z]+', line) or line.startswith('Total') or line.startswith('St. '):
                rows.append([r.strip() for r in line.split(',')])

if current_contest and header and rows:
    contests.append((current_contest, header, rows))

with open(output_path, "w", newline='', encoding="utf-8") as out:
    writer = csv.writer(out)
    for contest_name, header, data_rows in contests:
        # Write contest name as a merged cell
        writer.writerow([contest_name])
        # Write header, split by candidate and party, and make it easier to read
        candidates = [c.strip() for c in header.split(',')]
        writer.writerow(["County"] + candidates)
        for row in data_rows:
            writer.writerow(row)
        writer.writerow([])  # Blank line between contests
print(f"Saved grouped and cleaned CSV to {output_path}")
