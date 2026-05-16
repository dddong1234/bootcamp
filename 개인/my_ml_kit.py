# my_ml_kit.py

import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_validate
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


def make_pipe(preprocessor, model):
    return Pipeline([
        ('preprocessor', preprocessor),
        ('model', model)
    ])


def evaluate_model(
    name,
    pipe,
    X_train,
    y_train,
    X_test,
    y_test,
    results=None,
    cv=5,
    scoring=None
):
    if scoring is None:
        scoring = ['accuracy', 'f1', 'precision', 'recall', 'roc_auc']

    cv_scores = cross_validate(
        pipe,
        X_train,
        y_train,
        cv=cv,
        scoring=scoring
    )

    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)

    result = {
        'name': name,
        'cv_accuracy': cv_scores['test_accuracy'].mean(),
        'cv_f1': cv_scores['test_f1'].mean(),
        'cv_precision': cv_scores['test_precision'].mean(),
        'cv_recall': cv_scores['test_recall'].mean(),
        'cv_roc_auc': cv_scores['test_roc_auc'].mean(),
        'test_accuracy': accuracy_score(y_test, y_pred),
        'test_f1': f1_score(y_test, y_pred),
        'test_precision': precision_score(y_test, y_pred),
        'test_recall': recall_score(y_test, y_pred),
    }

    if hasattr(pipe, 'predict_proba'):
        y_proba = pipe.predict_proba(X_test)[:, 1]
        result['test_roc_auc'] = roc_auc_score(y_test, y_proba)
    else:
        result['test_roc_auc'] = None

    if results is not None:
        results.append(result)

    return result, pipe


def compare_results(results, sort_by='cv_roc_auc'):
    results_df = pd.DataFrame(results)
    return results_df.sort_values(
        by=sort_by,
        ascending=False
    ).reset_index(drop=True)


def print_test_report(pipe, X_test, y_test):
    y_pred = pipe.predict(X_test)

    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

def run_model_candidates(
    models,
    preprocessor,
    X_train,
    y_train,
    X_test,
    y_test,
    results=None,
    cv=5,
    scoring=None
):
    trained_pipes = {}

    if results is None:
        results = []

    for name, model in models.items():
        print(f"Running: {name}")

        pipe = make_pipe(
            preprocessor=preprocessor,
            model=model
        )

        result, trained_pipe = evaluate_model(
            name=name,
            pipe=pipe,
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            results=results,
            cv=cv,
            scoring=scoring
        )

        trained_pipes[name] = trained_pipe

    return results, trained_pipes