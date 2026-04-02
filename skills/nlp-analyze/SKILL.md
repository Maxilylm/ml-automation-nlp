---
name: nlp-analyze
description: "Text data EDA: vocabulary statistics, n-gram frequency analysis, document length distributions, language detection, and text quality assessment."
aliases: [text eda, text analysis, corpus analysis, vocabulary analysis, text statistics]
extends: spark
user_invocable: true
---

# NLP Analyze

Run comprehensive text data analysis on a corpus. Computes vocabulary statistics (type-token ratio, hapax legomena), n-gram frequencies, document length distributions, language detection, and text quality assessment (duplicates, noise, readability). Supports CSV, JSONL, and directory-of-files input formats.

## When to Use

- You have a text dataset and need to understand corpus characteristics before modeling.
- You want to identify quality issues: duplicates, empty documents, noisy text, or class imbalance in labels.
- You need vocabulary statistics (type-token ratio, hapax legomena) to inform preprocessing decisions.
- You want n-gram frequency analysis and document length distributions for feature engineering guidance.

## Workflow

1. **Env Check** -- Verify Python environment, install missing NLP dependencies (nltk, spacy if needed).
2. **Data Loading** -- Load text data from CSV, JSONL, or a directory of text files. Detect the text column automatically or use `--text-column`.
3. **Vocab Stats, N-grams, Length Distributions** -- Compute type-token ratio, hapax legomena, top unigrams/bigrams/trigrams, word/character/sentence length distributions, duplicate detection, and text quality indicators.

## Report Bus Integration

The `nlp-analyst` agent writes `nlp_analyze_report.json` to the report bus with keys: `document_count`, `vocabulary`, `length_distributions`, `top_ngrams`, `quality`, and `label_distribution` (when `--label-column` is provided). Downstream skills (`nlp-preprocess`, `nlp-embed`, `nlp-classify`) read this report to inherit corpus insights.

## Full Specification

Usage: `/nlp-analyze <text_data_path> [--text-column <col>] [--label-column <col>]`

See `commands/nlp-analyze.md` for the complete workflow.
