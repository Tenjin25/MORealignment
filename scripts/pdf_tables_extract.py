import camelot
import tabula
import os

pdf_path = "C:/Users/Shama/OneDrive/Documents/Course_Materials/CPT-236/Side_Projects/MORealignments/ActualResults-November82022.pdf"
output_dir = "C:/Users/Shama/OneDrive/Documents/Course_Materials/CPT-236/Side_Projects/MORealignments/Data"

# Camelot extraction
print("Extracting tables with Camelot...")
tables = camelot.read_pdf(pdf_path, pages="all")
for i, table in enumerate(tables):
    out_path = os.path.join(output_dir, f"camelot_table_{i+1}.csv")
    table.to_csv(out_path)
    print(f"Saved Camelot table {i+1} to {out_path}")

# Tabula extraction
print("Extracting tables with Tabula...")
tabula.convert_into(pdf_path, os.path.join(output_dir, "tabula_all_tables.csv"), output_format="csv", pages="all")
print(f"Saved all Tabula tables to {os.path.join(output_dir, 'tabula_all_tables.csv')}")
