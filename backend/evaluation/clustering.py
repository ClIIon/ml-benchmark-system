import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

def evaluate_clustering(model, X, seed=None):
    model.fit(X)
    results = {}

    if hasattr(model, "labels_"):
        labels = model.labels_
        results["silhouette"] = silhouette_score(X, labels)
        results["calinski"] = calinski_harabasz_score(X, labels)
        results["davies_bouldin"] = davies_bouldin_score(X, labels)
    else:
        labels = np.zeros(len(X))  # 如果模型没有 labels_
    
    # ✅ 2D PCA 用于可视化
    pca = PCA(n_components=2, random_state=seed)
    X_2d = pca.fit_transform(X)
    results["scatter"] = np.column_stack([X_2d, labels]).tolist()

    return results
