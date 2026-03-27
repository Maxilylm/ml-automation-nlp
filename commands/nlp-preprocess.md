# /nlp-preprocess

Text preprocessing pipeline: tokenize, stem, lemmatize, clean, and normalize text data.

## Usage

```
/nlp-preprocess <text_data_path> [--text-column <col>] [--steps lowercase,strip_html,remove_urls,remove_punctuation,stopwords,lemmatize] [--language en] [--output <path>]
```

- `text_data_path`: path to CSV, JSONL, or directory of text files
- `--text-column`: column containing text (default: auto-detect)
- `--steps`: comma-separated preprocessing steps (default: all standard steps)
- `--language`: language for stopwords and lemmatization (default: en)
- `--output`: output path for preprocessed data (default: `data/preprocessed/`)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `nlp_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/nlp_utils.py`
3. Verify text data path exists
4. Check required packages for selected steps (spaCy model for lemmatization, nltk for stopwords)

### Stage 1: Data Loading

1. Load text data (same logic as `/nlp-analyze`)
2. Report: document count, detected text column, sample preview

### Stage 2: Pipeline Configuration

1. Parse `--steps` parameter and build pipeline:
   - `lowercase` -- convert to lowercase
   - `strip_html` -- remove HTML tags
   - `remove_urls` -- strip URLs
   - `remove_emails` -- strip email addresses
   - `remove_punctuation` -- remove punctuation characters
   - `remove_numbers` -- strip numeric tokens
   - `remove_special` -- remove special characters
   - `normalize_whitespace` -- collapse multiple spaces/newlines
   - `stopwords` -- remove stopwords (language-aware)
   - `stem` -- apply Porter/Snowball stemming
   - `lemmatize` -- apply lemmatization (spaCy or WordNet)
   - `min_length` -- remove tokens shorter than N characters
2. Report: pipeline steps in order, language setting

### Stage 3: Apply Preprocessing

1. Apply each step sequentially to all documents
2. Track per-step statistics:
   - Tokens removed / transformed count
   - Vocabulary size before and after each step
   - Processing time per step
3. Handle edge cases: empty results, encoding errors, non-text content

### Stage 4: Quality Validation

1. Compare before/after statistics:
   - Vocabulary reduction ratio
   - Average document length change
   - Documents reduced to empty (flag if > 5%)
2. Sample 10 documents: show before/after side-by-side
3. Warn if aggressive preprocessing removed too much content

### Stage 5: Export

1. Save preprocessed data to `--output` path:
   - Same format as input (CSV, JSONL)
   - Add `_preprocessed` suffix to text column
   - Preserve all other columns
2. Save pipeline configuration to `src/preprocess_config.json`
3. Generate reusable `src/preprocess_pipeline.py` script

### Stage 6: Report

```python
from ml_utils import save_agent_report
save_agent_report("text-engineer", {
    "status": "completed",
    "pipeline_steps": steps_applied,
    "documents_processed": doc_count,
    "vocabulary_before": vocab_before,
    "vocabulary_after": vocab_after,
    "reduction_ratio": round(1 - vocab_after / vocab_before, 4),
    "avg_length_before": avg_len_before,
    "avg_length_after": avg_len_after,
    "empty_after_preprocessing": empty_count,
    "output_path": output_path,
    "recommendations": recommendations
})
```

Print preprocessing summary: steps applied, vocabulary reduction, length stats.
