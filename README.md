# spark-nlp

NLP and text analytics extension for [ml-automation](https://github.com/Maxilylm/ml-automation-core).

## Prerequisites

- [ml-automation](https://github.com/Maxilylm/ml-automation-core) core plugin (>= v1.8.0)
- Claude Code CLI
- NLP libraries as needed: nltk, spacy, gensim, sentence-transformers, bertopic

## Installation

```bash
claude plugin add /path/to/spark-nlp
```

## What's Included

### Agents

| Agent | Purpose | Hooks Into |
|---|---|---|
| `nlp-analyst` | Text data analysis: distributions, vocabulary, language detection, quality assessment | `after-eda` |
| `text-engineer` | Text feature engineering: embeddings, TF-IDF, tokenization, preprocessing pipelines | `after-feature-engineering` |
| `nlp-modeler` | NLP model training: sentiment, classification, NER, topic modeling | *(direct invocation)* |

### Commands

| Command | Purpose |
|---|---|
| `/nlp-analyze` | Text data EDA (vocabulary stats, n-grams, distributions, language detection) |
| `/nlp-preprocess` | Text preprocessing pipeline (tokenize, stem, lemmatize, clean, normalize) |
| `/nlp-embed` | Generate text embeddings (TF-IDF, Word2Vec, Sentence Transformers) |
| `/nlp-classify` | Train text classifier (sentiment, topic, custom categories) |
| `/nlp-ner` | Named Entity Recognition pipeline |
| `/nlp-topics` | Topic modeling (LDA, BERTopic, NMF) |

## Getting Started

```bash
# Analyze a text corpus
/nlp-analyze data/reviews.csv --text-column review_text --label-column sentiment

# Preprocess text data
/nlp-preprocess data/reviews.csv --steps lowercase,strip_html,remove_urls,stopwords,lemmatize

# Generate embeddings
/nlp-embed data/reviews.csv --method sentence-transformers --model all-MiniLM-L6-v2

# Train a sentiment classifier
/nlp-classify data/reviews.csv --text-column review_text --label-column sentiment --model logistic

# Extract named entities
/nlp-ner data/articles.csv --text-column body --model spacy --entity-types PER,ORG,LOC

# Discover topics
/nlp-topics data/articles.csv --text-column body --method bertopic --auto-topics
```

## How It Integrates

When installed alongside the core plugin:

1. **Automatic routing** -- Tasks mentioning NLP, text analysis, sentiment, NER, or topic modeling are routed to NLP agents
2. **Core workflow hooks** -- When running `/team-coldstart`:
   - `nlp-analyst` fires at `after-eda` to analyze text columns and corpus quality
   - `text-engineer` fires at `after-feature-engineering` to generate text embeddings and features
3. **Core agent reuse** -- Commands use eda-analyst, developer, ml-theory-advisor from core

## License

MIT
