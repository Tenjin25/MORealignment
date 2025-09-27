
import pdfplumber
import pandas as pd
import os

pdf_path = "C:/Users/Shama/OneDrive/Documents/Course_Materials/CPT-236/Side_Projects/MORealignments/ActualResults-November82022.pdf"
csv_path = "C:/Users/Shama/OneDrive/Documents/Course_Materials/CPT-236/Side_Projects/MORealignments/Data/ActualResults-November82022.csv"


rows = []
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            rows.extend(table)



# Extract each contest's results into a separate CSV
contest_indices = []
for i, row in enumerate(rows):
    if row and row[0] and not row[0].isdigit() and any("\n" in str(cell) for cell in row[1:]):
        contest_indices.append(i)

for idx, start in enumerate(contest_indices):
    contest_name = rows[start][0].strip()
    candidate_row = rows[start]
    # Merge party and candidate name for each column except county
    merged_candidates = []
    for c in candidate_row[1:]:
        parts = [p.strip() for p in c.replace('"', '').split('\n') if p.strip()]
        if len(parts) == 2:
            merged_candidates.append(f"{parts[1]} ({parts[0]})")
        elif len(parts) == 1:
            merged_candidates.append(parts[0])
        else:
            merged_candidates.append(c.replace('\n', ' ').strip())
    header = ['County'] + merged_candidates
    # Find end index (next contest or end of rows)
    end = contest_indices[idx+1] if idx+1 < len(contest_indices) else len(rows)
    data_rows = rows[start+1:end]
    cleaned_data = []
    for row in data_rows:
        if row and row[0] and row[0].lower() not in ['county', 'contest']:
            cleaned_row = [row[0].strip()] + [str(x).strip() for x in row[1:]]
            cleaned_data.append(cleaned_row)
    df = pd.DataFrame(cleaned_data, columns=header)
    # Save to CSV, sanitize contest name for filename
    safe_name = contest_name.replace('\n', '_').replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '').replace('.', '').replace(':', '').replace('"', '')
    out_path = f"C:/Users/Shama/OneDrive/Documents/Course_Materials/CPT-236/Side_Projects/MORealignments/Data/{safe_name}.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved {contest_name} to {out_path}")

# Remove empty rows and duplicates
df = pd.DataFrame(rows)
df = df.dropna(how='all')
df = df.drop_duplicates()



# Fix: Find the header row and all county rows
header_row_idx = None
for i, row in enumerate(rows):
    if row and row[0] == 'United States Senator':
        header_row_idx = i
        break

if header_row_idx is not None:
    # Use first row as header, all subsequent rows as county data
    header_row = rows[0]
    contest_name = header_row[0].strip()
    # Merge party and candidate name for each column except county
    merged_candidates = []
    for c in header_row[1:]:
        parts = [p.strip() for p in c.replace('"', '').split('\n') if p.strip()]
        if len(parts) == 2:
            merged_candidates.append(f"{parts[1]} ({parts[0]})")
        elif len(parts) == 1:
            merged_candidates.append(parts[0])
        else:
            merged_candidates.append(c.replace('\n', ' ').strip())
    header = ['Contest', 'County'] + merged_candidates
    data_rows = rows[1:]
    cleaned_data = []
    for row in data_rows:
        if row and row[0] and row[0].lower() not in ['county', 'contest']:
            cleaned_row = [contest_name, row[0].strip()] + [str(x).strip() for x in row[1:]]
            cleaned_data.append(cleaned_row)
    df = pd.DataFrame(cleaned_data, columns=header)
else:
    # Fallback: use previous logic
    custom_header = [
        "County",
        "Republican: Eric Schmitt",
        "Democratic: Trudy Busch Valentine",
        "Libertarian: Jonathan Dine",
        "Constitution: Paul Venable",
        "Write-In: Nathan V. Mooney",
        "Write-In: Theo Brown Sr",
        "Write-In: David Kirk"
    ]
    df = pd.DataFrame(rows[2:], columns=custom_header)

# Strip whitespace from all string cells
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

df.to_csv(csv_path, index=False)
print(f"CSV saved to {os.path.abspath(csv_path)}")
