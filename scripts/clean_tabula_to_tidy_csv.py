

import csv
import re
import os

input_path = r"C:/Users/Shama/OneDrive/Documents/Course_Materials/CPT-236/Side_Projects/MORealignments/Data/tabula_all_tables.csv"
output_path = r"C:/Users/Shama/OneDrive/Documents/Course_Materials/CPT-236/Side_Projects/MORealignments/Data/tabula_all_tables_tidy.csv"

# Helper to flatten multiline headers and candidate names
def flatten_header(header):
    header = header.replace('\n', ' ').replace('"', '').strip()
    header = re.sub(r'\s+', ' ', header)
    return header

def is_contest_header(line):
    return bool(re.match(r'^[A-Za-z].*', line)) and not line.startswith(('Adair', 'Total', 'District', 'St. ', 'St. Louis', 'Kansas City'))

def parse_candidate(candidate):
    # Try to split party and candidate name
    m = re.match(r'(Republican|Democratic|Libertarian|Constitution|Write-In|WI|REP|DEM|LIB|CST|GRN|IND|NPA|OTH)\s+(.*)', candidate)
    if m:
        return m.group(1), m.group(2)
    return '', candidate

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
            candidates = [c.strip() for c in header.split(',')]
        else:
            if re.match(r'^[A-Z][a-z]+', line) or line.startswith('Total') or line.startswith('St. '):
                parts = [r.strip() for r in line.split(',')]
                county = parts[0].upper()
                # Try to extract district from contest name if present (e.g., "U.S. House, 9")
                office = current_contest
                district = ''
                office_match = re.match(r'(.+?)(?:\s*District\s*(\d+))?$', office)
                if office_match:
                    office = office_match.group(1).strip()
                    if office_match.group(2):
                        district = office_match.group(2)
                for i, votes in enumerate(parts[1:]):
                    candidate = candidates[i] if i < len(candidates) else f"Candidate_{i+1}"
                    party, cand_name = parse_candidate(candidate)
                    votes_clean = votes.replace('"', '').replace(' ', '')
                    if votes_clean == '' or not votes_clean.isdigit():
                        continue
                    output_rows.append([county, office, district, party, cand_name, int(votes_clean)])

with open(output_path, "w", newline='', encoding="utf-8") as out:
    writer = csv.writer(out)
    writer.writerow(["county", "office", "district", "party", "candidate", "votes"])
    for row in output_rows:
        writer.writerow(row)
print(f"Saved truly tidy CSV to {output_path}")
