
# All imports at the very top
import os
import re
import pandas as pd
import json
from collections import defaultdict

# Paths
DATA_DIR = 'Data'
OUTPUT_PATH = 'Data/mo_county_aggregated_results.json'

# Load valid counties and build normalization map
county_fips_path = os.path.join(DATA_DIR, 'mo_county_fips.csv')
county_df = pd.read_csv(county_fips_path)
def normalize_county_key(name):
    if not isinstance(name, str):
        return ''
    return re.sub(r'[^a-z]', '', name.lower())

# Build a mapping from normalized key to official county name
county_name_map = {}
for official in county_df['County']:
    key = normalize_county_key(official)
    county_name_map[key] = official
# Add St. Louis City explicitly if not present
county_name_map[normalize_county_key('St. Louis City')] = 'St. Louis City'

def get_official_county_name(name):
    # Robust handling for St. Louis variants
    key = normalize_county_key(name)
    if key == normalize_county_key('ST LOUIS'):
        # If the original name is exactly 'ST LOUIS', treat as 'St. Louis County'
        return county_name_map.get(normalize_county_key('St. Louis County'), None)
    if key == normalize_county_key('ST LOUIS CITY'):
        return county_name_map.get(normalize_county_key('St. Louis City'), None)
    # Try direct match
    return county_name_map.get(key, None)

# Ballotpedia-style metadata
output_json = {
    "focus": "Clean geographic political patterns",
    "processed_date": "2025-01-07",
    "categorization_system": {
        "competitiveness_scale": {
            "Republican": [
                {"category": "Annihilation", "range": "R+40%+", "color": "#67000d"},
                {"category": "Dominant", "range": "R+30-40%", "color": "#a50f15"},
                {"category": "Stronghold", "range": "R+20-30%", "color": "#cb181d"},
                {"category": "Safe", "range": "R+10-20%", "color": "#ef3b2c"},
                {"category": "Likely", "range": "R+5.5-10%", "color": "#fb6a4a"},
                {"category": "Lean", "range": "R+1-5.5%", "color": "#fcae91"},
                {"category": "Tilt", "range": "R+0.5-1%", "color": "#fee8c8"}
            ],
            "Tossup": [
                {"category": "Tossup", "range": "±0.5%", "color": "#f7f7f7"}
            ],
            "Democratic": [
                {"category": "Tilt", "range": "D+0.5-1%", "color": "#e1f5fe"},
                {"category": "Lean", "range": "D+1-5.5%", "color": "#c6dbef"},
                {"category": "Likely", "range": "D+5.5-10%", "color": "#9ecae1"},
                {"category": "Safe", "range": "D+10-20%", "color": "#6baed6"},
                {"category": "Stronghold", "range": "D+20-30%", "color": "#3182bd"},
                {"category": "Dominant", "range": "D+30-40%", "color": "#08519c"},
                {"category": "Annihilation", "range": "D+40%+", "color": "#08306b"}
            ]
        },
        "office_types": ["Federal", "State", "Judicial", "Other"],
        "enhanced_features": [
            "Competitiveness categorization for each county",
            "Contest type classification (Federal/State/Judicial)",
            "Office ranking system for analysis prioritization",
            "Color coding compatible with political geography visualization"
        ]
    },
    "summary": {},
    "results_by_year": defaultdict(lambda: defaultdict(dict))
}

