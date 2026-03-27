---
name: nlp-embed
description: "Generate text embeddings using TF-IDF, Word2Vec, or Sentence Transformers. Includes embedding quality assessment and dimensionality reduction."
aliases: [text embeddings, tfidf, word2vec, sentence embeddings, vectorize text]
extends: ml-automation
user_invocable: true
---

# NLP Embed

Generate document embeddings from text data. Supports TF-IDF sparse features, Word2Vec trained on corpus, and Sentence Transformer dense embeddings. Assesses embedding quality via similarity distributions and class separation metrics. Exports embeddings for downstream classification or clustering tasks.

## Full Specification

See `commands/nlp-embed.md` for the complete workflow.
