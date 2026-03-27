# /nlp-ner

Named Entity Recognition pipeline: detect, classify, and extract entities from text.

## Usage

```
/nlp-ner <text_data_path> [--text-column <col>] [--model spacy|bert|rule-based] [--entity-types PER,ORG,LOC,DATE] [--training-data <path>]
```

- `text_data_path`: path to CSV, JSONL, or directory of text files
- `--text-column`: column containing text (default: auto-detect)
- `--model`: NER model type (default: spacy)
- `--entity-types`: comma-separated entity types to detect (default: all)
- `--training-data`: annotated data for custom model training (IOB or spaCy format)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `nlp_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/nlp_utils.py`
3. Verify text data path exists
4. Check model availability:
   - spaCy: verify `en_core_web_sm` or `en_core_web_trf` is installed
   - BERT: verify `transformers` package
   - rule-based: no external dependency

### Stage 1: Data Loading

1. Load text data (same logic as `/nlp-analyze`)
2. If `--training-data` provided: load annotated data (IOB, spaCy JSON, or CoNLL format)
3. Report: document count, sample preview

### Stage 2: Entity Extraction (Pre-trained Models)

1. **spaCy NER**:
   - Load spaCy model (`en_core_web_sm` or `en_core_web_trf`)
   - Process all documents through NER pipeline
   - Extract entities with labels, start/end positions, confidence
2. **BERT NER** (token classification):
   - Load `dslim/bert-base-NER` or specified model
   - Tokenize and run inference
   - Align subword tokens to word-level entities
   - Apply B-I-O tag decoding
3. **Rule-based**:
   - Regex patterns for dates, emails, phone numbers, URLs
   - Gazetteer lookup for known entities
   - Pattern matching for monetary values, percentages

### Stage 3: Custom Model Training (if --training-data provided)

1. Parse annotated training data into model-specific format
2. Train/validation split (80/20)
3. For spaCy: update NER component with training data
4. For BERT: fine-tune token classification head
5. Evaluate on validation set: entity-level P/R/F1
6. Report: training loss, validation metrics per entity type

### Stage 4: Entity Analysis

1. Entity frequency distribution (by type and by value)
2. Co-occurrence analysis (which entity types appear together)
3. Entity density per document (entities per 100 tokens)
4. Ambiguous entities (same text, different types)
5. Report: top entities per type (top 20), co-occurrence matrix

### Stage 5: Export

1. Save extracted entities to `reports/entities.jsonl`:
   ```json
   {"doc_id": 0, "text": "...", "entities": [{"text": "Apple", "label": "ORG", "start": 0, "end": 5}]}
   ```
2. If custom model trained: save to `models/ner/`
3. Generate inference script `src/extract_entities.py`

### Stage 6: Report

```python
from ml_utils import save_agent_report
save_agent_report("nlp-modeler", {
    "status": "completed",
    "model": model_type,
    "documents_processed": doc_count,
    "total_entities": total_entity_count,
    "entity_distribution": {etype: count for etype, count in type_counts.items()},
    "top_entities": {etype: top_values for etype, top_values in top_per_type.items()},
    "metrics": per_type_metrics,  # if training data provided
    "output_files": ["reports/entities.jsonl"],
    "recommendations": recommendations
})
```

Print entity extraction summary: counts by type, top entities, quality metrics.
