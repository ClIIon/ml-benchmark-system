# 机器学习算法模型评估系统 — 使用文档 & README

> 最后更新：2025-09-13

本项目为**前后端分离**架构：后端使用 **Flask + Flask‑SocketIO** 暴露 HTTP 接口与实时推送；前端使用 **Vue 3 + Vite + Element Plus + ECharts** 提供交互与可视化。

---

## 0. 你将用到哪些工具与环境？

> 本节为工具与环境介绍。

- **VS Code**（或任意编辑器）：查看/修改代码与配置。
- **Python 3.9–3.12** + **pip**：安装并运行后端。
- **Conda/Miniconda**：隔离后端依赖环境，推荐创建独立 Python 环境（如 `conda create -n ml-benchmark python=3.10`）。
- **Node.js ≥ 18（推荐 20 LTS）** + **npm**：安装并运行前端（Vite 需要 Node ≥ 18）。
- **现代浏览器 (Chrome / Edge / Firefox / Safari)**：用于访问前端界面和查看可视化结果，推荐最新版的 Chrome 或 Edge。
- **浏览器开发者工具**：排查前端网络请求与 Socket 连接。

> 可选：
> - **nvm** 管理多版本 Node（macOS/Linux 推荐 `nvm`，Windows 可用 `nvm-windows`）。
> - **eventlet**：后端 Socket 推送更稳定的并发驱动（通过 `pip` 自动安装）。

---

## 1. 代码目录结构

```
backend/
├── api.py                # Flask + Socket.IO 服务入口（端口 5000）
├── pipeline.py           # 统一评估调度
├── datasets/
│   └── loader.py         # 数据集注册与加载
├── evaluation/           # 任务评估与可视化数据
│   ├── classification.py
│   ├── regression.py
│   ├── clustering.py
│   ├── dim_reduction.py
│   └── utils.py
└── models/
    └── registry.py       # 模型注册：LR/SVM/RF/GBDT/KMeans/PCA…

frontend/
├── node_modules
├── public
├── index.html
├── package.json          # 依赖与脚本（Vite 7, Vue 3）
├── package-lock.json
├── README.md
├── vite.config.js
└── src/
    ├── main.js
    ├── App.vue
    ├── components/
    │   ├── BenchmarkControls.vue
    │   └── BenchmarkResults.vue
    ├── services/socket.js     # ⇦ 与后端 Socket.IO 相连（默认 http://localhost:5000）
    └── visualizations/…
```

### 1.1📚 已注册数据集
后端在 backend/datasets/loader.py 中注册了以下数据集：
| 数据集名称          | 类型   | 来源/说明                                                                  |
| ------------------ | ----   | -------------------------------------------------------------------       |
| **breast\_cancer** | 分类   | scikit-learn `load_breast_cancer`（乳腺癌诊断数据）                         |
| **wine**           | 分类   | scikit-learn `load_wine`（葡萄酒成分分类）                                  |
| **boston**         | 回归   | scikit-learn `fetch_california_housing`（加州房价预测）                     |
| **fashion\_mnist** | 分类   | TensorFlow `keras.datasets.fashion_mnist`（服装图像分类）                   |
| **digits**         | 分类   | scikit-learn `load_digits`（8x8 手写数字图片）                              |
| **20newsgroups**   | 分类   | scikit-learn `fetch_20newsgroups_vectorized`（20 类新闻组，词袋模型向量）    |
| **cifar10**        | 分类   | TensorFlow `keras.datasets.cifar10`（32×32 彩色图像，10 类）                |
| **mnist**          | 分类   | TensorFlow `keras.datasets.mnist`（28×28 手写数字图片）                     |


