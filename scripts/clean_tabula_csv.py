import csv
import re
import os

input_path = r"C:/Users/Shama/OneDrive/Documents/Course_Materials/CPT-236/Side_Projects/MORealignments/Data/tabula_all_tables.csv"
output_dir = r"C:/Users/Shama/OneDrive/Documents/Course_Materials/CPT-236/Side_Projects/MORealignments/Data/contest_csvs"
os.makedirs(output_dir, exist_ok=True)

# Helper to sanitize filenames
def sanitize_filename(name):
    return re.sub(r'[^\w\-]+', '_', name.strip())

# Read all lines
with open(input_path, encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

contests = []
current_contest = None
header = None
rows = []

for line in lines:
    # Detect contest header (starts with a non-county, non-total, non-numeric, and not 'Total')
    if re.match(r'^[A-Za-z].*', line) and not line.startswith(('Adair', 'Total', 'District', 'St. ', 'St. Louis', 'Kansas City')):
        # Save previous contest
        if current_contest and header and rows:
            contests.append((current_contest, header, rows))
        # Start new contest
        current_contest = line.replace('"', '').replace(',', '').replace('\n', ' ').strip()
        header = None
        rows = []
    elif current_contest:
        # If header not set, set it
        if header is None:
            header = line.replace('"', '').replace('\n', ' ').strip()
        else:
            # If line starts with a county or 'Total', add as data row
            if re.match(r'^[A-Z][a-z]+', line) or line.startswith('Total') or line.startswith('St. '):
                rows.append(line)

# Add last contest
if current_contest and header and rows:
    contests.append((current_contest, header, rows))

# Write each contest to a separate CSV
for contest_name, header, data_rows in contests:
    filename = sanitize_filename(contest_name) + ".csv"
    out_path = os.path.join(output_dir, filename)
    with open(out_path, "w", newline='', encoding="utf-8") as out:
        writer = csv.writer(out)
        # Write header
        writer.writerow([h.strip() for h in header.split(',')])
        # Write rows
        for row in data_rows:
            writer.writerow([r.strip() for r in row.split(',')])
print(f"Saved {len(contests)} cleaned contest CSVs to {output_dir}")
