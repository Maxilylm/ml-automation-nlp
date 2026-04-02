"""
NLP utilities for the ml-automation-nlp extension plugin.

Requires ml_utils.py from the ml-automation core plugin to be present
in the same directory (copied via Stage 0 of NLP commands).
"""

import json
import re
import math
from pathlib import Path
from collections import Counter


# --- Relevance Detection ---

NLP_INDICATORS = {
    "nltk",
    "spacy",
    "gensim",
    "textblob",
    "transformers",
    "sentence_transformers",
    "sklearn.feature_extraction.text",
    "bertopic",
    "flair",
    "stanza",
    "coreferee",
    "allennlp",
}

NLP_FILE_PATTERNS = [
    "corpus",
    "text_data",
    "documents",
    "texts",
]


def detect_nlp_relevance(project_path="."):
    """Check if project has NLP/text analytics indicators for relevance gating.

    Checks: NLP library imports, text corpus files, CSV/JSONL with text fields,
    directories named corpus/text_data/documents.

    Args:
        project_path: root directory of the project

    Returns:
        dict with 'is_nlp': bool, 'indicators': list of found indicators
    """
    indicators = []
    project = Path(project_path)

    # Check for text corpus directories
    for dir_name in NLP_FILE_PATTERNS:
        corpus_dir = project / dir_name
        if corpus_dir.is_dir():
            file_count = len(list(corpus_dir.glob("*")))
            if file_count > 0:
                indicators.append(f"{dir_name}/ directory with {file_count} files")

    # Check for .txt files in bulk (corpus indicator)
    txt_files = list(project.glob("**/*.txt"))[:100]
    if len(txt_files) > 10:
        indicators.append(f"{len(txt_files)} .txt files found (possible corpus)")

    # Check requirements for NLP packages
    for req_file in ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"]:
        req_path = project / req_file
        if req_path.exists():
            try:
                content = req_path.read_text().lower()
                for pkg in NLP_INDICATORS:
                    pkg_base = pkg.split(".")[0]
                    if pkg_base in content:
                        indicators.append(f"{pkg_base} in {req_file}")
            except (UnicodeDecodeError, PermissionError):
                continue

    # Check Python files for NLP imports
    py_files = list(project.glob("**/*.py"))[:50]
    for py_file in py_files:
        try:
            content = py_file.read_text()
            for pkg in NLP_INDICATORS:
                pkg_base = pkg.split(".")[0]
                if f"import {pkg_base}" in content or f"from {pkg_base}" in content:
                    indicators.append(f"{pkg_base} import in {py_file.name}")
                    break
        except (UnicodeDecodeError, PermissionError):
            continue

    # Check CSV files for text columns (long string columns)
    csv_files = list(project.glob("**/*.csv"))[:10]
    for csv_file in csv_files:
        try:
            with open(csv_file) as f:
                header = f.readline().strip().lower()
                if any(col in header for col in ["text", "content", "body", "message",
                                                   "review", "comment", "description",
                                                   "sentence", "document", "abstract"]):
                    indicators.append(f"Text column in {csv_file.name}")
        except (UnicodeDecodeError, PermissionError):
            continue

    # Check JSONL files for text fields
    jsonl_files = list(project.glob("**/*.jsonl"))[:10]
    for jsonl_file in jsonl_files:
        try:
            with open(jsonl_file) as f:
                first_line = f.readline().strip()
                if first_line:
                    obj = json.loads(first_line)
                    if any(k in obj for k in ["text", "content", "body", "sentence",
                                               "document", "review", "comment"]):
                        indicators.append(f"Text field in {jsonl_file.name}")
        except (json.JSONDecodeError, UnicodeDecodeError, PermissionError):
            continue

    # Check for spaCy models
    for model_dir in ["en_core_web_sm", "en_core_web_md", "en_core_web_lg",
                       "en_core_web_trf"]:
        if (project / model_dir).is_dir():
            indicators.append(f"spaCy model: {model_dir}")

    return {
        "is_nlp": len(indicators) > 0,
        "indicators": indicators,
    }


# --- Text Preprocessing ---

_URL_PATTERN = re.compile(
    r"https?://[^\s<>\"']+|www\.[^\s<>\"']+"
)
_EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)
_HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
_MULTI_SPACE_PATTERN = re.compile(r"\s+")

# Common English stopwords (subset — full list from NLTK has ~179 words)
_STOPWORDS_EN = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "was", "are", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "need", "dare",
    "ought", "used", "not", "no", "nor", "as", "if", "than", "that",
    "this", "these", "those", "it", "its", "i", "me", "my", "we", "our",
    "you", "your", "he", "him", "his", "she", "her", "they", "them",
    "their", "what", "which", "who", "whom", "when", "where", "why", "how",
    "all", "each", "every", "both", "few", "more", "most", "other", "some",
    "such", "only", "own", "same", "so", "very", "just", "because",
    "about", "into", "through", "during", "before", "after", "above",
    "below", "between", "out", "off", "over", "under", "again", "further",
    "then", "once", "here", "there", "also", "up", "down",
}


