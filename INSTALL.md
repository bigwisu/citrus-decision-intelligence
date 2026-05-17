# Installation and Replication Guide

This guide provides step-by-step instructions for replicating the Decision Intelligence evolution analysis.

## Prerequisites

### System Requirements
- Python 3.14 or higher
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space

### Required Access
- **Institutional access** to Scopus database
- **Institutional access** to ScienceDirect
- Internet connection for preprint repository searches

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd citrus-decision-intelligence
```

### 2. Set Up Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install jupyter pandas numpy matplotlib seaborn scikit-learn scipy
```

### 4. Register Jupyter Kernel

```bash
python -m ipykernel install --user --name=venv --display-name="Python (venv)"
```

### 5. Verify Installation

```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(jupyter|pandas|numpy|matplotlib|seaborn|scikit-learn|scipy)"
```

## Data Collection

### Step 1: Scopus Export

1. **Access Scopus:**
   - Navigate to https://www.scopus.com/
   - Log in with institutional credentials

2. **Perform Search:**
   - Search query: `"Decision Intelligence"`
   - Search in: Title, Abstract, Keywords
   - No date restrictions

3. **Export Data:**
   - Select all results
   - Click "Export"
   - Format: CSV
   - Include all available fields
   - Save as: `data/lexical-DI-scopus_export_[date]_[id].csv`

4. **Required Fields:**
   - Authors, Author full names, Author(s) ID
   - Title, Year, Source title
   - Volume, Issue, Page start, Page end
   - Abstract, Author Keywords, Index Keywords
   - Document Type, DOI, Link
   - Cited by, EID

### Step 2: ScienceDirect Export

**Important:** Due to ScienceDirect web application limitations, you must export data in **three separate batches** by document type.

#### Export 1: Articles

1. **Access ScienceDirect:**
   - Navigate to https://www.sciencedirect.com/
   - Log in with institutional credentials

2. **Search and Filter:**
   - Search query: `"Decision Intelligence"`
   - Filter by: **Article** document type only

3. **Export:**
   - Select all article results
   - Export format: BibTeX
   - Save as: `data/lexical-DI-article-1-ScienceDirect_citations_[timestamp].bib`

4. **Note:** If articles exceed export limit, create multiple files:
   - `lexical-DI-article-1-ScienceDirect_citations_[timestamp].bib`
   - `lexical-DI-article-2-ScienceDirect_citations_[timestamp].bib`
   - `lexical-DI-article-3-ScienceDirect_citations_[timestamp].bib`

#### Export 2: Reviews

1. **Search and Filter:**
   - Search query: `"Decision Intelligence"`
   - Filter by: **Review** document type only

2. **Export:**
   - Select all review results
   - Export format: BibTeX
   - Save as: `data/lexical-DI-review-ScienceDirect_citations_[timestamp].bib`

#### Export 3: Conference Papers

1. **Search and Filter:**
   - Search query: `"Decision Intelligence"`
   - Filter by: **Conference** document type only

2. **Export:**
   - Select all conference results
   - Export format: BibTeX
   - Save as: `data/lexical-DI-conference-ScienceDirect_citations_[timestamp].bib`

### Step 3: Preprints Collection

**Challenge:** Scopus preprint export has limitations that prevent direct CSV export.

**Solution:** Use LLM assistance to extract and structure preprint data.

#### Manual Method:

1. **Search Preprint Repositories:**
   - Arxiv: https://arxiv.org/ (search: "Decision Intelligence")
   - SSRN: https://www.ssrn.com/ (search: "Decision Intelligence")
   - TechRxiv: https://www.techrxiv.org/ (search: "Decision Intelligence")

2. **Extract Data:**
   - For each preprint, collect:
     - Title
     - Authors
     - Year
     - Repository name
     - Abstract

3. **Create CSV:**
   - Create file: `data/preprints.csv`
   - Columns: `Title,Authors,Year,Repository,Abstract`
   - Populate with collected data

#### LLM-Assisted Method:

