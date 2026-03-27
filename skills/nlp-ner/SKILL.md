---
name: nlp-ner
description: "Named Entity Recognition pipeline: extract persons, organizations, locations, dates, and custom entities using spaCy, BERT, or rule-based methods."
aliases: [named entity recognition, entity extraction, ner model, extract entities]
extends: ml-automation
user_invocable: true
---

# NLP NER

Run Named Entity Recognition on text data. Supports pre-trained models (spaCy, BERT-NER), rule-based extraction (regex, gazetteers), and custom model training from annotated data. Produces entity frequency analysis, co-occurrence matrices, and exports structured entity data for downstream use.

## Full Specification

See `commands/nlp-ner.md` for the complete workflow.