def preprocess_text(text, steps=None, language="en", custom_stopwords=None):
    """Apply a configurable preprocessing pipeline to text.

    Available steps (applied in order given):
        lowercase, strip_html, remove_urls, remove_emails,
        remove_punctuation, remove_numbers, remove_special,
        normalize_whitespace, stopwords, min_length_3

    Args:
        text: input text string
        steps: list of step names (default: standard pipeline)
        language: language code for stopwords (default: 'en')
        custom_stopwords: additional stopwords to remove

    Returns:
        preprocessed text string
    """
    if steps is None:
        steps = [
            "lowercase", "strip_html", "remove_urls", "remove_emails",
            "remove_punctuation", "normalize_whitespace", "stopwords",
        ]

    stopwords = set(_STOPWORDS_EN)
    if custom_stopwords:
        stopwords.update(w.lower() for w in custom_stopwords)

    for step in steps:
        if step == "lowercase":
            text = text.lower()
        elif step == "strip_html":
            text = _HTML_TAG_PATTERN.sub(" ", text)
        elif step == "remove_urls":
            text = _URL_PATTERN.sub(" ", text)
        elif step == "remove_emails":
            text = _EMAIL_PATTERN.sub(" ", text)
        elif step == "remove_punctuation":
            text = re.sub(r"[^\w\s]", " ", text)
        elif step == "remove_numbers":
            text = re.sub(r"\b\d+\b", " ", text)
        elif step == "remove_special":
            text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        elif step == "normalize_whitespace":
            text = _MULTI_SPACE_PATTERN.sub(" ", text).strip()
        elif step == "stopwords":
            tokens = text.split()
            tokens = [t for t in tokens if t.lower() not in stopwords]
            text = " ".join(tokens)
        elif step == "min_length_3":
            tokens = text.split()
            tokens = [t for t in tokens if len(t) >= 3]
            text = " ".join(tokens)

    return text


# --- TF-IDF ---

def compute_tfidf(documents, max_features=10000, ngram_range=(1, 2),
                   min_df=2, max_df=0.95, sublinear_tf=True):
    """Compute TF-IDF feature matrix from a list of documents.

    Pure-Python implementation for environments without sklearn.
    For production use, prefer sklearn.feature_extraction.text.TfidfVectorizer.

    Args:
        documents: list of text strings
        max_features: maximum number of features (default: 10000)
        ngram_range: tuple (min_n, max_n) for n-gram extraction (default: (1, 2))
        min_df: minimum document frequency (int or float, default: 2)
        max_df: maximum document frequency (float, default: 0.95)
        sublinear_tf: apply sublinear TF scaling (1 + log(tf)) (default: True)

    Returns:
        dict with:
            'matrix': list of lists (dense TF-IDF matrix, samples x features)
            'feature_names': list of feature strings
            'idf_weights': dict mapping feature -> IDF weight
            'shape': tuple (n_samples, n_features)
    """
    n_docs = len(documents)

    # Convert min_df/max_df to absolute counts
    if isinstance(min_df, float):
        min_df = int(min_df * n_docs)
    if isinstance(max_df, float):
        max_df = int(max_df * n_docs)

    min_n, max_n = ngram_range

    # Tokenize and extract n-grams per document
    doc_ngrams = []
    for doc in documents:
        tokens = doc.lower().split()
        ngrams = []
        for n in range(min_n, max_n + 1):
            for i in range(len(tokens) - n + 1):
                ngrams.append(" ".join(tokens[i:i + n]))
        doc_ngrams.append(ngrams)

    # Document frequency
    df_counts = Counter()
    for ngrams in doc_ngrams:
        unique_ngrams = set(ngrams)
        for ng in unique_ngrams:
            df_counts[ng] += 1

    # Filter by min_df and max_df
    valid_features = {
        ng for ng, count in df_counts.items()
        if count >= min_df and count <= max_df
    }

    # Select top features by document frequency
    feature_df = [(ng, df_counts[ng]) for ng in valid_features]
    feature_df.sort(key=lambda x: x[1], reverse=True)
    selected_features = [ng for ng, _ in feature_df[:max_features]]
    feature_to_idx = {ng: i for i, ng in enumerate(selected_features)}

    # Compute IDF
    idf = {}
    for feature in selected_features:
        idf[feature] = math.log(n_docs / (1 + df_counts[feature])) + 1

    # Compute TF-IDF matrix
    n_features = len(selected_features)
    matrix = []

    for ngrams in doc_ngrams:
        tf_counts = Counter(ngrams)
        row = [0.0] * n_features
        for ng, count in tf_counts.items():
            if ng in feature_to_idx:
                idx = feature_to_idx[ng]
                tf = 1 + math.log(count) if sublinear_tf and count > 0 else count
                row[idx] = tf * idf[ng]
        # L2 normalize
        norm = math.sqrt(sum(v * v for v in row))
        if norm > 0:
            row = [v / norm for v in row]
        matrix.append(row)

    return {
        "matrix": matrix,
        "feature_names": selected_features,
        "idf_weights": {f: round(idf[f], 4) for f in selected_features},
        "shape": (n_docs, n_features),
    }


