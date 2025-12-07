

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (confusion_matrix, ConfusionMatrixDisplay,
                              roc_curve, auc, precision_recall_curve,
                              classification_report, roc_auc_score)
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import learning_curve
import numpy as np
import pandas as pd
import os




def plot_confusion_matrix(model, X_test_trans, y_test, labels=None, figsize=(6,6)):
    cm = confusion_matrix(y_test, model.predict(X_test_trans), labels=labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    fig, ax = plt.subplots(figsize=figsize)
    disp.plot(ax=ax, cmap='Blues')
    plt.title('Macierz pomyłek (Confusion Matrix)')
    plt.tight_layout()
    return fig




def plot_feature_importances(model, feature_names, top_n=20):
    if not hasattr(model, 'feature_importances_'):
        raise ValueError('Model nie ma attribute feature_importances_')
    importances = model.feature_importances_
    idx = np.argsort(importances)[::-1][:top_n]
    fig, ax = plt.subplots(figsize=(10,6))
    colors = plt.cm.viridis(np.linspace(0, 1, len(idx)))
    ax.barh(range(len(idx)), importances[idx][::-1], color=colors[::-1])
    ax.set_yticks(range(len(idx)))
    ax.set_yticklabels([feature_names[i] for i in idx[::-1]])
    ax.set_xlabel('Importance')
    ax.set_title(f'Top {top_n} Feature Importances')
    plt.tight_layout()
    return fig




def plot_roc_curves(results, X_test_trans, y_test):
    """Plot ROC curves for all models (binary or multi-class)"""
    n_classes = len(np.unique(y_test))
    fig, ax = plt.subplots(figsize=(10, 8))

    if n_classes == 2:
        # Binary classification
        for name, result in results.items():
            model = result['model']
            if hasattr(model, 'predict_proba'):
                y_proba = model.predict_proba(X_test_trans)[:, 1]
                fpr, tpr, _ = roc_curve(y_test, y_proba)
                roc_auc = auc(fpr, tpr)
                ax.plot(fpr, tpr, label=f'{name} (AUC = {roc_auc:.3f})', linewidth=2)

        ax.plot([0, 1], [0, 1], 'k--', label='Random Classifier', linewidth=1)
        ax.set_xlabel('False Positive Rate', fontsize=12)
        ax.set_ylabel('True Positive Rate', fontsize=12)
        ax.set_title('ROC Curves - Binary Classification', fontsize=14)
    else:
        # Multi-class classification - use One-vs-Rest approach
        y_test_bin = label_binarize(y_test, classes=np.unique(y_test))

        for name, result in results.items():
            model = result['model']
            if hasattr(model, 'predict_proba'):
                y_proba = model.predict_proba(X_test_trans)

                # Compute ROC curve and AUC for each class
                fpr = dict()
                tpr = dict()
                roc_auc = dict()

                for i in range(n_classes):
                    fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_proba[:, i])
                    roc_auc[i] = auc(fpr[i], tpr[i])

                # Compute micro-average ROC curve
                fpr_micro, tpr_micro, _ = roc_curve(y_test_bin.ravel(), y_proba.ravel())
                roc_auc_micro = auc(fpr_micro, tpr_micro)

                ax.plot(fpr_micro, tpr_micro,
                       label=f'{name} (micro-avg AUC = {roc_auc_micro:.3f})',
                       linewidth=2)

        ax.plot([0, 1], [0, 1], 'k--', label='Random Classifier', linewidth=1)
        ax.set_xlabel('False Positive Rate', fontsize=12)
        ax.set_ylabel('True Positive Rate', fontsize=12)
        ax.set_title('ROC Curves - Multi-class (Micro-average)', fontsize=14)

    ax.legend(loc='lower right')
    ax.grid(alpha=0.3)
    plt.tight_layout()
    return fig




