# spark-nlp — Cortex Code Extension

NLP and text analytics. Text preprocessing, embeddings, topic modeling, sentiment analysis, NER, and text classification. Requires spark-core installed.

## Available Agents

| Agent | When to use |
|---|---|
| `nlp-analyst` | User wants to explore a text corpus, check vocabulary, distribution of lengths, or language statistics |
| `nlp-modeler` | User wants to build a text classifier, embedding model, topic model, or sentiment analyzer |
| `text-engineer` | User wants to build a text preprocessing pipeline, tokenization, normalization, or feature extraction |

## Available Skills

| Skill | Trigger |
|---|---|
| `/nlp-preprocess` | "preprocess text", "clean text data", "tokenize", "normalize text", "build text pipeline" |
| `/nlp-analyze` | "analyze text corpus", "text EDA", "vocabulary statistics", "explore text data" |
| `/nlp-classify` | "classify text", "sentiment analysis", "text categorization", "train text classifier" |
| `/nlp-ner` | "named entity recognition", "extract entities", "NER on this text", "find names and locations" |
| `/nlp-embed` | "create embeddings", "sentence embeddings", "word vectors", "semantic similarity" |
| `/nlp-topics` | "topic modeling", "LDA topics", "discover topics in corpus", "topic extraction" |

## Routing

- Corpus exploration, text statistics → `nlp-analyst`
- Classification, embedding, topic modeling → `nlp-modeler`
- Text preprocessing pipelines → `text-engineer`
- Fallback → spark-core orchestrator
