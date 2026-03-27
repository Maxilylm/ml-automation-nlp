# /nlp-embed

Generate text embeddings using TF-IDF, Word2Vec, or Sentence Transformers.

## Usage

```
/nlp-embed <text_data_path> [--text-column <col>] [--method tfidf|word2vec|sentence-transformers] [--model <model_name>] [--output <path>]
```

- `text_data_path`: path to CSV, JSONL, or directory of text files
- `--text-column`: column containing text (default: auto-detect)
- `--method`: embedding method (default: sentence-transformers)
- `--model`: model name (default: `all-MiniLM-L6-v2` for sentence-transformers, skip-gram for word2vec)
- `--output`: output path for embeddings (default: `embeddings/`)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `nlp_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/nlp_utils.py`
3. Verify text data path exists
4. Check required packages based on `--method`:
   - tfidf: `sklearn`
   - word2vec: `gensim`
   - sentence-transformers: `sentence-transformers`

### Stage 1: Data Loading and Preprocessing

1. Load text data (same logic as `/nlp-analyze`)
2. Apply basic preprocessing (lowercase, strip whitespace, remove empty)
3. Report: document count, avg document length

### Stage 2: TF-IDF Embeddings (if method=tfidf)

1. Configure TfidfVectorizer:
   - `ngram_range`: (1, 2) -- unigrams and bigrams
   - `max_features`: 10000 (configurable)
   - `min_df`: 2, `max_df`: 0.95
   - `sublinear_tf`: True
2. Fit and transform corpus
3. Report: feature count, sparsity ratio, top 20 features by IDF weight
4. Save: sparse matrix (.npz), vectorizer (pickle), feature names (JSON)

### Stage 3: Word2Vec Embeddings (if method=word2vec)

1. Tokenize all documents
2. Train Word2Vec model:
   - `vector_size`: 300 (configurable)
   - `window`: 5
   - `min_count`: 2
   - `sg`: 1 (skip-gram)
   - `epochs`: 10
3. Generate document embeddings via weighted average (TF-IDF weights)
4. Report: vocabulary size, embedding dimension, training time
5. Save: Word2Vec model (.model), document embeddings (.npy)

### Stage 4: Sentence Transformer Embeddings (if method=sentence-transformers)

1. Load Sentence Transformer model (`--model`)
2. Encode all documents (batch processing with progress)
3. Normalize embeddings (L2)
4. Report: embedding dimension, encoding time, throughput (docs/sec)
5. Save: embeddings (.npy), model name and config (JSON)

### Stage 5: Embedding Quality Assessment

1. Compute pairwise similarity distribution (sample 1000 pairs)
2. Check for degenerate embeddings (near-zero norm, all-same vectors)
3. If labels available: compute class separation (silhouette score, inter/intra-class distance)
4. Dimensionality reduction (UMAP to 2D) for visualization data export
5. Report: similarity distribution stats, quality flags

### Stage 6: Report

```python
from ml_utils import save_agent_report
save_agent_report("text-engineer", {
    "status": "completed",
    "method": method,
    "model": model_name,
    "documents_embedded": doc_count,
    "embedding_dimension": dimension,
    "output_path": output_path,
    "quality": {
        "mean_similarity": mean_sim,
        "std_similarity": std_sim,
        "degenerate_count": degen_count,
        "silhouette_score": silhouette  # if labels available
    },
    "recommendations": recommendations
})
```

Write embeddings to `--output` directory.
Print summary: method, dimension, document count, quality metrics.