1. **Collect Search Results:**
   - Copy search results from each repository
   - Include all metadata visible

2. **Use LLM to Structure:**
   - Prompt: "Extract the following fields from these preprint search results into CSV format: Title, Authors, Year, Repository, Abstract"
   - Provide search results text
   - Review and validate output

3. **Save Output:**
   - Save as: `data/preprints.csv`
   - Verify format matches expected structure

## Directory Structure Setup

Ensure your `data/` directory contains:

```
data/
├── lexical-DI-scopus_export_May 17-2026_[id].csv
├── lexical-DI-article-1-ScienceDirect_citations_[timestamp].bib
├── lexical-DI-article-2-ScienceDirect_citations_[timestamp].bib  (if needed)
├── lexical-DI-article-3-ScienceDirect_citations_[timestamp].bib  (if needed)
├── lexical-DI-review-ScienceDirect_citations_[timestamp].bib
├── lexical-DI-conference-ScienceDirect_citations_[timestamp].bib
└── preprints.csv
```

## Running the Analysis

### 1. Start Jupyter

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Launch Jupyter Lab
jupyter lab

# Or launch Jupyter Notebook
jupyter notebook
```

### 2. Open Analysis Notebook

- Navigate to `decision_intelligence_evolution.ipynb`
- Select kernel: **Python (venv)**

### 3. Execute Analysis

- Run all cells sequentially (Cell → Run All)
- Or run cells individually to inspect each step

### 4. Review Outputs

The notebook will generate:
- Visualization charts (displayed inline)
- `decision_intelligence_integrated.csv` (final dataset)
- Summary statistics (printed output)

## Troubleshooting

### Common Issues

#### 1. Kernel Not Found
```bash
# Re-register the kernel
python -m ipykernel install --user --name=venv --display-name="Python (venv)"
```

#### 2. Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install jupyter pandas numpy matplotlib seaborn scikit-learn scipy
```

#### 3. Data Files Not Found
- Verify files are in `data/` directory
- Check file naming matches expected patterns
- Ensure file extensions are correct (.csv, .bib)

#### 4. BibTeX Parsing Errors
- Verify BibTeX files are valid
- Check for special characters in abstracts
- Ensure files are UTF-8 encoded

#### 5. Memory Issues
- Process data in smaller batches
- Increase system RAM
- Close other applications

### File Naming Conventions

The notebook uses glob patterns to find files:
- Scopus: `*scopus*.csv`
- ScienceDirect: `*ScienceDirect*.bib`
- Preprints: `preprints.csv` (exact name)

Ensure your files match these patterns.

## Validation

### Data Quality Checks

After loading data, verify:

1. **Record Counts:**
   - Scopus: Should match your export
   - ScienceDirect: Sum of all BibTeX files
   - Preprints: Count in CSV

2. **Required Fields:**
   - All records have titles
   - Year values are numeric
   - DOIs present (where applicable)

3. **Deduplication:**
   - Check overlap count between Scopus and ScienceDirect
   - Verify duplicates are removed

4. **Filtering:**
   - Confirm only Article/Review/Conference from Scopus/SD
   - Verify all preprints retained

## Output Directory

Create an `output/` directory for saving visualizations:

```bash
mkdir output
```

The notebook will save charts to this directory (if configured).

## Updates and Maintenance

### Updating Data

To refresh the analysis with new data:

1. Re-export from Scopus and ScienceDirect
2. Replace files in `data/` directory
3. Re-run notebook

### Updating Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Update all packages
pip install --upgrade jupyter pandas numpy matplotlib seaborn scikit-learn scipy
```

## Support

For issues or questions:
1. Check this installation guide
2. Review notebook comments
3. Verify data file formats
4. Open an issue in the repository

## License and Compliance

**Important:** 
- Data from Elsevier (Scopus, ScienceDirect) is subject to their Terms of Use
- Do not redistribute Elsevier data
- Obtain your own institutional access
- Use data only for permitted research purposes

---

**Last Updated:** May 2026