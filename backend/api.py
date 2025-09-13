from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from datasets.loader import load_dataset
from models.registry import get_model
from pipeline import evaluate_model

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

VALID_MODELS = {
    "breast_cancer": ["logistic_regression", "decision_tree", "random_forest", "svm", "knn", "naive_bayes", "gbdt"],
    "wine": ["logistic_regression", "decision_tree", "random_forest", "svm", "knn", "naive_bayes"],
    "boston": ["linear_regression", "decision_tree", "random_forest", "gbdt"],
    "fashion_mnist": ["logistic_regression", "svm", "knn", "kmeans", "pca"],
}

def get_task(dataset, model):
    if dataset == "boston":
        return "regression"
    elif model == "kmeans":
        return "clustering"
    elif model == "pca":
        return "dim_reduction"
    else:
        return "classification"

@app.route("/benchmark", methods=["POST"])
def benchmark():
    data = request.json
    dataset_name = data.get("dataset")
    model_name = data.get("model")

    if model_name not in VALID_MODELS.get(dataset_name, []):
        return jsonify({"error": f"模型 {model_name} 不适用于数据集 {dataset_name}"}), 400

    X, y, features, targets = load_dataset(dataset_name)
    task = get_task(dataset_name, model_name)
    model = get_model(model_name, task=task)
    results = evaluate_model(model, X, y, task=task)

    return jsonify({
        "dataset": dataset_name,
        "model": model_name,
        "task": task,
        "metrics": results
    })

@socketio.on("run_benchmark")
def handle_benchmark(data):
    dataset_name = data.get("dataset")
    model_name = data.get("model")
    seed_raw = data.get("seed", None)
    if seed_raw in [None, ""]:
        seed = None
    else:
        try:
            seed = int(seed_raw)
        except ValueError:
            seed = None

    sample_size = data.get("sample_size", None)

    if model_name not in VALID_MODELS.get(dataset_name, []):
        emit("error", {"error": f"模型 {model_name} 不适用于数据集 {dataset_name}"})
        return

    emit("progress", {"status": f"开始处理 {dataset_name} - {model_name}", "percent": 10})
    X, y, features, targets = load_dataset(dataset_name, sample_size=sample_size)
    task = get_task(dataset_name, model_name)
    emit("progress", {"status": "模型训练中..."})
    model = get_model(model_name, task=task, seed=seed)
    results = evaluate_model(model, X, y, task=task, seed=seed)

    emit("result", {
        "dataset": dataset_name,
        "model": model_name,
        "task": task,
        "metrics": results
    })
    emit("progress", {"status": "任务完成 ✅"})

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)
