# Decision Intelligence Evolution Analysis

An analytical study tracking the evolution of "Decision Intelligence" as a research topic across academic literature from 1965 to 2026.

## Overview

This analysis examines how the term "Decision Intelligence" has emerged and evolved in scholarly publications by integrating data from three major sources: Scopus, ScienceDirect, and preprint repositories (Arxiv, SSRN, TechRxiv).

## Key Findings

### Temporal Evolution

The analysis reveals the publication trajectory of "Decision Intelligence" research over six decades:

- **First Publication:** 1965
- **Time Span:** 1965-2026 (61 years)
- **Recent Growth:** Significant acceleration in the last 5 years
- **Peak Year:** [See temporal analysis charts in `output/`]

### Source Distribution

Publications are distributed across three primary sources:

1. **Scopus Database:** Comprehensive multidisciplinary coverage
2. **ScienceDirect:** Elsevier's full-text database
3. **Preprints:** Early-stage research from Arxiv, SSRN, and TechRxiv

**Note:** Scopus and ScienceDirect data were deduplicated using DOI-based matching to avoid double-counting publications indexed in both databases.

### Document Type Analysis

The study focuses on three scholarly publication types:

- **Articles:** Peer-reviewed research papers
- **Reviews:** Comprehensive literature reviews
- **Conference Papers:** Conference proceedings and presentations

**Filtering Strategy:** Scopus and ScienceDirect records were filtered to include only these three types, while all preprints were retained to capture emerging research trends.

### Visualizations

All analytical outputs are available in the `output/` directory:

1. **Temporal Trends** (`output/temporal_evolution.png`)
   - Publications per year (1965-2026)
   - Cumulative growth curve
   - Year-over-year growth rates

2. **Source Distribution** (`output/source_distribution.png`)
   - Breakdown by database (Scopus/ScienceDirect/Preprints)
   - Overlap analysis between Scopus and ScienceDirect

3. **Document Type Distribution** (`output/document_type_distribution.png`)
   - Article vs. Review vs. Conference Paper proportions
   - Evolution of document types over time

4. **Integrated Timeline** (`output/integrated_timeline.png`)
   - Stacked visualization showing all sources and types over time
   - Identification of key growth periods

## Methodology

### Data Collection

**Search Term:** `"Decision Intelligence"` (applied consistently across all sources)

**Sources:**
1. **Scopus:** CSV export with full metadata
2. **ScienceDirect:** Three separate BibTeX exports (articles, reviews, conference papers) to overcome web application export limitations
3. **Preprints:** CSV extracted using LLM assistance due to Scopus preprint export limitations

### Data Processing Pipeline

```
1. Load Data
   ├── Scopus CSV
   ├── ScienceDirect BibTeX (3 files)
   └── Preprints CSV

2. Source Flagging
   └── Tag each record with origin

3. Document Type Mapping
   └── Extract types from ScienceDirect filenames

4. Deduplication (Scopus ↔ ScienceDirect)
   └── DOI-based matching and removal

5. Filtering
   ├── Scopus: Keep Article/Review/Conference only
   ├── ScienceDirect: Keep Article/Review/Conference only
   └── Preprints: Keep all

6. Integration
   └── Merge filtered Scopus + ScienceDirect + all Preprints

7. Analysis & Visualization
   └── Temporal trends, distributions, statistics

8. Export
   └── Integrated dataset (CSV)
```

### Deduplication Strategy

**Challenge:** Publications indexed in both Scopus and ScienceDirect create duplicates.

**Solution:** 
- DOI-based matching identifies overlapping records
- Scopus records retained (more complete metadata)
- ScienceDirect duplicates removed
- ScienceDirect document type classification preserved in Scopus records

**Result:** Clean dataset with no double-counting

## Data Limitations and Compliance

### Elsevier Terms of Use

**Important:** Data from Elsevier sources (Scopus and ScienceDirect) **cannot be redistributed** according to their Terms of Use. 

The `data/` directory is excluded from version control. To replicate this analysis:
1. Obtain institutional access to Scopus and ScienceDirect
2. Perform searches using the term "Decision Intelligence"
3. Export data following the methodology described
4. Place files in the `data/` directory

### Known Limitations

1. **ScienceDirect Export:** Web application limits required splitting exports by document type
2. **Preprint Data:** Manual extraction using LLM due to Scopus export constraints
3. **Coverage:** Limited to publications explicitly using "Decision Intelligence" term
4. **Language:** Primarily English-language publications
5. **Access Date:** Data collected May 2026

## Repository Structure

```
citrus-decision-intelligence/
├── data/                          # Source data (not in git)
│   ├── lexical-DI-scopus_export_*.csv
│   ├── lexical-DI-article-*.bib
│   ├── lexical-DI-review-*.bib
│   ├── lexical-DI-conference-*.bib
│   └── preprints.csv
├── output/                        # Analysis outputs
│   ├── temporal_evolution.png
│   ├── source_distribution.png
│   ├── document_type_distribution.png
│   └── integrated_timeline.png
├── decision_intelligence_evolution.ipynb  # Analysis notebook
├── decision_intelligence_integrated.csv   # Final dataset
├── .gitignore
├── LICENSE
├── README.md                      # This file
└── INSTALL.md                     # Replication instructions
```

## Outputs

### Generated Files

1. **`decision_intelligence_integrated.csv`**
   - Deduplicated and integrated dataset
   - All sources combined
   - Ready for further analysis

2. **Visualization Charts** (in `output/` directory)
   - Publication trends over time
   - Source and document type distributions
   - Cumulative growth analysis

### Summary Statistics

Key metrics from the analysis:

- **Total Unique Publications:** [See notebook output]
- **Scopus Records:** [Filtered to Article/Review/Conference]
- **ScienceDirect Records:** [Unique, filtered records]
- **Preprints:** [All preprints included]
- **Duplicates Removed:** [DOI-based deduplication count]
- **Time Span:** 1965-2026
- **Peak Publication Year:** [Year with most publications]
- **5-Year Growth Rate:** [Recent trend]

## Citation

If you use this analysis or methodology, please cite appropriately and ensure compliance with data provider terms of use.

## License

See [LICENSE](LICENSE) file for details.

## Replication

For detailed instructions on replicating this analysis, see [INSTALL.md](INSTALL.md).

---

**Research Purpose:** This analysis is conducted for academic research to understand the emergence and evolution of "Decision Intelligence" as a scholarly concept.

**Data Compliance:** Users must obtain their own institutional access to Scopus and ScienceDirect and comply with all applicable terms of service.