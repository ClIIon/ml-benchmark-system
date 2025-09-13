# 统一的指标解释字典
METRIC_EXPLANATIONS = {
    # 🟢 分类任务
    "accuracy": "整体预测正确率。所有样本中被正确分类的比例。",
    "precision": "精确率：预测为某一类的样本中，有多少是真的该类。高精确率表示误报少。",
    "recall": "召回率：真实属于某类的样本中，有多少被正确识别出来。高召回率表示漏报少。",
    "f1": "F1 分数：精确率与召回率的调和平均，综合平衡两者。",
    "auc": "AUC (曲线下面积)：模型区分正负样本的能力，越接近 1 越好。",

    # 🟠 回归任务
    "MSE": "均方误差 (Mean Squared Error)：预测值与真实值差的平方的平均。越小越好，受异常值影响大。",
    "RMSE": "均方根误差 (Root Mean Squared Error)：MSE 的平方根，更直观地表示预测误差的大小。",
    "MAE": "平均绝对误差 (Mean Absolute Error)：预测值与真实值差的绝对值平均。越小越好，鲁棒性比 MSE 更强。",
    "R2": "决定系数 (R²)：模型拟合优度，范围通常在 [0,1]，越接近 1 表示拟合效果越好。",

    # 🔵 聚类任务
    "silhouette": "轮廓系数 (Silhouette Score)：衡量样本与同簇内样本的紧密度以及与其他簇的分离度。范围 [-1,1]，越接近 1 越好。",
    "calinski": "Calinski-Harabasz 指数：簇间方差与簇内方差的比值。值越大越好。",
    "davies_bouldin": "Davies-Bouldin 指数：衡量簇间相似度，值越小越好。",

    # 🟣 降维任务
    "Explained Variance Ratio": "解释方差比例：每个主成分对原始数据方差的贡献度。",
    "Cumulative EVR": "累计解释方差比例：前若干主成分能保留多少原始信息。越接近 1 越好。",
}

def enrich_with_explanations(results):
    """
    给评估结果增加解释字段
    """
    enriched = {}
    for key, value in results.items():
        enriched[key] = {
            "value": value,
            "explanation": METRIC_EXPLANATIONS.get(key, "")
        }
    return enriched
