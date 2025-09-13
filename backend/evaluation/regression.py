import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def evaluate_regression(model, X, y, seed=None):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    results = {
        "MSE": mean_squared_error(y_test, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_test, y_pred)),
        "MAE": mean_absolute_error(y_test, y_pred),
        "R2": r2_score(y_test, y_pred),
        # ✅ 可视化用数据
        "residuals": (y_test - y_pred).tolist(),
        "scatter": np.column_stack([y_test, y_pred]).tolist()
    }
    return results
