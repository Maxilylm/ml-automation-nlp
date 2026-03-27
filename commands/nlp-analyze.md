# /nlp-analyze

Text data EDA: vocabulary statistics, n-gram analysis, distributions, and language detection.

## Usage

```
/nlp-analyze <text_data_path> [--text-column <col>] [--label-column <col>] [--language auto]
```

- `text_data_path`: path to CSV, JSONL, or directory of text files
- `--text-column`: column name containing text (default: auto-detect)
- `--label-column`: column name containing labels (optional, for per-class analysis)
- `--language`: expected language or `auto` for detection (default: auto)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `nlp_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/nlp_utils.py`
3. Verify text data path exists and is readable
4. Detect data format (CSV, JSONL, directory of text files)

### Stage 1: Data Loading

1. Load text data based on format:
   - **CSV**: read with pandas, identify text column (longest avg string length or `--text-column`)
   - **JSONL**: parse line-by-line, extract text field
   - **Directory**: read each file as one document
2. Report: document count, format, detected text column
3. Flag empty or null text entries

### Stage 2: Basic Statistics

1. Document length distribution (words, characters, sentences)
2. Token count: total tokens, unique tokens, type-token ratio
3. Sentence count distribution
4. Report: mean/median/min/max/std for all length metrics

### Stage 3: Vocabulary Analysis

1. Build vocabulary from corpus
2. Token frequency distribution (top 50 tokens)
3. Hapax legomena count (tokens appearing exactly once)
4. Bigram and trigram frequency analysis (top 30 each)
5. Zipf's law fit (log-log frequency plot data)
6. If `--label-column` provided: per-class vocabulary overlap

### Stage 4: Language Detection

1. Run language detection on sample of documents (up to 500)
2. Report: language distribution, confidence scores
3. Flag mixed-language documents
4. Identify encoding issues or non-text content

### Stage 5: Text Quality Assessment

1. Duplicate detection (exact match and near-duplicate via Jaccard similarity)
2. Noise detection: HTML tags, URLs, email addresses, excessive punctuation
3. Empty/near-empty documents (< 5 words)
4. Readability scores (Flesch-Kincaid grade level)
5. Report: quality issue counts with sample excerpts

### Stage 6: Report

```python
from ml_utils import save_agent_report
save_agent_report("nlp-analyst", {
    "status": "completed",
    "document_count": doc_count,
    "vocabulary": {
        "total_tokens": total_tokens,
        "unique_tokens": unique_tokens,
        "ttr": type_token_ratio,
        "hapax_count": hapax_count
    },
    "length_stats": {
        "words": {"mean": m, "median": med, "min": mn, "max": mx},
        "characters": {"mean": m, "median": med, "min": mn, "max": mx}
    },
    "languages": language_distribution,
    "quality_issues": {
        "duplicates": dup_count,
        "empty": empty_count,
        "noisy": noisy_count
    },
    "top_ngrams": {"unigrams": top_uni, "bigrams": top_bi, "trigrams": top_tri},
    "recommendations": recommendations
})
```

Write analysis report to `reports/nlp_analysis_report.json`.
Print summary table with vocabulary stats, length distributions, and quality issues.
