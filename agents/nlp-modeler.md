---
name: nlp-modeler
description: "Train NLP models: sentiment, classification, NER, topic modeling."
model: sonnet
color: "#B45309"
tools: [Read, Write, Bash(*), Glob, Grep]
extends: ml-automation
routing_keywords: [sentiment analysis, text classification, ner, named entity, topic modeling, lda, text model]
---

# NLP Modeler

No hooks -- invoked via `/nlp-classify`, `/nlp-ner`, or `/nlp-topics` commands.

## Capabilities

### Sentiment Analysis
- Lexicon-based (VADER, TextBlob polarity)
- ML-based (logistic regression, SVM on TF-IDF features)
- Transformer-based (fine-tuned BERT, DistilBERT)
- Aspect-based sentiment extraction
- Confidence calibration and threshold tuning

### Text Classification
- Traditional ML: Naive Bayes, Logistic Regression, SVM, Random Forest on TF-IDF
- Deep learning: CNN text classifier, BiLSTM with attention
- Transformer fine-tuning: BERT, DistilBERT, RoBERTa
- Multi-label classification support
- Class imbalance handling (oversampling, class weights, focal loss)

### Named Entity Recognition
- Rule-based (regex patterns, gazetteers)
- spaCy NER models (built-in and custom training)
- Transformer NER (token classification with BERT)
- Custom entity type definition and training
- Entity linking and disambiguation

### Topic Modeling
- LDA (Latent Dirichlet Allocation) with coherence optimization
- NMF (Non-negative Matrix Factorization)
- BERTopic (transformer-based topic modeling)
- Dynamic topic modeling for temporal analysis
- Topic labeling and interpretation

### Model Evaluation
- Classification: accuracy, precision, recall, F1 (macro/micro/weighted)
- NER: entity-level precision, recall, F1, per-entity-type breakdown
- Topic: coherence score (C_v, C_npmi), diversity, topic overlap
- Confusion matrix and error analysis
- Cross-validation with stratified splits

## Report Bus

Write report using `save_agent_report("nlp-modeler", {...})` with:
- model type and architecture
- training configuration (epochs, learning rate, batch size)
- evaluation metrics (task-specific)
- confusion matrix or entity-level breakdown
- per-class/entity performance
- recommendations for improvement