### 1.2🤖 已注册算法模型
后端在 backend/models/registry.py 中注册了以下模型：
| 模型名称                     | 类型    | 对应实现                                                                        |
| ------------------------ | ----- | --------------------------------------------------------------------------- |
| **logistic\_regression** | 分类    | `sklearn.linear_model.LogisticRegression`                                   |
| **linear\_regression**   | 回归    | `sklearn.linear_model.LinearRegression`                                     |
| **decision\_tree**       | 分类/回归 | `sklearn.tree.DecisionTreeClassifier` / `DecisionTreeRegressor`             |
| **random\_forest**       | 分类/回归 | `sklearn.ensemble.RandomForestClassifier` / `RandomForestRegressor`         |
| **gbdt**                 | 分类/回归 | `sklearn.ensemble.GradientBoostingClassifier` / `GradientBoostingRegressor` |
| **svm**                  | 分类    | `sklearn.svm.SVC`（支持概率输出）                                                   |
| **knn**                  | 分类    | `sklearn.neighbors.KNeighborsClassifier`                                    |
| **naive\_bayes**         | 分类    | `sklearn.naive_bayes.GaussianNB`                                            |
| **kmeans**               | 聚类    | `sklearn.cluster.KMeans`                                                    |
| **pca**                  | 降维    | `sklearn.decomposition.PCA`                                                 |



---

## 2. 快速启动（本地）

### 2.1 后端（Flask + Socket.IO）

1) **进入后端目录并创建 Conda 环境**  
```bash
# 进入 backend 目录
cd backend

# 创建名为 ml-benchmark 的环境（推荐 Python 3.10）
conda create -n ml-benchmark python=3.10 -y

# 激活环境
conda activate ml-benchmark
```

2) **安装依赖**
> 代码用到的python库：`flask`, `flask-cors`, `flask-socketio`, `eventlet`, `numpy`, `scikit-learn`，以及 `TensorFlow`（用于 `mnist`/`cifar10`/`fashion_mnist` 数据集）。 
```bash
pip install -U pip
pip install flask flask-cors flask-socketio eventlet numpy scikit-learn 
```

> • Linux/Windows：`pip install tensorflow` 。  
> • Apple Silicon（M1/M2/M3）：`pip install tensorflow-macos tensorflow-metal`。


3) **启动后端**
```bash
cd backend
# 在 backend 目录下
python api.py
# 成功后监听： http://127.0.0.1:5000
```

> 说明：开发模式使用 `socketio.run(app, debug=True, port=5000)`。

---

### 2.2 前端（Vue 3 + Vite）

1) **安装 Node.js**（≥ 18，推荐 20 LTS）  
- macOS/Linux 推荐 `nvm`：`nvm install --lts && nvm use --lts`  
- Windows 可使用 [nvm-windows]

2) **安装依赖并启动**

```bash
# 进入 frontend 目录
cd frontend

# 安装依赖
npm install

# 启动开发服务（默认端口 5173）
npm run dev
```

3) **访问前端**  
打开浏览器访问 `http://localhost:5173`。前端默认尝试通过 **Socket.IO** 连接 `http://localhost:5000`。

> 如需修改后端地址，请编辑：`src/services/socket.js`：  
> ```js
> // 将硬编码替换为可配置：
> const socket = io(import.meta.env.VITE_API_BASE_URL || "http://localhost:5000");
> ```
> 然后在 `frontend/.env` 中设置：
> ```env
> VITE_API_BASE_URL=http://127.0.0.1:5000
> ```

---

## 3. 功能与数据流

- **交互入口**：`src/components/BenchmarkControls.vue`  
  - 可选数据集：`breast_cancer`、`wine`、`boston(加州房价)`、`fashion_mnist`  
  - 根据数据集自动限制可选模型（见下表）  
  - 可传 `seed`（随机种子，整数或留空），`sample_size`（仅 `fashion_mnist` 使用，抽取样本进行训练防止训练时间过长导致网页访问超时，默认 2000）

- **触发评估**：前端通过 **Socket.IO** 发送事件：`run_benchmark`  
  - 载荷（示例）：
    ```json
    {
      "dataset": "breast_cancer",
      "model": "random_forest",
      "seed": 42,
      "sample_size": null
    }
    ```
  - 后端会按进度多次 `emit("progress", {{ "status": "...", "percent": 30 }})`，完成后 `emit("result", {{ ... }})`。

- **HTTP 调用（可选）**：也可直接 `POST /benchmark`，载荷同上。

### 3.1 任务类型自动判定（来自 `api.py` 的 `get_task`）
| 条件 | 任务类型 |
|---|---|
| `dataset == "boston"` | `regression` |
| `model == "kmeans"` | `clustering` |
| `model == "pca"` | `dim_reduction` |
| 其他 | `classification` |

