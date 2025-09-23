import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, confusion_matrix
from sklearn.preprocessing import label_binarize

def evaluate_classification(model, X, y, seed=None):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    results = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
        "recall": recall_score(y_test, y_pred, average="macro", zero_division=0),
        "f1": f1_score(y_test, y_pred, average="macro", zero_division=0)
    }
    print(results)
    # AUC
    try:
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)
            if y_prob.shape[1] == 2:
                results["auc"] = roc_auc_score(y_test, y_prob[:, 1])
            else:
                results["auc"] = roc_auc_score(y_test, y_prob, multi_class="ovr")
    except Exception:
        results["auc"] = None

    # ROC & CM
    try:
        classes = np.unique(y_test)
        if len(classes) == 2:
            fpr, tpr, _ = roc_curve(y_test, y_prob[:, 1])
            results["roc"] = {"binary": [[float(a), float(b)] for a, b in zip(fpr, tpr)]}
        else:
            y_bin = label_binarize(y_test, classes=classes)
            roc_dict = {}
            for i, cls in enumerate(classes):
                fpr, tpr, _ = roc_curve(y_bin[:, i], y_prob[:, i])
                roc_dict[str(cls)] = [[float(a), float(b)] for a, b in zip(fpr, tpr)]
            results["roc"] = roc_dict
        results["cm"] = confusion_matrix(y_test, y_pred).tolist()
    except Exception:
        results["roc"], results["cm"] = {}, []

    return results
