# Content-Automation (W.I.P.)

A comprehensive toolkit for automating crossword puzzle generation and management.

## Overview

This project provides tools for generating crossword puzzles and managing clue content. It consists of two main components:

1. **Grid Generator** - Creates filled crossword grids using constraint satisfaction algorithms
2. **Clue TSV Generator** - Processes grid files to extract words and generate TSV files for clue management

## Components

### Grid Generator

The grid generator uses a constraint satisfaction algorithm to fill crossword grids with words. It features:

- Bitmap-based domain representation for efficient constraint propagation
- Arc consistency enforcement (AC-3 algorithm)
- Backtracking search with interleaved constraint propagation
- Support for multiple grid layouts
- Word grouping to ensure thematic consistency

#### Key Files:
- `grid_gen_bitmaps/ccw_csp.py` - Core constraint satisfaction solver
- `grid_gen_bitmaps/crossowrd.py` - Crossword representation
- `grid_gen_bitmaps/bitmap_array.py` - Efficient bitmap operations
- `grid_gen_bitmaps/constant.py` - Configuration constants

### Clue TSV Generator

The clue TSV generator extracts words from filled grid files and creates a structured TSV file for further clue management.

#### Key Files:
- `clue_tsv_generator/clue_tsv_generator.py` - Extracts words from grid files and generates TSV

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/content-automation.git
cd content-automation
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Generating Crossword Grids

The grid generator is implemented as a Streamlit application:

```bash
cd grid_gen_bitmaps
streamlit run ccw_csp.py
```

This will open a web interface where you can:
1. Upload a previous content TSV file
2. Select the number of puzzles to generate
3. Generate and download crossword grids

### Generating Clue TSV Files

To generate a TSV file from filled grid files:

```bash
cd clue_tsv_generator
python clue_tsv_generator.py
```

This will:
1. Read all grid files from the `grids` directory
2. Extract words, positions, and directions
3. Generate a `grid_clues.tsv` file with the following columns:
   - puzzleId
   - word
   - row
   - column
   - direction
   - clueContent (empty, to be filled later)

## Directory Structure

```
Content-Automation/
├── .venv/                  # Virtual environment (gitignored)
├── clue_tsv_generator/     # TSV generation tools
│   ├── clue_tsv_generator.py
│   └── grids/              # Directory containing filled grid files
├── grid_gen_bitmaps/       # Grid generation tools
│   ├── bitmap_array.py
│   ├── ccw_csp.py
│   ├── constant.py
│   ├── crossowrd.py
│   └── grid_layouts/       # Grid templates
├── outputs/                # Generated grid files
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

## Technical Details

### Constraint Satisfaction Algorithm

The crossword grid generator uses:

1. **Variable Selection**: Chooses variables (words) with minimum remaining values
2. **Value Ordering**: Prioritizes words that are likely to be compatible with neighbors
3. **Constraint Propagation**: Uses AC-3 algorithm to enforce arc consistency
4. **Backtracking Search**: Recursively assigns values and backtracks when constraints are violated

### Word Selection

Words are selected based on:
- Length constraints (must fit in the grid)
- Overlap constraints (must share letters at intersections)
- Thematic grouping (words from the same group may be preferred)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.