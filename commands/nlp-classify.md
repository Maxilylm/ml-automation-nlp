# /nlp-classify

Train a text classifier for sentiment, topic, or custom category prediction.

## Usage

```
/nlp-classify <text_data_path> [--text-column <col>] [--label-column <col>] [--task sentiment|topic|custom] [--model logistic|svm|naive-bayes|bert] [--test-split 0.2]
```

- `text_data_path`: path to CSV or JSONL with text and labels
- `--text-column`: column containing text (default: auto-detect)
- `--label-column`: column containing labels (default: auto-detect)
- `--task`: classification task type (default: custom)
- `--model`: model type (default: logistic)
- `--test-split`: test set proportion (default: 0.2)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` -- if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `nlp_utils.py` exists in `src/` -- if missing, copy from this plugin's `templates/nlp_utils.py`
3. Verify data path exists and contains text + label columns
4. Check required packages based on `--model`

### Stage 1: Data Loading and Exploration

1. Load dataset, identify text and label columns
2. Report: sample count, class distribution, class balance ratio
3. Check for missing labels, empty text entries
4. Train/test split with stratification

### Stage 2: Text Preprocessing

1. Apply standard preprocessing pipeline:
   - Lowercase, remove HTML/URLs, normalize whitespace
   - Tokenize, remove stopwords
   - Lemmatize (for traditional ML models)
2. For sentiment task: preserve negation markers, emoticons
3. Report: vocabulary size after preprocessing

### Stage 3: Feature Engineering

1. Based on `--model`:
   - **logistic / svm / naive-bayes**: TF-IDF features (unigrams + bigrams, max 10000 features)
   - **bert**: tokenize with BERT tokenizer, prepare input tensors
2. Handle class imbalance:
   - Compute class weights (inverse frequency)
   - Report imbalance ratio and strategy applied

### Stage 4: Model Training

1. **Logistic Regression**: `sklearn.linear_model.LogisticRegression` with class weights
2. **SVM**: `sklearn.svm.LinearSVC` with class weights
3. **Naive Bayes**: `sklearn.naive_bayes.MultinomialNB` with alpha tuning
4. **BERT**: fine-tune `bert-base-uncased` (or `distilbert-base-uncased`) with:
   - Learning rate: 2e-5, epochs: 3, batch size: 16
   - Linear warmup, weight decay
5. Cross-validation (5-fold stratified) for hyperparameter selection
6. Report: training time, best hyperparameters

### Stage 5: Evaluation

1. Predict on test set
2. Compute metrics:
   - Accuracy, macro F1, weighted F1
   - Per-class precision, recall, F1
   - Confusion matrix
3. Error analysis: sample misclassified examples (up to 20)
4. For sentiment: analyze borderline predictions (confidence near 0.5)
5. Report: full metrics table, confusion matrix, error examples

### Stage 6: Export

1. Save trained model to `models/text_classifier/`
2. Save preprocessing pipeline and vectorizer
3. Generate inference script `src/classify.py`
4. Generate `src/classifier_config.json`

### Stage 7: Report

```python
from ml_utils import save_agent_report
save_agent_report("nlp-modeler", {
    "status": "completed",
    "task": task_type,
    "model": model_type,
    "train_samples": train_count,
    "test_samples": test_count,
    "classes": class_list,
    "metrics": {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "per_class": per_class_metrics
    },
    "confusion_matrix": cm.tolist(),
    "misclassified_examples": error_examples[:20],
    "model_path": "models/text_classifier/",
    "recommendations": recommendations
})
```

Write results to `reports/text_classification_report.json`.
Print classification report and confusion matrix.
