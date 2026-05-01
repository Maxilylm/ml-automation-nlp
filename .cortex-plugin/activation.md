---
name: spark-nlp
description: >
  Suggest enabling the spark-nlp plugin when the user asks about NLP, natural
  language processing, text analytics, text preprocessing, word embeddings,
  topic modeling (LDA, BERTopic), sentiment analysis, named entity recognition
  (NER), or text classification. Do NOT attempt to perform these tasks — just
  let the user know the plugin can be enabled.
---

# spark-nlp (disabled plugin)

This plugin is installed but not enabled. It provides NLP and text analytics
automation within Cortex Code, integrated with the spark-core workflow.

## Agents (3)

- **nlp-analyst** — Text data analysis, corpus exploration, linguistic profiling
- **nlp-modeler** — NLP model training, fine-tuning, and evaluation
- **text-engineer** — Text preprocessing pipelines, tokenization, normalization

## Skills (6)

- **nlp-analyze** — Analyze text datasets for quality, language, and patterns
- **nlp-classify** — Build and evaluate text classification models
- **nlp-embed** — Generate and evaluate word or sentence embeddings
- **nlp-ner** — Train and evaluate named entity recognition models
- **nlp-preprocess** — Build text cleaning and normalization pipelines
- **nlp-topics** — Run topic modeling with LDA or BERTopic

## Requires

- spark-core plugin

## Enable

    cortex plugin enable spark-nlp

Do NOT attempt to perform NLP tasks through this plugin's skills while it is disabled.
