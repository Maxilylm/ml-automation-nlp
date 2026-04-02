---
name: nlp-classify
description: "Train text classifiers for sentiment, topic, or custom categories. Supports Logistic Regression, SVM, Naive Bayes, and BERT fine-tuning."
aliases: [text classification, sentiment analysis, sentiment model, text classifier, classify text]
extends: spark
user_invocable: true
---

# NLP Classify

Train and evaluate text classifiers. Supports traditional ML models (Logistic Regression, SVM, Naive Bayes on TF-IDF) and transformer fine-tuning (BERT, DistilBERT). Handles class imbalance, performs cross-validation, generates confusion matrices and per-class metrics, and exports a reusable inference script.

## When to Use

- You have labeled text data and need to train a sentiment, topic, or custom-category classifier.
- You want to compare multiple model types (logistic regression, SVM, naive Bayes, BERT) on the same dataset.
- You need detailed evaluation: per-class precision/recall/F1, confusion matrix, and cross-validation scores.
- You want an exported inference script for production deployment or batch prediction.

## Workflow

1. **Env Check** -- Verify Python environment, install model-specific dependencies (scikit-learn for traditional models, transformers + torch for BERT).
2. **Data Loading** -- Load text and label columns from CSV or JSONL. Detect class distribution and flag imbalance.
3. **Feature Extraction** -- Generate TF-IDF features (for traditional models) or tokenize with the appropriate transformer tokenizer (for BERT).
4. **Training** -- Train the selected model with stratified cross-validation. Apply class weighting or oversampling if imbalance is detected.
5. **Evaluation** -- Compute accuracy, macro/weighted F1, per-class metrics, and confusion matrix on a held-out test set. Export the trained model and an inference script.

## Report Bus Integration

The `nlp-modeler` agent writes `nlp_classify_report.json` to the report bus with keys: `model`, `accuracy`, `macro_f1`, `weighted_f1`, `per_class`, `confusion_matrix`, `cross_val_scores`, and `inference_script_path`. The core `spark` orchestrator can read this report for end-to-end pipeline summaries.

## Full Specification

Usage: `/nlp-classify <text_data_path> [--text-column <col>] [--label-column <col>] [--model logistic|svm|naive-bayes|bert]`

See `commands/nlp-classify.md` for the complete workflow.
