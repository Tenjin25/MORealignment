import csv
import re
import os

input_path = r"C:/Users/Shama/OneDrive/Documents/Course_Materials/CPT-236/Side_Projects/MORealignments/Data/tabula_all_tables.csv"
output_path = r"C:/Users/Shama/OneDrive/Documents/Course_Materials/CPT-236/Side_Projects/MORealignments/Data/tabula_all_tables_cleaned.csv"

# Helper to flatten multiline headers

def flatten_header(header):
    return header.replace('\n', ' ').replace('"', '').strip()

# Helper to detect contest header

def is_contest_header(line):
    return bool(re.match(r'^[A-Za-z].*', line)) and not line.startswith(('Adair', 'Total', 'District', 'St. ', 'St. Louis', 'Kansas City'))

# Read all lines
with open(input_path, encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

output_rows = []
current_contest = None
header = None

for line in lines:
    if is_contest_header(line):
        current_contest = flatten_header(line)
        header = None
    elif current_contest:
        if header is None:
            header = flatten_header(line)
            # Add contest and header row
            output_rows.append(["Contest"] + header.split(','))
        else:
            # If line starts with a county or 'Total', add as data row
            if re.match(r'^[A-Z][a-z]+', line) or line.startswith('Total') or line.startswith('St. '):
                output_rows.append([current_contest] + [r.strip() for r in line.split(',')])

# Write cleaned CSV
with open(output_path, "w", newline='', encoding="utf-8") as out:
    writer = csv.writer(out)
    for row in output_rows:
        writer.writerow(row)
print(f"Saved cleaned CSV to {output_path}")
