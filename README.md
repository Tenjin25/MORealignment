# Missouri Electoral Realignments Interactive Map

An interactive visualization of Missouri's electoral trends from 2000-2024, showing county-level results for Presidential and US Senate races. This project analyzes partisan competitiveness and geographic voting patterns across Missouri's 115 counties.

## Live Demo

[View the Interactive Map](https://tenjin25.github.io/MORealignment/)

## Features

### Interactive Map
- **County-level visualization** with color-coded competitiveness ratings
- **Click counties** to view detailed results and vote breakdowns
- **Hover tooltips** showing quick statistics
- **Contest selection** dropdown to switch between different elections (2000-2024)
- **Statewide results** panel showing aggregated state totals and margins

### Competitiveness Analysis
Nine-tier competitiveness scale from "Annihilation" to "Tossup":
- **Annihilation** (40%+ margin)
- **Dominant** (30-40% margin)
- **Stronghold** (20-30% margin)
- **Safe** (10-20% margin)
- **Likely** (5.5-10% margin)
- **Lean** (1-5.5% margin)
- **Tilt** (0.5-1% margin)
- **Tossup** (<0.5% margin)

### Data Coverage
- **Years**: 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2016, 2018, 2020, 2024
- **Contests**: Presidential elections and US Senate races
- **Geography**: All 115 Missouri counties (114 counties + St. Louis City)

## Key Findings

### Jackson County - Kansas City's Urban Core
- Consistently Democratic stronghold containing Kansas City proper
- 2020: Biden 58.49% vs Trump 38.27%
- 2024: Harris 58.71% vs Trump 40.49%
- **Trend**: Strengthening Democratic advantage (+21.84% in 2024)

### St. Louis County - Suburban Bellwether
- Shifted from swing county to Democratic lean
- 2020: Biden 58.47% vs Trump 39.81%
- 2024: Harris 57.68% vs Trump 40.77%
- **Trend**: Stable Democratic performance in suburban areas

### Greene County - Springfield Metro
- Republican stronghold with consistent GOP advantage
- 2020: Trump 59.08% vs Biden 38.94%
- 2024: Trump 60.86% vs Harris 37.07%
- **Trend**: Strengthening Republican dominance

### Southeast Missouri (Bootheel)
- Rural counties showing dramatic Republican gains
- Counties like Pemiscot, Dunklin shifting 20-30 points toward GOP
- **Trend**: Accelerating rural polarization

### Statewide Pattern
- Missouri has trended increasingly Republican since 2008
- Rural areas shifting dramatically toward GOP
- Urban cores (KC, STL) becoming more Democratic
- Suburban counties remain contested but leaning Republican

## Technical Details

### Data Sources
- **Precinct-level results**: Missouri Secretary of State election data (2000-2024)
- **County boundaries**: US Census Bureau TIGER/Line shapefiles (2020)
- **Aggregation**: Custom Python scripts for data processing

### Special Handling

#### Kansas City / Jackson County
Kansas City appears as a separate entity in precinct files but is part of Jackson County. The aggregation script:
1. Identifies all "Kansas City" rows in precinct data
2. Remaps them to "Jackson" before aggregation
3. Combines vote totals for unified Jackson County results
4. Applies across all years (2000-2024)

#### St. Louis City vs County
St. Louis City is an independent jurisdiction separate from St. Louis County:
- **GeoJSON**: "St. Louis city" (lowercase) vs "St. Louis County"
- **Election data**: "St. Louis City" (uppercase) vs "St. Louis County"
- Lookup logic handles case normalization for proper matching

### Technology Stack
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Mapping**: Mapbox GL JS
- **Data Processing**: Python 3.13+ with pandas
- **Version Control**: Git/GitHub
- **Hosting**: GitHub Pages

## Project Structure

```
MORealignments/
├── index.html                 # Main interactive map page
├── Data/
│   ├── mo_county_aggregated_results.json  # Processed election data
│   ├── mo_county_fips.csv                 # County FIPS codes
│   └── *__mo__general__precinct.csv       # Raw precinct-level data (2000-2024)
├── VTDs/
│   └── tl_2020_29_county20.geojson       # Missouri county boundaries
├── scripts/
│   ├── county_aggregate_results.py        # Main aggregation script
│   ├── download_mo_vtds.py               # Download county shapefiles
│   └── join_precinct_data.py             # Data joining utilities
├── styles/
│   └── map.css                           # Map styling
└── README.md
```

## Running Locally

### Prerequisites
- Python 3.13 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Tenjin25/MORealignment.git
   cd MORealignment
   ```

2. **Install Python dependencies**
   ```bash
   pip install pandas
   ```

3. **Run the map**
   - Open `index.html` in a web browser
   - Or use a local web server:
     ```bash
     python -m http.server 8000
     ```
     Then navigate to `http://localhost:8000`

### Regenerating Data

To update or regenerate the aggregated election data:

```bash
python scripts/county_aggregate_results.py
```

This script:
- Reads all precinct-level CSV files from `Data/` directory
- Filters to Presidential and US Senate races only
- Normalizes county names to title case
- Remaps Kansas City to Jackson County
- Aggregates votes by county, office, and party
- Calculates competitiveness metrics
- Outputs to `Data/mo_county_aggregated_results.json`

## Data Processing Pipeline

### 1. Column Normalization
- Converts all column names to lowercase
- Handles variations: "candidate" vs "first_name"/"last_name" vs "first name"/"last name"

### 2. Candidate Name Handling
- Detects empty candidate columns
- Fills from last_name + first_name when needed
- Proper name ordering (e.g., "Al Gore Joe Lieberman")

### 3. County Name Normalization
- Converts all county names to title case for consistency
- Handles ALLCAPS (2000-2008 files) vs Title Case (2012-2024 files)

### 4. Kansas City Aggregation
- Identifies rows where county contains "Kansas City"
- Remaps to "Jackson" before groupby operation
- Ensures votes combine correctly across all years

### 5. Contest Filtering
- Include: Presidential and US Senate races
- Exclude: US House, State House, State Senate, Propositions

### 6. Competitiveness Calculation
- Calculates two-party vote share and margin
- Assigns competitiveness tier based on margin percentage
- Determines winner and color coding

## Map Configuration

### Contest Dropdown
Contests are organized by office type:
- **US President**: Presidential elections (2000, 2004, 2008, 2012, 2016, 2020, 2024)
- **US Senate**: Senate races (2000, 2002, 2004, 2006, 2010, 2012, 2016, 2018, 2024)

### Color Scheme
- **Democratic**: Shades of blue (lighter = closer race)
- **Republican**: Shades of red (lighter = closer race)
- **Intensity**: Darker colors = larger margins

### Map Controls
- **Zoom**: Mouse wheel or +/- buttons
- **Pan**: Click and drag
- **County select**: Click any county
- **Contest switch**: Use dropdown menu

## Known Issues & Limitations

### Data Gaps
- 2014: No statewide races (only gubernatorial in off-year)
- 2022: No precinct data available yet
- State House/Senate: Excluded due to complexity of district mapping

### Browser Compatibility
- Requires modern browser with ES6 support
- Mapbox GL JS requires WebGL support
- Best performance on Chrome/Edge

### Performance
- Initial load may take 2-3 seconds for GeoJSON parsing
- 115 counties with 11 years of data = ~1,265 county-contest combinations
- Color updates are throttled to 300ms to prevent lag

## Future Enhancements

### Planned Features
- [ ] Add gubernatorial races
- [ ] Include 2022 data when available
- [ ] Time-series animation showing trends over time
- [ ] Export functionality for charts/maps
- [ ] Mobile-responsive design improvements

### Data Expansions
- [ ] Add demographic overlays (Census data)
- [ ] Include third-party candidates
- [ ] Add voter turnout statistics
- [ ] Historical comparison tools

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Areas for Contribution
- Adding historical election data (pre-2000)
- Improving mobile responsiveness
- Adding new visualizations
- Enhancing competitiveness analysis
- Documentation improvements

## License

This project is open source and available for educational and research purposes.

## Credits

### Data Sources
- **Missouri Secretary of State**: Election results
- **US Census Bureau**: County boundary shapefiles
- **OpenElections Project**: Data format inspiration

### Built With
- [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/)
- [Pandas](https://pandas.pydata.org/)
- [Python](https://www.python.org/)

## Contact

For questions or feedback:
- **GitHub**: [@Tenjin25](https://github.com/Tenjin25)
- **Repository**: [MORealignment](https://github.com/Tenjin25/MORealignment)

---

**Note**: This is an educational project analyzing publicly available election data. All results are sourced from official Missouri Secretary of State records.