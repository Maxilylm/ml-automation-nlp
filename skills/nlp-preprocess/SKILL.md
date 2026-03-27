---
name: nlp-preprocess
description: "Text preprocessing pipeline: tokenize, stem, lemmatize, clean HTML/URLs, remove stopwords, normalize whitespace. Configurable step-by-step pipeline with before/after statistics."
aliases: [text cleaning, text normalization, tokenize, lemmatize, stopword removal]
extends: ml-automation
user_invocable: true
---

# NLP Preprocess

Build and apply a configurable text preprocessing pipeline. Steps include lowercasing, HTML/URL removal, punctuation stripping, stopword removal, stemming, lemmatization, and whitespace normalization. Tracks vocabulary reduction and document length changes at each step. Exports reusable pipeline script.

## Full Specification

See `commands/nlp-preprocess.md` for the complete workflow.
