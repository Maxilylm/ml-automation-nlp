---
name: nlp-preprocess
description: "Text preprocessing pipeline: tokenize, stem, lemmatize, clean HTML/URLs, remove stopwords, normalize whitespace. Configurable step-by-step pipeline with before/after statistics."
aliases: [text cleaning, text normalization, tokenize, lemmatize, stopword removal]
extends: spark
user_invocable: true
---

# NLP Preprocess

Build and apply a configurable text preprocessing pipeline. Steps include lowercasing, HTML/URL removal, punctuation stripping, stopword removal, stemming, lemmatization, and whitespace normalization. Tracks vocabulary reduction and document length changes at each step. Exports a reusable pipeline script.

## When to Use

- Your text data contains HTML tags, URLs, or noisy formatting that needs cleaning before modeling.
- You want a reproducible, step-by-step preprocessing pipeline with before/after statistics at each stage.
- You need to experiment with different preprocessing configurations (e.g., with or without lemmatization) and compare their impact.
- You want an exported pipeline script that can be reused in production or by downstream NLP skills.

## Workflow

1. **Env Check** -- Verify Python environment, install NLTK data or spaCy models required by the selected steps.
2. **Data Loading** -- Load text data from CSV, JSONL, or directory. Detect or use the specified `--text-column`.
3. **Step-by-step Pipeline** -- Apply each preprocessing step in order, recording vocabulary size and mean document length before and after each step. Steps: `lowercase`, `strip_html`, `remove_urls`, `remove_punctuation`, `stopwords`, `lemmatize`, and more. Export the cleaned dataset and a reusable pipeline script.

## Report Bus Integration

The `text-engineer` agent writes `nlp_preprocess_report.json` to the report bus with keys: `steps_applied`, `per_step_stats` (vocabulary size and mean length before/after each step), `total_vocabulary_reduction`, and `output_path`. Downstream skills (`nlp-embed`, `nlp-classify`) read this report to locate the cleaned data.

## Full Specification

Usage: `/nlp-preprocess <text_data_path> [--text-column <col>] [--steps lowercase,strip_html,remove_urls,remove_punctuation,stopwords,lemmatize]`

See `commands/nlp-preprocess.md` for the complete workflow.