def get_competitiveness(margin_pct, winner):
    if margin_pct is None:
        return None
    if winner == 'REP':
        if margin_pct >= 40:
            return {"category": "Annihilation", "party": "Republican", "code": "R_ANNIHILATION", "color": "#67000d"}
        elif margin_pct >= 30:
            return {"category": "Dominant", "party": "Republican", "code": "R_DOMINANT", "color": "#a50f15"}
        elif margin_pct >= 20:
            return {"category": "Stronghold", "party": "Republican", "code": "R_STRONGHOLD", "color": "#cb181d"}
        elif margin_pct >= 10:
            return {"category": "Safe", "party": "Republican", "code": "R_SAFE", "color": "#ef3b2c"}
        elif margin_pct >= 5.5:
            return {"category": "Likely", "party": "Republican", "code": "R_LIKELY", "color": "#fb6a4a"}
        elif margin_pct >= 1:
            return {"category": "Lean", "party": "Republican", "code": "R_LEAN", "color": "#fcae91"}
        elif margin_pct >= 0.5:
            return {"category": "Tilt", "party": "Republican", "code": "R_TILT", "color": "#fee8c8"}
    elif winner == 'DEM':
        if margin_pct >= 40:
            return {"category": "Annihilation", "party": "Democratic", "code": "D_ANNIHILATION", "color": "#08306b"}
        elif margin_pct >= 30:
            return {"category": "Dominant", "party": "Democratic", "code": "D_DOMINANT", "color": "#08519c"}
        elif margin_pct >= 20:
            return {"category": "Stronghold", "party": "Democratic", "code": "D_STRONGHOLD", "color": "#3182bd"}
        elif margin_pct >= 10:
            return {"category": "Safe", "party": "Democratic", "code": "D_SAFE", "color": "#6baed6"}
        elif margin_pct >= 5.5:
            return {"category": "Likely", "party": "Democratic", "code": "D_LIKELY", "color": "#9ecae1"}
        elif margin_pct >= 1:
            return {"category": "Lean", "party": "Democratic", "code": "D_LEAN", "color": "#c6dbef"}
        elif margin_pct >= 0.5:
            return {"category": "Tilt", "party": "Democratic", "code": "D_TILT", "color": "#e1f5fe"}
    if margin_pct < 0.5:
        return {"category": "Tossup", "party": "Tossup", "code": "TOSSUP", "color": "#f7f7f7"}
    return None

def normalize_candidate_name(name):
    if not name:
        return ''
    name = name.replace('"', '').strip()
    # If name is in 'Last, First (Nickname)' format, convert to 'First Last'
    match = re.match(r'^(\w+),\s*([\w\-]+)(?:\s*\(([^)]+)\))?', name)
    if match:
        first = match.group(2)
        last = match.group(1)
        nickname = match.group(3)
        if nickname:
            name = f"{first} ({nickname}) {last}"
        else:
            name = f"{first} {last}"
    # Remove extra spaces and punctuation except for nickname
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'[.,()]', '', name)
    return name.strip()

# List all relevant CSVs
csv_files = [
    "20001107__mo__general__precinct.csv",
    "20021105__mo__general__precinct.csv",
    "20041102__mo__general__precinct.csv",
    "20061107__mo__general__precinct.csv",
    "20081104__mo__general__precinct.csv",
    "20101102__mo__general__precinct.csv",
    "20121106__mo__general__precinct.csv",
    "20141104__mo__general__precinct.csv",
    "20161108__mo__general__precinct.csv",
    "20181106__mo__general__precinct.csv",
    "20201103__mo__general__precinct.csv",
    "20241105__mo__general__precinct.csv"
]
all_years = set()
all_contests = set()
all_county_results = 0
results_by_year = defaultdict(lambda: defaultdict(dict))