### 3.2 数据集 ↔ 可用模型（来自 `VALID_MODELS`）
| 数据集 | 任务 | 模型 |
|---|---|---|
| `breast_cancer` | classification | logistic_regression, decision_tree, random_forest, svm, knn, naive_bayes, gbdt |
| `wine` | classification | logistic_regression, decision_tree, random_forest, svm, knn, naive_bayes |
| `boston`（UI 显示“房价/加州”） | regression | linear_regression, decision_tree, random_forest, gbdt |
| `fashion_mnist` | classification / clustering / dim_reduction | logistic_regression, svm, knn, kmeans, pca |

> **依赖提示**：若选择 `mnist/cifar10/fashion_mnist`（或将来开启它们），需要安装 TensorFlow；`20newsgroups_vectorized` 需联网下载。

### 3.3 评估指标与返回结构

- **分类（classification）** → `accuracy`, `precision`, `recall`, `f1`，并尝试返回：
  - `roc`: ROC 曲线点集（binary 或 multiclass）
  - `cm`: 混淆矩阵（二维数组）

- **回归（regression）** → `MSE`, `RMSE`, `MAE`, `R2`，以及：
  - `residuals`: 残差序列
  - `scatter`: 真实值/预测值散点

- **聚类（clustering）** → `silhouette`, `calinski`, `davies_bouldin`，以及：
  - `scatter`: PCA 2D 降维后的点 + 聚类标签

- **降维（dim_reduction）** →
  - `scatter`: 前两主成分坐标
  - `Explained Variance Ratio` / `Cumulative EVR`（若模型提供，如 PCA）

> 返回的每个指标会被包装为：`{{ "value": 指标值, "explanation": 文字解释 }}`，便于前端表格展示与提示。

---

## 4. 接口说明

### 4.1 WebSocket / Socket.IO（前端默认使用）
- **连接地址**：`http://<backend-host>:5000`
- **事件**：
  - `run_benchmark`（客户端 → 服务端）
    - 载荷字段：`dataset`, `model`, `seed?`, `sample_size?`
  - `progress`（服务端 → 客户端）
    - 示例：`{{ "status": "数据加载中...", "percent": 30 }}`
  - `result`（服务端 → 客户端）
    - 字段：`dataset`, `model`, `task`, `metrics`（见上）
  - `error`（服务端 → 客户端）

### 4.2 HTTP
- **POST** `/benchmark`  
  - `Content-Type: application/json`
  - **Body 示例**：
    ```json
    { "dataset": "boston", "model": "gbdt", "seed": 123 }
    ```
  - **成功响应**：
    ```json
    {{
      "dataset": "boston",
      "model": "gbdt",
      "task": "regression",
      "metrics": {{ "...": "同上" }}
    }}
    ```
  - **错误响应**：`400 {{ "error": "模型 xxx 不适用于数据集 yyy" }}`

---

## 5. 如何注册新的数据集与模型

系统支持用户扩展新的`数据集`与`模型`。

### 5.1 注册新的数据集

在`backend/datasets/loader.py`使用`@register_dataset("名称")`装饰器注册：
```python
from sklearn.datasets import load_iris
from datasets.loader import register_dataset

@register_dataset("iris")
def load_iris_dataset(sample_size=None):
    data = load_iris()
    return data.data, data.target, data.feature_names, data.target_names
```

> 返回格式：`X, y, feature_names, target_names`

在`api.py`的`VALID_MODELS`中指定该数据集允许的模型：

```python
VALID_MODELS = {
    "iris": ["logistic_regression", "decision_tree", "random_forest", "svm", "knn"],
    # 其它保持不变
}
```

## 5.2 注册新的模型

在`backend/models/registry.py`使用`@register_model("名称")`装饰器注册：
```python
import xgboost as xgb
from models.registry import register_model

@register_model("xgboost")
def xgboost_classifier(task=None, seed=None, **kwargs):
    if task == "classification":
        return xgb.XGBClassifier(random_state=seed, **kwargs)
    elif task == "regression":
        return xgb.XGBRegressor(random_state=seed, **kwargs)
    else:
        raise ValueError("XGBoost 暂不支持该任务类型")
```