# --- Embeddings ---

def generate_embeddings(texts, method="sentence-transformers",
                         model="all-MiniLM-L6-v2"):
    """Generate text embeddings using the specified method.

    Args:
        texts: list of text strings
        method: embedding method ('sentence-transformers', 'word2vec', 'tfidf')
        model: model name (for sentence-transformers or word2vec config)

    Returns:
        dict with:
            'embeddings': numpy array or list of lists (n_samples x dimension)
            'method': method used
            'model': model name
            'dimension': embedding dimension
            'count': number of texts embedded
    """
    if method == "tfidf":
        result = compute_tfidf(texts)
        return {
            "embeddings": result["matrix"],
            "method": "tfidf",
            "model": "tfidf",
            "dimension": result["shape"][1],
            "count": result["shape"][0],
        }
    elif method == "word2vec":
        return _embed_word2vec(texts, model)
    elif method == "sentence-transformers":
        return _embed_sentence_transformers(texts, model)
    else:
        raise ValueError(f"Unknown embedding method: {method}")


def _embed_sentence_transformers(texts, model):
    """Generate embeddings using Sentence Transformers."""
    try:
        from sentence_transformers import SentenceTransformer
        st_model = SentenceTransformer(model)
        embeddings = st_model.encode(
            texts, show_progress_bar=True, normalize_embeddings=True
        )
        return {
            "embeddings": embeddings,
            "method": "sentence-transformers",
            "model": model,
            "dimension": embeddings.shape[1],
            "count": len(texts),
        }
    except ImportError:
        raise ImportError(
            "sentence-transformers required. "
            "Install with: pip install sentence-transformers"
        )


def _embed_word2vec(texts, model_config):
    """Generate document embeddings via Word2Vec averaging."""
    try:
        from gensim.models import Word2Vec
        import numpy as np

        # Tokenize
        tokenized = [text.lower().split() for text in texts]

        # Train Word2Vec
        w2v_model = Word2Vec(
            sentences=tokenized,
            vector_size=300,
            window=5,
            min_count=2,
            sg=1,  # skip-gram
            epochs=10,
            workers=4,
        )

        # Document embeddings via averaging
        dimension = w2v_model.vector_size
        embeddings = []
        for tokens in tokenized:
            vectors = [
                w2v_model.wv[t] for t in tokens if t in w2v_model.wv
            ]
            if vectors:
                doc_vec = np.mean(vectors, axis=0)
                # L2 normalize
                norm = np.linalg.norm(doc_vec)
                if norm > 0:
                    doc_vec = doc_vec / norm
                embeddings.append(doc_vec)
            else:
                embeddings.append(np.zeros(dimension))

        embeddings = np.array(embeddings)
        return {
            "embeddings": embeddings,
            "method": "word2vec",
            "model": "word2vec-skipgram-300d",
            "dimension": dimension,
            "count": len(texts),
        }
    except ImportError:
        raise ImportError(
            "gensim required. Install with: pip install gensim"
        )


# --- Text Statistics ---