def plot_precision_recall_curves(results, X_test_trans, y_test):
    """Plot Precision-Recall curves for all models"""
    n_classes = len(np.unique(y_test))
    fig, ax = plt.subplots(figsize=(10, 8))

    if n_classes == 2:
        # Binary classification
        for name, result in results.items():
            model = result['model']
            if hasattr(model, 'predict_proba'):
                y_proba = model.predict_proba(X_test_trans)[:, 1]
                precision, recall, _ = precision_recall_curve(y_test, y_proba)
                ax.plot(recall, precision, label=name, linewidth=2)

        ax.set_xlabel('Recall', fontsize=12)
        ax.set_ylabel('Precision', fontsize=12)
        ax.set_title('Precision-Recall Curves - Binary Classification', fontsize=14)
    else:
        # Multi-class
        y_test_bin = label_binarize(y_test, classes=np.unique(y_test))

        for name, result in results.items():
            model = result['model']
            if hasattr(model, 'predict_proba'):
                y_proba = model.predict_proba(X_test_trans)

                # Compute micro-average precision-recall curve
                precision_micro, recall_micro, _ = precision_recall_curve(
                    y_test_bin.ravel(), y_proba.ravel()
                )
                ax.plot(recall_micro, precision_micro, label=f'{name} (micro-avg)', linewidth=2)

        ax.set_xlabel('Recall', fontsize=12)
        ax.set_ylabel('Precision', fontsize=12)
        ax.set_title('Precision-Recall Curves - Multi-class (Micro-average)', fontsize=14)

    ax.legend(loc='best')
    ax.grid(alpha=0.3)
    plt.tight_layout()
    return fig




def plot_model_comparison(results):
    """Bar chart comparing model accuracies"""
    fig, ax = plt.subplots(figsize=(10, 6))

    models = list(results.keys())
    accuracies = [results[m]['accuracy'] for m in models]

    colors = plt.cm.viridis(np.linspace(0, 1, len(models)))
    bars = ax.bar(models, accuracies, color=colors, alpha=0.8, edgecolor='black')

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_xlabel('Model', fontsize=12)
    ax.set_title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 1.0)
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig




