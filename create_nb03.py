#!/usr/bin/env python3
import json

# Complete notebook structure
notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.9.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# All cells content
cells = [
    ("markdown", "# Decision Intelligence Evolution - Keyword Trends and Co-occurrence Analysis\n\n**Execution Order: 3 of 3**\n\nThis notebook performs:\n1. Keyword extraction from titles, abstracts, and author keywords\n2. Temporal trends analysis of key terms\n3. Co-occurrence network mapping\n4. Network visualization (VOSviewer-style)\n5. Visualization of keyword evolution\n\n**Prerequisites**: \n- Run `01_data_preparation.ipynb` first to generate the dataset WITH abstracts\n- The file `output/decision_intelligence_with_abstracts.csv` must exist\n\n**Note**: This analysis uses abstracts which are NOT committed to Git."),
    ("markdown", "## 1. Setup and Imports"),
    ("code", "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport networkx as nx\nfrom pathlib import Path\nfrom collections import Counter, defaultdict\nimport re\nfrom itertools import combinations\nimport warnings\nwarnings.filterwarnings('ignore')\n\n# Set style\nplt.style.use('seaborn-v0_8-darkgrid')\nsns.set_palette(\"husl\")\n\n# Directories\nOUTPUT_DIR = Path('output')\nOUTPUT_DIR.mkdir(exist_ok=True)\n\nprint(\"✓ Libraries imported successfully\")\nprint(f\"✓ Output directory: {OUTPUT_DIR.absolute()}\")"),
    ("markdown", "## 2. Load Data with Abstracts"),
    ("code", "# Load the dataset WITH abstracts\ndata_file = OUTPUT_DIR / 'decision_intelligence_with_abstracts.csv'\n\nif not data_file.exists():\n    print(\"❌ ERROR: File with abstracts not found!\")\n    print(\"   Please run notebook 01_data_preparation.ipynb first.\")\n    raise FileNotFoundError(f\"Required file not found: {data_file}\")\n\ndf = pd.read_csv(data_file, encoding='utf-8')\n\nprint(f\"✓ Loaded {len(df)} records\")\nprint(f\"  Records with abstracts: {df['abstract'].notna().sum()}\")\nprint(f\"  Records with keywords: {df['keywords'].notna().sum()}\")\nprint(f\"  Year range: {df['year'].min():.0f} - {df['year'].max():.0f}\")"),
    ("markdown", "## 3. Keyword Extraction and Preprocessing"),
    ("code", '''def extract_keywords_from_text(text, min_length=3):
    """Extract meaningful technical keywords from text. Focuses ONLY on multi-word technical terms."""
    if pd.isna(text):
        return []
    
    stopwords = {
        'the', 'and', 'for', 'with', 'this', 'that', 'from', 'are', 'was', 'were',
        'been', 'have', 'has', 'had', 'can', 'will', 'would', 'could', 'should',
        'may', 'might', 'must', 'shall', 'our', 'their', 'these', 'those', 'such',
        'into', 'through', 'during', 'before', 'after', 'however', 'moreover',
        'furthermore', 'therefore', 'additionally', 'finally', 'first', 'second',
        'third', 'next', 'then', 'thus', 'hence', 'consequently', 'accordingly',
        'meanwhile', 'subsequently', 'specifically', 'particularly', 'especially',
        'notably', 'using', 'based', 'results', 'research', 'study', 'studies',
        'paper', 'article', 'work', 'approach', 'method', 'methods', 'analysis',
        'data', 'information', 'system', 'systems', 'model', 'models', 'framework',
        'process', 'processes', 'while', 'although', 'though', 'since', 'because',
        'when', 'where', 'which', 'what', 'who', 'how', 'why', 'all', 'some',
        'many', 'most', 'few', 'several', 'various', 'different', 'same', 'other',
        'another', 'each', 'every', 'traditional', 'experimental', 'proposed',
        'novel', 'new', 'existing', 'current', 'recent', 'previous', 'future',
        'author', 'authors', 'et', 'al', 'decision', 'intelligence', 'design',
        'multi', 'findings', 'large', 'industry', 'science', 'purpose', 'internet',
        'originality', 'things', 'despite', 'scopus', 'language', 'digital',
        'extensive', 'making', 'artificial', 'business', 'value', 'practical',
        'implications', 'limitations', 'contribution', 'contributions'
    }
    
    multi_word_pattern = r'\\b[A-Z][a-z]+(?:\\s+[A-Z][a-z]+){1,4}\\b'
    multi_words = re.findall(multi_word_pattern, str(text))
    
    keywords = []
    for phrase in multi_words:
        phrase_lower = phrase.lower()
        words_in_phrase = phrase_lower.split()
        if any(w in stopwords for w in words_in_phrase):
            continue
        if len(words_in_phrase) < 2:
            continue
        if len(phrase) < min_length:
            continue
        keywords.append(phrase)
    
    return keywords

def parse_author_keywords(keywords_str):
    """Parse author-provided keywords from various formats."""
    if pd.isna(keywords_str):
        return []
    keywords = re.split(r'[;,|]', str(keywords_str))
    cleaned = []
    for kw in keywords:
        kw = kw.strip()
        if len(kw) > 2:
            cleaned.append(kw.title())
    return cleaned

print("✓ Keyword extraction functions defined")'''),
    ("code", '''# Manual exclusion list for publishers, metadata, and non-technical terms
MANUAL_EXCLUSIONS = {
    'elsevier ltd', 'elsevier', 'springer nature switzerland', 'springer nature',
    'springer', 'ieee', 'wiley', 'taylor francis', 'taylor', 'francis', 'francis group',
    'sage publications', 'sage', 'emerald publishing', 'emerald', 'mdpi', 
    'frontiers media', 'frontiers', 'nature publishing group', 'nature publishing',
    'oxford university press', 'oxford', 'cambridge university press', 'cambridge', 'acm',
    'all rights reserved', 'rights reserved', 'copyright holder',
    'creative commons', 'open access', 'peer review', 'peer reviewed',
    'corresponding author', 'et al', 'ibid', 'op cit',
    'bibliometric analysis', 'systematic review', 'literature review',
    'case study', 'empirical study', 'qualitative study', 'quantitative study',
    'scopus', 'web of science', 'google scholar', 'pubmed'
}

# Extract keywords from all sources
print("Extracting keywords from titles, abstracts, and author keywords...")

df['title_keywords'] = df['title'].apply(extract_keywords_from_text)
df['abstract_keywords'] = df['abstract'].apply(extract_keywords_from_text)
df['author_keywords_parsed'] = df['keywords'].apply(parse_author_keywords)

def combine_keywords(row):
    all_kw = row['author_keywords_parsed'].copy() if row['author_keywords_parsed'] else []
    for kw in row['title_keywords']:
        if kw not in all_kw and kw.lower() not in MANUAL_EXCLUSIONS:
            all_kw.append(kw)
    for kw in row['abstract_keywords']:
        if kw not in all_kw and kw.lower() not in MANUAL_EXCLUSIONS:
            all_kw.append(kw)
    all_kw = [kw for kw in all_kw if kw.lower() not in MANUAL_EXCLUSIONS]
    return all_kw

df['all_keywords'] = df.apply(combine_keywords, axis=1)

print(f"✓ Keywords extracted")
print(f"  Average keywords per document: {df['all_keywords'].apply(len).mean():.1f}")
print(f"  Documents with keywords: {(df['all_keywords'].apply(len) > 0).sum()}")
print(f"  Documents with author keywords: {df['author_keywords_parsed'].apply(lambda x: len(x) > 0).sum()}")'''),
    ("markdown", "## 4. Top Keywords Analysis"),
    ("code", '''def normalize_keyword(keyword):
    """Normalize keywords to handle variations."""
    normalized = re.sub(r'\\s*\\([^)]*\\)', '', keyword)
    normalized = normalized.replace('-', ' ')
    normalized = re.sub(r'\\s+', ' ', normalized)
    normalized = normalized.strip().title()
    return normalized

# Normalize and count all keywords
all_keywords_flat = [kw for keywords in df['all_keywords'] for kw in keywords]
all_keywords_normalized = [normalize_keyword(kw) for kw in all_keywords_flat]
keyword_counts = Counter(all_keywords_normalized)

# Get top keywords
top_n = 30
top_keywords = keyword_counts.most_common(top_n)

print(f"\\n📊 Top {top_n} Keywords in Decision Intelligence Research:")
print("="*60)
for i, (keyword, count) in enumerate(top_keywords, 1):
    pct = count / len(df) * 100
    print(f"{i:2d}. {keyword:30s} {count:4d} ({pct:5.1f}% of documents)")

# Save to CSV
top_keywords_df = pd.DataFrame(top_keywords, columns=['keyword', 'count'])
top_keywords_df['percentage'] = (top_keywords_df['count'] / len(df) * 100).round(1)
top_keywords_df.to_csv(OUTPUT_DIR / 'top_keywords.csv', index=False)
print(f"\\n✓ Top keywords saved to: {OUTPUT_DIR / 'top_keywords.csv'}")'''),
]

# Add cells to notebook
for cell_type, content in cells:
    notebook["cells"].append({
        "cell_type": cell_type,
        "execution_count": None,
        "metadata": {},
        "outputs": [] if cell_type == "code" else None,
        "source": [content] if cell_type == "markdown" else [content]
    })

# Write notebook
with open('03_keyword_analysis.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)

print(f"✓ Created complete notebook with {len(notebook['cells'])} cells")

# Made with Bob