然后在`api.py`的`VALID_MODELS`中绑定：
```python
VALID_MODELS = {
    "breast_cancer": ["logistic_regression", "decision_tree", "random_forest", "svm", "knn", "naive_bayes", "gbdt", "xgboost"],
}
```

## 5.3 前端更新

数据集下拉框：修改`frontend/src/components/BenchmarkControls.vue`的下拉选项。

模型列表：无需手动修改，前端会根据`VALID_MODELS`自动显示。

📌 小结
1) **在 loader.py 用 @register_dataset 注册新数据集。**
2) **在 registry.py 用 @register_model 注册新模型。**
3) **在 api.py 的 VALID_MODELS 中配置映射。**
4) **在前端 BenchmarkControls.vue 增加下拉框选项。**

完成后，系统即可支持新数据集和模型，并自动出现在前端界面。


## 6. 常见问题（Troubleshooting）

- **前端按钮点击无响应 / 页面无结果**
  - 确认后端已在 **5000** 端口启动；前端默认连 `http://localhost:5000`。
  - 若后端在远端或端口不同，请修改 `src/services/socket.js` 或使用 `VITE_API_BASE_URL` 方案。

- **CORS/跨域错误**
  - 已在后端启用 `flask_cors.CORS(app)`。若自定义域名/端口仍报错，可在 CORS 中设置明确的 `allow_origins`。

- **Socket 连接失败（超时/404/握手失败）**
  - 确认使用 **同一协议与主机**（例如都用 `http://localhost`）。
  - 反向代理（Nginx）需正确转发 **WebSocket** 协议（`Upgrade` 头）。

- **TensorFlow 安装困难 / 过慢**
  - 仅使用 `breast_cancer`/`wine`/`boston` 时可以**不安装 TensorFlow**。
  - Apple Silicon 用 `tensorflow-macos + tensorflow-metal`。

- **模型可用性报错**：`模型 XXX 不适用于数据集 YYY`
  - 这是由 `VALID_MODELS` 限制的映射，请按上表选择。

---

## 7. 构建与部署（简版）

### 7.1 前端构建静态资源
```bash
cd frontend
npm run build
# 产物在 dist/ 下，可由 Nginx/静态服务器托管
```

### 7.2 后端生产运行（轻量）
```bash
cd backend
# 方式 A：直接运行（适合单机/小流量）
python api.py

# 方式 B：Gunicorn + eventlet
# pip install gunicorn eventlet
# 注：Flask‑SocketIO 官方推荐 eventlet/gevent 作为 worker
gunicorn -k eventlet -w 1 -b 0.0.0.0:5000 api:app
```

> 若置于反向代理后（如 Nginx），请确保开启 WebSocket 转发（`Upgrade`/`Connection` 头）。

---

## 8. 二次开发建议

- **把后端地址改为可配置**（见上面的 `VITE_API_BASE_URL` 示例）。
- **为数据集增加开关与体积限制**（大数据时默认采样，例如 `fashion_mnist` 的 `sample_size`）。
- **日志与监控**：在 `progress` 里统一携带百分比与阶段名，便于前端进度条更顺滑。

---

## 9. 附件

- **示例 `requirements.txt`（后端）**：参见文件 `requirements.txt`  
  ```text
  flask
  flask-cors
  flask-socketio
  eventlet
  numpy
  scikit-learn
  # TF 数据集需要：
  # tensorflow            # Linux/Windows CPU
  # tensorflow-macos      # macOS Apple Silicon
  # tensorflow-metal      # macOS Apple Silicon GPU 加速
  ```

- **示例 `.env`（前端，可选）**
  ```env
  VITE_API_BASE_URL=http://127.0.0.1:5000
  ```

---

### 启动复盘
```bash
# 后端
cd backend
conda create -n ml-benchmark python=3.10 -y
conda activate ml-benchmark
pip install -U pip flask flask-cors flask-socketio eventlet numpy scikit-learn tensorflow  # 如需 TF 数据集
python api.py  # http://127.0.0.1:5000

# 前端
cd ./frontend
npm install
npm run dev  # http://localhost:5173
