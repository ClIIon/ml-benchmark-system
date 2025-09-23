import numpy as np

def evaluate_dim_reduction(model, X, seed=None):
    X_2d = model.fit_transform(X)
    results = {
        "scatter": X_2d[:, :2].tolist()  # 仅取前两个主成分做可视化
    }

    if hasattr(model, "explained_variance_ratio_"):
        evr = model.explained_variance_ratio_
        results["Explained Variance Ratio"] = evr.tolist()
        results["Cumulative EVR"] = float(np.cumsum(evr)[-1])
    print(results)
    return results
