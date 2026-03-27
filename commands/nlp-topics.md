# /nlp-topics

Topic modeling: discover latent topics in a text corpus using LDA, BERTopic, or NMF.

## Usage

```
/nlp-topics <text_data_path> [--text-column <col>] [--method lda|bertopic|nmf] [--num-topics <n>] [--auto-topics]
```

- `text_data_path`: path to CSV, JSONL, or directory of text files
- `--text-column`: column containing text (default: auto-detect)
- `--method`: topic modeling algorithm (default: lda)
- `--num-topics`: number of topics (default: 10)
- `--auto-topics`: automatically determine optimal number of topics

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `nlp_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/nlp_utils.py`
3. Verify text data path exists
4. Check required packages:
   - lda: `sklearn`, `gensim`
   - bertopic: `bertopic`, `sentence-transformers`, `umap-learn`, `hdbscan`
   - nmf: `sklearn`

### Stage 1: Data Loading and Preprocessing

1. Load text data (same logic as `/nlp-analyze`)
2. Preprocess: lowercase, remove stopwords, lemmatize
3. Filter: remove documents shorter than 10 words after preprocessing
4. Report: document count after filtering, vocabulary size

### Stage 2: LDA Topic Modeling (if method=lda)

1. Build document-term matrix (bag-of-words or TF-IDF)
2. If `--auto-topics`: sweep num_topics from 5 to 30, compute coherence (C_v) for each
3. Train LDA model with `--num-topics`:
   - Gensim LdaMulticore for speed
   - passes=10, iterations=100
   - alpha='auto', eta='auto'
4. Report: per-topic top 10 words with weights, coherence score

### Stage 3: BERTopic (if method=bertopic)

1. Generate sentence embeddings (Sentence Transformers)
2. Reduce dimensionality (UMAP: n_components=5, n_neighbors=15)
3. Cluster documents (HDBSCAN: min_cluster_size=10)
4. Extract topic representations (c-TF-IDF)
5. If `--auto-topics`: use HDBSCAN automatic cluster detection
6. Report: topic count, per-topic representation, outlier percentage

### Stage 4: NMF Topic Modeling (if method=nmf)

1. Build TF-IDF matrix (max_features=10000)
2. If `--auto-topics`: sweep and evaluate reconstruction error + coherence
3. Fit NMF model with `--num-topics`
4. Extract topic-word distributions
5. Report: per-topic top 10 words, reconstruction error

### Stage 5: Topic Analysis

1. **Topic coherence**: C_v and C_npmi scores
2. **Topic diversity**: percentage of unique words across all topics
3. **Document-topic distribution**: dominant topic per document
4. **Topic size distribution**: document count per topic
5. **Topic labels**: generate descriptive label for each topic (top 3 words)
6. If `--auto-topics`: plot coherence vs. num_topics data

### Stage 6: Export

1. Save topic model to `models/topics/`
2. Save document-topic assignments to `reports/topic_assignments.csv`
3. Save topic-word distributions to `reports/topic_words.json`
4. Generate visualization data for topic maps

### Stage 7: Report

```python
from ml_utils import save_agent_report
save_agent_report("nlp-modeler", {
    "status": "completed",
    "method": method,
    "num_topics": num_topics,
    "documents_processed": doc_count,
    "coherence_score": coherence,
    "topic_diversity": diversity,
    "topics": [
        {"id": 0, "label": "technology AI", "top_words": [...], "doc_count": n},
        ...
    ],
    "topic_sizes": topic_size_distribution,
    "output_files": [
        "reports/topic_assignments.csv",
        "reports/topic_words.json"
    ],
    "recommendations": recommendations
})
```

Print topic summary: topic ID, label, top words, document count, coherence.