def plot_learning_curve(model, X, y, cv=5, figsize=(10, 6)):
    """Plot learning curves to diagnose bias/variance"""
    train_sizes, train_scores, val_scores = learning_curve(
        model, X, y, cv=cv, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10),
        scoring='accuracy'
    )

    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)

    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(train_sizes, train_mean, label='Training score', color='blue', marker='o')
    ax.fill_between(train_sizes, train_mean - train_std, train_mean + train_std,
                     alpha=0.15, color='blue')

    ax.plot(train_sizes, val_mean, label='Cross-validation score', color='red', marker='s')
    ax.fill_between(train_sizes, val_mean - val_std, val_mean + val_std,
                     alpha=0.15, color='red')

    ax.set_xlabel('Training Set Size', fontsize=12)
    ax.set_ylabel('Accuracy Score', fontsize=12)
    ax.set_title('Learning Curve', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(alpha=0.3)
    plt.tight_layout()
    return fig




def plot_data_distribution(df, target_col='Risk', figsize=(15, 10)):
    """Plot distributions of features and target variable"""
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if target_col in num_cols:
        num_cols.remove(target_col)

    n_cols = min(4, len(num_cols))
    n_rows = (len(num_cols) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten() if len(num_cols) > 1 else [axes]

    for idx, col in enumerate(num_cols):
        if idx < len(axes):
            axes[idx].hist(df[col].dropna(), bins=30, color='skyblue', edgecolor='black', alpha=0.7)
            axes[idx].set_title(col, fontsize=10)
            axes[idx].set_xlabel('Value')
            axes[idx].set_ylabel('Frequency')
            axes[idx].grid(alpha=0.3)

    # Hide unused subplots
    for idx in range(len(num_cols), len(axes)):
        axes[idx].axis('off')

    plt.suptitle('Feature Distributions', fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    return fig




def plot_target_distribution(y, figsize=(8, 6)):
    """Plot target variable distribution"""
    fig, ax = plt.subplots(figsize=figsize)

    unique, counts = np.unique(y, return_counts=True)
    colors = plt.cm.Set3(np.arange(len(unique)))

    bars = ax.bar(unique, counts, color=colors, edgecolor='black', alpha=0.8)

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)} ({height/len(y)*100:.1f}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_xlabel('Risk Class', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('Target Variable Distribution', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    return fig




def plot_correlation_matrix(df, figsize=(12, 10)):
    """Plot correlation matrix heatmap"""
    num_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[num_cols].corr()

    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=0.5,
                cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title('Feature Correlation Matrix', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    return fig




def plot_missing_values(df, figsize=(10, 6)):
    """Plot missing values for each feature"""
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if len(missing) == 0:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, 'No Missing Values!',
                ha='center', va='center', fontsize=20, fontweight='bold', color='green')
        ax.axis('off')
        return fig

    fig, ax = plt.subplots(figsize=figsize)
    colors = plt.cm.Reds(np.linspace(0.4, 0.8, len(missing)))
    bars = ax.barh(range(len(missing)), missing.values, color=colors, edgecolor='black')
    ax.set_yticks(range(len(missing)))
    ax.set_yticklabels(missing.index)
    ax.set_xlabel('Number of Missing Values', fontsize=12)
    ax.set_title('Missing Values per Feature', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)

    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{int(width)}',
                ha='left', va='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    return fig




def save_all_visualizations(results, X_test_trans, y_test, df, output_dir='visualizations'):
    """Generate and save all visualization plots"""
    os.makedirs(output_dir, exist_ok=True)

    print("Generowanie wizualizacji...")

    # Model comparison
    fig = plot_model_comparison(results)
    fig.savefig(os.path.join(output_dir, 'model_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("  ✓ Model comparison saved")

    # ROC curves
    fig = plot_roc_curves(results, X_test_trans, y_test)
    fig.savefig(os.path.join(output_dir, 'roc_curves.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("  ✓ ROC curves saved")

    # Precision-Recall curves
    fig = plot_precision_recall_curves(results, X_test_trans, y_test)
    fig.savefig(os.path.join(output_dir, 'precision_recall_curves.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("  ✓ Precision-Recall curves saved")

    # Confusion matrices for each model
    for name, result in results.items():
        fig = plot_confusion_matrix(result['model'], X_test_trans, y_test)
        fig.savefig(os.path.join(output_dir, f'confusion_matrix_{name}.png'), dpi=300, bbox_inches='tight')
        plt.close(fig)
    print("  ✓ Confusion matrices saved")

    # Feature importances for tree-based models
    for name, result in results.items():
        model = result['model']
        if hasattr(model, 'feature_importances_'):
            # Get feature names from the model
            if hasattr(model, 'feature_names_in_'):
                feature_names = model.feature_names_in_
            else:
                feature_names = [f'Feature_{i}' for i in range(len(model.feature_importances_))]

            fig = plot_feature_importances(model, feature_names, top_n=20)
            fig.savefig(os.path.join(output_dir, f'feature_importance_{name}.png'), dpi=300, bbox_inches='tight')
            plt.close(fig)
    print("  ✓ Feature importances saved")

    # Data quality visualizations
    fig = plot_target_distribution(df['Risk'])
    fig.savefig(os.path.join(output_dir, 'target_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("  ✓ Target distribution saved")

    fig = plot_data_distribution(df)
    fig.savefig(os.path.join(output_dir, 'feature_distributions.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("  ✓ Feature distributions saved")

    fig = plot_correlation_matrix(df)
    fig.savefig(os.path.join(output_dir, 'correlation_matrix.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("  ✓ Correlation matrix saved")

    fig = plot_missing_values(df)
    fig.savefig(os.path.join(output_dir, 'missing_values.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("  ✓ Missing values plot saved")

    print(f"\nWszystkie wizualizacje zapisane w folderze: {output_dir}/")
    return output_dir