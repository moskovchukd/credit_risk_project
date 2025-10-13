

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np




def plot_confusion_matrix(model, X_test_trans, y_test, labels=None, figsize=(6,6)):
    cm = confusion_matrix(y_test, model.predict(X_test_trans), labels=labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    fig, ax = plt.subplots(figsize=figsize)
    disp.plot(ax=ax)
    plt.title('Macierz pomyłek')
    return fig




def plot_feature_importances(model, feature_names, top_n=20):
    if not hasattr(model, 'feature_importances_'):
        raise ValueError('Model nie ma attribute feature_importances_')
    importances = model.feature_importances_
    idx = np.argsort(importances)[::-1][:top_n]
    fig, ax = plt.subplots(figsize=(8,6))
    ax.barh(range(len(idx)), importances[idx][::-1])
    ax.set_yticks(range(len(idx)))
    ax.set_yticklabels([feature_names[i] for i in idx[::-1]])
    ax.set_xlabel('Importance')
    ax.set_title('Top feature importances')
    return fig