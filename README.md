# Canonical Field Resolver

A geospatial resolver engine in Python that reconciles field boundaries from multiple data sources (e.g., ag retailers, OEMs, growers) into a persistent, canonical field ID.

## Features

This engine handles:

- **Spatial similarity matching** - Compare and match field boundaries using geometric operations
- **Field versioning** - Track changes to field boundaries over time and seasons
- **Seasonal splits and merges** - Handle complex field transformations with lineage tracking
- **API access** - RESTful API for field resolution and retrieval
- **Real-world geospatial formats** - Support for shapefiles, GeoJSON, and other standard formats

## Tech Stack

- **Language**: Python 3.11+
- **Core Libraries**:
  - `shapely` for geometric operations
  - `geopandas` for spatial dataframes
  - `uuid` for ID generation
  - `FastAPI` for microservice API
  - `PostGIS` (optional) for persistent backend
- **File Formats**: GeoJSON, Shapefile, CSV

## Project Structure

```
canonical_field_resolver/
│
├── resolver/                  # Core logic
│   ├── __init__.py
│   ├── matcher.py             # IoU matching, canonical assignment
│   ├── versioning.py          # Version control for fields
│   ├── lineage.py             # Splits/merges tracking
│   └── logger.py              # Logging configuration
│
├── api/                       # FastAPI app
│   ├── main.py
│   ├── routes.py
│   └── models.py
│
├── data/                      # Sample inputs (GeoJSON, shapefiles)
│
├── tests/                     # Unit tests
│   ├── test_matcher.py
│   ├── test_versioning.py
│   └── test_recording_lineage.py
│
├── requirements.txt
└── README.md
```

## Development Modules

The project is developed in progressive steps:

### Step 1: Field Matching Engine (Core Logic)
- Load polygon data from memory
- Compare spatial overlap (IoU)
- Assign or match to canonical ID
- Store canonical fields in memory

### Step 2: Versioning & Field History
- Track changes over time
- Store field versions per season
- Handle slight boundary adjustments

### Step 3: Handling Splits and Merges
- Detect and record splits (1 → many) or merges (many → 1)
- Add parent-child lineage tracking

### Step 4: Input from Real Data (GeoJSON / Shapefile)
- Read GeoJSON and shapefiles using geopandas
- Convert and standardize inputs for matching

### Step 5: Build FastAPI Microservice
Expose API to:
- Submit new field polygons
- Retrieve canonical ID and linked sources
- View version lineage
- Return JSON responses

### Step 6: Data Persistence Layer (Optional)
- Store canonical fields and source metadata in PostGIS or GeoParquet
- Use spatial indexes for efficient lookups

### Step 7: CLI + UI Tools (Optional)
- Create command-line tools for batch processing
- Build simple Streamlit UI to visualize fields and matches

## Getting Started

### Prerequisites

- Python 3.11+
- Required packages (see `requirements.txt`)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd canonical_field_resolver

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test files
pytest tests/test_matcher.py
pytest tests/test_versioning.py
pytest tests/test_recording_lineage.py
```

## Usage

### Basic Field Resolution

```python
from resolver import matcher

# Load a GeoJSON feature
geojson_feature = {
    "type": "Feature", 
    "geometry": {
        "type": "Polygon",
        "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]
    }
}

# Resolve to canonical field ID
field_id = matcher.resolve_field(geojson_feature)
print(f"Canonical Field ID: {field_id}")
```

### API Usage

Once the FastAPI service is running:

```bash
# Submit a new field
curl -X POST "http://localhost:8000/fields" \
  -H "Content-Type: application/json" \
  -d '{"type": "Feature", "geometry": {...}}'

# Get field information
curl "http://localhost:8000/fields/{field_id}"
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
