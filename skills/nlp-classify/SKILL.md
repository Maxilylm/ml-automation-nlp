---
name: nlp-classify
description: "Train text classifiers for sentiment, topic, or custom categories. Supports Logistic Regression, SVM, Naive Bayes, and BERT fine-tuning."
aliases: [text classification, sentiment analysis, sentiment model, text classifier, classify text]
extends: ml-automation
user_invocable: true
---

# NLP Classify

Train and evaluate text classifiers. Supports traditional ML models (Logistic Regression, SVM, Naive Bayes on TF-IDF) and transformer fine-tuning (BERT, DistilBERT). Handles class imbalance, performs cross-validation, generates confusion matrices and per-class metrics, and exports a reusable inference script.

## Full Specification

See `commands/nlp-classify.md` for the complete workflow.