for csv_file in csv_files:
    csv_path = os.path.join(DATA_DIR, csv_file)
    df = pd.read_csv(csv_path, dtype=str)
    
    # Normalize column names to lowercase for consistency
    df.columns = df.columns.str.lower()
    
    # Create 'candidate' column if it doesn't exist or is empty (combine first/last name)
    # Format: "FirstName LastName" (not "LastName FirstName")
    if 'candidate' not in df.columns or df['candidate'].fillna('').str.strip().eq('').all():
        if 'first_name' in df.columns and 'last_name' in df.columns:
            df['candidate'] = (df['first_name'].fillna('') + ' ' + df['last_name'].fillna('')).str.strip()
        elif 'first name' in df.columns and 'last name' in df.columns:
            df['candidate'] = (df['first name'].fillna('') + ' ' + df['last name'].fillna('')).str.strip()
        else:
            df['candidate'] = ''
    else:
        # Candidate column exists but may have some empty values - fill those from first/last name
        mask = df['candidate'].fillna('').str.strip().eq('')
        if mask.any():
            if 'first_name' in df.columns and 'last_name' in df.columns:
                df.loc[mask, 'candidate'] = (df.loc[mask, 'first_name'].fillna('') + ' ' + df.loc[mask, 'last_name'].fillna('')).str.strip()
            elif 'first name' in df.columns and 'last name' in df.columns:
                df.loc[mask, 'candidate'] = (df.loc[mask, 'first name'].fillna('') + ' ' + df.loc[mask, 'last name'].fillna('')).str.strip()
    
    # Include Presidential, US Senate, and statewide offices (Governor, Attorney General, etc.)
    include_keywords = ['President', 'Senator', 'Senate', 'Governor', 'Attorney General', 'Secretary of State', 'State Treasurer', 'State Auditor', 'Lieutenant Governor']
    exclude_keywords = ['State Senator', 'State Senate', 'US House', 'U.S. House', 'State Representative', 'State House']
    
    # Must contain at least one include keyword AND not contain any exclude keywords
    include_mask = df['office'].str.contains('|'.join(include_keywords), case=False, na=False)
    exclude_mask = df['office'].str.contains('|'.join(exclude_keywords), case=False, na=False)
    mask = include_mask & ~exclude_mask
    df_filtered = df[mask].copy() if 'office' in df.columns else df.copy()
    # Extract only the year (first 4 digits)
    year = csv_file[:4]
    all_years.add(year)
    
    # Manual party mappings for races where party data is missing in source files
    party_mappings = {
        '2018': {
            'Nicole Galloway': 'DEM',
            'Saundra McDowell': 'REP'
        }
    }
    
    # Apply party mappings if year and candidate match
    if year in party_mappings:
        for candidate_name, party in party_mappings[year].items():
            mask = df_filtered['candidate'].str.contains(candidate_name, case=False, na=False)
            df_filtered.loc[mask, 'party'] = party
    
    # Clean up candidate names (fix formatting issues)
    name_corrections = {
        'Jeremiah W Jay Nixon': 'Jay Nixon',
        'Jeremiah W. (Jay) Nixon': 'Jay Nixon',
        'Christopher Bond': 'Kit Bond',
        'Christopher S. Bond': 'Kit Bond'
    }
    
    for old_name, new_name in name_corrections.items():
        df_filtered.loc[df_filtered['candidate'] == old_name, 'candidate'] = new_name
    
    # Aggregate precinct-level files to county-level
    if 'precinct' in df_filtered.columns:
        # Fill NaN values before groupby
        df_filtered['party'] = df_filtered['party'].fillna('')
        df_filtered['candidate'] = df_filtered['candidate'].fillna('')
        
        # Normalize all county names to title case for consistency
        df_filtered['county'] = df_filtered['county'].str.title()
        
        # Remap Kansas City to Jackson BEFORE aggregation
        kc_count = df_filtered[df_filtered['county'].str.contains('Kansas City', case=False, na=False)].shape[0]
        if kc_count > 0:
            print(f"  Remapping {kc_count} Kansas City rows to Jackson in {year}")
        df_filtered.loc[df_filtered['county'].str.contains('Kansas City', case=False, na=False), 'county'] = 'Jackson'
        
        # Group by county, office, party, candidate and sum votes
        df_filtered.loc[:, 'votes'] = df_filtered['votes'].astype(float)
        df_filtered = df_filtered.groupby(['county', 'office', 'party', 'candidate'], as_index=False)['votes'].sum()
    if 'county' not in df_filtered.columns:
        continue
    for office in df_filtered['office'].unique():
        office_df = df_filtered[df_filtered['office'] == office].copy()
        
        # Fill NaN values before processing
        office_df['party'] = office_df['party'].fillna('')
        office_df['candidate'] = office_df['candidate'].fillna('')
        
        # Remap 'Kansas City' to 'Jackson' before processing
        office_df.loc[office_df['county'].str.upper().str.contains('KANSAS CITY', na=False), 'county'] = 'Jackson'
        
        # Convert votes to float before groupby
        office_df.loc[:, 'votes'] = office_df['votes'].astype(float)
        
        # Re-aggregate after remapping to combine Jackson + Kansas City
        office_df = office_df.groupby(['county', 'office', 'party', 'candidate'], as_index=False)['votes'].sum()
        
        for county in office_df['county'].unique():
            # Normal county logic
            official_county = get_official_county_name(county)
            if not official_county:
                continue
            county_df = office_df[office_df['county'] == county].copy()
            county_df['party'] = county_df['party'].fillna('')
            # Use contains for party matching
            dem_mask = county_df['party'].str.upper().str.contains('DEM')
            rep_mask = county_df['party'].str.upper().str.contains('REP')
            dem_votes = county_df[dem_mask]['votes'].astype(float).sum()
            rep_votes = county_df[rep_mask]['votes'].astype(float).sum()
            other_votes = county_df[~(dem_mask | rep_mask)]['votes'].astype(float).sum()
            total_votes = dem_votes + rep_votes + other_votes
            two_party_total = dem_votes + rep_votes
            margin = abs(rep_votes - dem_votes)
            # Calculate percentages based on total votes (not just two-party)
            dem_pct = round(dem_votes / total_votes * 100, 2) if total_votes > 0 else None
            rep_pct = round(rep_votes / total_votes * 100, 2) if total_votes > 0 else None
            # Calculate margin as percentage of two-party total
            margin_pct = round(margin / two_party_total * 100, 2) if two_party_total > 0 else None
            margin_pct_str = f"{margin_pct:.2f}" if margin_pct is not None else None
            winner = 'REP' if rep_votes > dem_votes else ('DEM' if dem_votes > rep_votes else 'TIE')
            # Candidate selection: filter out missing/empty candidate names
            dem_candidates = county_df[dem_mask & county_df['candidate'].notna() & (county_df['candidate'] != '')]
            if not dem_candidates.empty:
                dem_candidate = normalize_candidate_name(dem_candidates.sort_values('votes', ascending=False)['candidate'].iloc[0])
            else:
                dem_rows = county_df[county_df['party'].str.upper().str.contains('DEM') & county_df['candidate'].notna() & (county_df['candidate'] != '')]
                dem_candidate = normalize_candidate_name(dem_rows.sort_values('votes', ascending=False)['candidate'].iloc[0]) if not dem_rows.empty else ''
            rep_candidates = county_df[rep_mask & county_df['candidate'].notna() & (county_df['candidate'] != '')]
            if not rep_candidates.empty:
                rep_candidate = normalize_candidate_name(rep_candidates.sort_values('votes', ascending=False)['candidate'].iloc[0])
            else:
                rep_rows = county_df[county_df['party'].str.upper().str.contains('REP') & county_df['candidate'].notna() & (county_df['candidate'] != '')]
                rep_candidate = normalize_candidate_name(rep_rows.sort_values('votes', ascending=False)['candidate'].iloc[0]) if not rep_rows.empty else ''
            competitiveness = get_competitiveness(margin_pct, winner)
            all_parties = {}
            for party in county_df['party'].unique():
                party_votes = county_df[county_df['party'] == party]['votes'].astype(float).sum()
                all_parties[party.upper()] = int(party_votes)
            contest_id = f"{official_county}_{office.replace(' ', '_')}_{year}"
            all_contests.add(office)
            all_county_results += 1
            results_by_year[year][office][official_county] = {
                "county": official_county,
                "contest": office,
                "year": year,
                "dem_candidate": dem_candidate,
                "rep_candidate": rep_candidate,
                "dem_votes": int(dem_votes),
                "rep_votes": int(rep_votes),
                "dem_pct": dem_pct,
                "rep_pct": rep_pct,
                "other_votes": int(other_votes),
                "total_votes": int(total_votes),
                "two_party_total": int(two_party_total),
                "margin": int(margin) if margin is not None else None,
                "margin_pct": margin_pct_str,
                "winner": winner,
                "competitiveness": competitiveness,
                "all_parties": all_parties
            }

output_json["summary"] = {
    "total_years": len(all_years),
    "total_contests": len(all_contests),
    "total_county_results": all_county_results,
    "years_covered": sorted(list(all_years))
}
# Sort results_by_year chronologically
output_json["results_by_year"] = {year: results_by_year[year] for year in sorted(results_by_year.keys())}

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(output_json, f, ensure_ascii=False, indent=2)

print(f"County-aggregated Ballotpedia-style JSON created: {OUTPUT_PATH}")
