---
name: nlp-topics
description: "Topic modeling: discover latent topics using LDA, BERTopic, or NMF. Automatic topic count selection, coherence scoring, and topic labeling."
aliases: [topic modeling, lda, bertopic, nmf, discover topics, latent topics]
extends: spark
user_invocable: true
---

# NLP Topics

Discover latent topics in a text corpus. Supports LDA (Gensim), BERTopic (transformer-based), and NMF (scikit-learn). Includes automatic topic count optimization via coherence scoring, topic diversity analysis, document-topic assignment, and labeled topic summaries.

## When to Use

- You want to discover the main themes or topics in an unlabeled text corpus.
- You need to compare topic modeling methods (LDA vs BERTopic vs NMF) and select the best fit for your data.
- You want automatic topic count optimization using coherence scores instead of guessing the number of topics.
- You need document-topic assignments for downstream clustering, filtering, or labeling workflows.

## Workflow

1. **Env Check** -- Verify Python environment, install method-specific dependencies (gensim for LDA, bertopic + sentence-transformers for BERTopic, scikit-learn for NMF).
2. **Data Loading** -- Load text data from CSV, JSONL, or directory. Use preprocessed output from `nlp-preprocess` if available.
3. **Topic Discovery** -- Run the selected method, optimize topic count via coherence scoring (or use `--num-topics` if specified), generate topic labels from top words, assign documents to topics, and export topic summaries and document-topic mappings.

## Report Bus Integration

The `nlp-modeler` agent writes `nlp_topics_report.json` to the report bus with keys: `method`, `num_topics`, `coherence_score`, `topics` (list of top words per topic), `topic_distribution`, and `output_path`. Downstream skills and the core orchestrator can use topic assignments for corpus segmentation or label generation.

## Full Specification

Usage: `/nlp-topics <text_data_path> [--text-column <col>] [--method lda|bertopic|nmf] [--num-topics <n>]`

See `commands/nlp-topics.md` for the complete workflow.
