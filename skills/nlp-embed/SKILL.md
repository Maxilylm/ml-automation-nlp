---
name: nlp-embed
description: "Generate text embeddings using TF-IDF, Word2Vec, or Sentence Transformers. Includes embedding quality assessment and dimensionality reduction."
aliases: [text embeddings, tfidf, word2vec, sentence embeddings, vectorize text]
extends: ml-automation
user_invocable: true
---

# NLP Embed

Generate document embeddings from text data. Supports TF-IDF sparse features, Word2Vec trained on the corpus, and Sentence Transformer dense embeddings. Assesses embedding quality via similarity distributions and class separation metrics. Exports embeddings for downstream classification or clustering tasks.

## When to Use

- You need numerical representations of text for classification, clustering, or similarity search.
- You want to compare embedding methods (TF-IDF vs Word2Vec vs Sentence Transformers) on your corpus.
- You need embedding quality diagnostics such as intra-class vs inter-class similarity or nearest-neighbor sanity checks.
- You want exported embeddings (numpy arrays or sparse matrices) ready for downstream ML pipelines.

## Workflow

1. **Env Check** -- Verify Python environment, install method-specific dependencies (scikit-learn for TF-IDF, gensim for Word2Vec, sentence-transformers for dense embeddings).
2. **Data Loading** -- Load text data from CSV, JSONL, or directory. Use preprocessed output from `nlp-preprocess` if available.
3. **Embedding Generation** -- Generate embeddings with the selected method, compute quality metrics (similarity distributions, coverage), apply optional dimensionality reduction (PCA/UMAP), and export the embedding matrix.

## Report Bus Integration

The `text-engineer` agent writes `nlp_embed_report.json` to the report bus with keys: `method`, `model`, `dimension`, `count`, `quality_metrics`, and `output_path`. Downstream skills (`nlp-classify`, `nlp-topics`) read this report to locate pre-computed embeddings.

## Full Specification

Usage: `/nlp-embed <text_data_path> [--text-column <col>] [--method tfidf|word2vec|sentence-transformers]`

See `commands/nlp-embed.md` for the complete workflow.
