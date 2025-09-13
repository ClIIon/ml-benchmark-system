import numpy as np
from evaluation.classification import evaluate_classification
from evaluation.regression import evaluate_regression
from evaluation.clustering import evaluate_clustering
from evaluation.dim_reduction import evaluate_dim_reduction
from evaluation.utils import enrich_with_explanations


def evaluate_model(model, X, y=None, task="classification", seed=None):
    """
    统一评估入口
    task: classification / regression / clustering / dim_reduction
    """
    if seed is None:
        seed = np.random.randint(0, 10000)

    if task == "classification":
        results = evaluate_classification(model, X, y, seed)
    elif task == "regression":
        results = evaluate_regression(model, X, y, seed)
    elif task == "clustering":
        results = evaluate_clustering(model, X, seed)
    elif task == "dim_reduction":
        results = evaluate_dim_reduction(model, X, seed)
    else:
        raise ValueError(f"未知任务类型: {task}")

    # ✅ 增加解释性信息
    results = enrich_with_explanations(results)
    return results