def compute_text_stats(documents):
    """Compute comprehensive text statistics for a corpus.

    Args:
        documents: list of text strings

    Returns:
        dict with vocabulary stats, length distributions, n-gram frequencies,
        and quality indicators
    """
    if not documents:
        return {"error": "Empty document list"}

    all_tokens = []
    doc_lengths_words = []
    doc_lengths_chars = []
    doc_lengths_sentences = []

    for doc in documents:
        tokens = doc.split()
        all_tokens.extend(tokens)
        doc_lengths_words.append(len(tokens))
        doc_lengths_chars.append(len(doc))
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', doc)
        sentences = [s.strip() for s in sentences if s.strip()]
        doc_lengths_sentences.append(len(sentences))

    total_tokens = len(all_tokens)
    token_counts = Counter(all_tokens)
    unique_tokens = len(token_counts)
    hapax = sum(1 for count in token_counts.values() if count == 1)

    # Type-token ratio
    ttr = unique_tokens / max(total_tokens, 1)

    # N-gram frequencies
    lower_tokens = [t.lower() for t in all_tokens]
    unigram_freq = Counter(lower_tokens).most_common(30)
    bigrams = [
        f"{lower_tokens[i]} {lower_tokens[i + 1]}"
        for i in range(len(lower_tokens) - 1)
    ]
    bigram_freq = Counter(bigrams).most_common(30)
    trigrams = [
        f"{lower_tokens[i]} {lower_tokens[i + 1]} {lower_tokens[i + 2]}"
        for i in range(len(lower_tokens) - 2)
    ]
    trigram_freq = Counter(trigrams).most_common(20)

    # Quality indicators
    empty_docs = sum(1 for d in documents if len(d.strip()) == 0)
    short_docs = sum(1 for wc in doc_lengths_words if wc < 5)

    # Duplicate detection (exact)
    doc_set = set()
    exact_duplicates = 0
    for doc in documents:
        normalized = doc.strip().lower()
        if normalized in doc_set:
            exact_duplicates += 1
        doc_set.add(normalized)

    def _stats(values):
        if not values:
            return {"mean": 0, "median": 0, "min": 0, "max": 0, "std": 0}
        n = len(values)
        mean = sum(values) / n
        sorted_v = sorted(values)
        median = sorted_v[n // 2] if n % 2 else (sorted_v[n // 2 - 1] + sorted_v[n // 2]) / 2
        variance = sum((v - mean) ** 2 for v in values) / max(n - 1, 1)
        std = math.sqrt(variance)
        return {
            "mean": round(mean, 2),
            "median": round(median, 2),
            "min": min(values),
            "max": max(values),
            "std": round(std, 2),
        }

    return {
        "document_count": len(documents),
        "vocabulary": {
            "total_tokens": total_tokens,
            "unique_tokens": unique_tokens,
            "type_token_ratio": round(ttr, 4),
            "hapax_legomena": hapax,
        },
        "length_distributions": {
            "words": _stats(doc_lengths_words),
            "characters": _stats(doc_lengths_chars),
            "sentences": _stats(doc_lengths_sentences),
        },
        "top_ngrams": {
            "unigrams": [{"token": t, "count": c} for t, c in unigram_freq],
            "bigrams": [{"token": t, "count": c} for t, c in bigram_freq],
            "trigrams": [{"token": t, "count": c} for t, c in trigram_freq],
        },
        "quality": {
            "empty_documents": empty_docs,
            "short_documents": short_docs,
            "exact_duplicates": exact_duplicates,
        },
    }


# --- Classification Evaluation ---

def evaluate_classification(y_true, y_pred, labels=None):
    """Evaluate text classification results with standard metrics.

    Args:
        y_true: list of true labels
        y_pred: list of predicted labels
        labels: optional list of label names (default: auto-detect)

    Returns:
        dict with accuracy, macro/weighted F1, per-class metrics,
        confusion matrix
    """
    assert len(y_true) == len(y_pred), "Label count mismatch"

    if labels is None:
        labels = sorted(set(y_true) | set(y_pred))

    n = len(y_true)
    label_to_idx = {label: i for i, label in enumerate(labels)}
    n_classes = len(labels)

    # Confusion matrix
    cm = [[0] * n_classes for _ in range(n_classes)]
    correct = 0
    for true, pred in zip(y_true, y_pred):
        if true in label_to_idx and pred in label_to_idx:
            cm[label_to_idx[true]][label_to_idx[pred]] += 1
        if true == pred:
            correct += 1

    accuracy = correct / max(n, 1)

    # Per-class metrics
    per_class = {}
    macro_p, macro_r, macro_f1 = 0.0, 0.0, 0.0
    weighted_f1_sum = 0.0
    total_support = 0

    for i, label in enumerate(labels):
        tp = cm[i][i]
        fp = sum(cm[j][i] for j in range(n_classes)) - tp
        fn = sum(cm[i][j] for j in range(n_classes)) - tp
        support = tp + fn

        precision = tp / max(tp + fp, 1)
        recall = tp / max(tp + fn, 1)
        f1 = 2 * precision * recall / max(precision + recall, 1e-8)

        per_class[label] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "support": support,
        }

        macro_p += precision
        macro_r += recall
        macro_f1 += f1
        weighted_f1_sum += f1 * support
        total_support += support

    macro_f1 /= max(n_classes, 1)
    weighted_f1 = weighted_f1_sum / max(total_support, 1)

    return {
        "accuracy": round(accuracy, 4),
        "macro_f1": round(macro_f1, 4),
        "weighted_f1": round(weighted_f1, 4),
        "per_class": per_class,
        "confusion_matrix": cm,
        "labels": labels,
        "sample_count": n,
    }
