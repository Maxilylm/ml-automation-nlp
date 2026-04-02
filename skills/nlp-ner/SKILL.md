---
name: nlp-ner
description: "Named Entity Recognition pipeline: extract persons, organizations, locations, dates, and custom entities using spaCy, BERT, or rule-based methods."
aliases: [named entity recognition, entity extraction, ner model, extract entities]
extends: ml-automation
user_invocable: true
---

# NLP NER

Run Named Entity Recognition on text data. Supports pre-trained models (spaCy, BERT-NER), rule-based extraction (regex, gazetteers), and custom model training from annotated data. Produces entity frequency analysis, co-occurrence matrices, and exports structured entity data for downstream use.

## When to Use

- You need to extract named entities (persons, organizations, locations, dates) from unstructured text.
- You want to compare extraction approaches: pre-trained spaCy pipelines, fine-tuned BERT-NER, or custom rule-based patterns.
- You need entity frequency analysis and co-occurrence matrices to understand relationships in your corpus.
- You have annotated data and want to train or fine-tune a custom NER model with evaluation metrics.

## Workflow

1. **Env Check** -- Verify Python environment, download spaCy model or transformer weights based on the selected `--model`.
2. **Data Loading** -- Load text data from CSV, JSONL, or directory. Use the specified `--text-column` or auto-detect.
3. **NER Extraction** -- Run the selected model over the corpus, extract entities filtered by `--entity-types`, compute entity frequency distributions, build co-occurrence matrices, and export structured entity data (CSV/JSON).

## Report Bus Integration

The `nlp-modeler` agent writes `nlp_ner_report.json` to the report bus with keys: `model`, `entity_types`, `entity_counts`, `top_entities_per_type`, `co_occurrence_summary`, and `output_path`. Downstream consumers can use the structured entity output for knowledge graph construction or feature enrichment.

## Full Specification

Usage: `/nlp-ner <text_data_path> [--text-column <col>] [--model spacy|bert|rule-based] [--entity-types PER,ORG,LOC,DATE]`

See `commands/nlp-ner.md` for the complete workflow.
