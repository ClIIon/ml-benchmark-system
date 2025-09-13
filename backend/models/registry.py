from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

MODEL_REGISTRY = {}

def register_model(name):
    def decorator(fn):
        MODEL_REGISTRY[name] = fn
        return fn
    return decorator

@register_model("logistic_regression")
def logistic_regression(task=None, seed=None, **kwargs):
    return LogisticRegression(max_iter=1000, random_state=seed, **kwargs)

@register_model("linear_regression")
def linear_regression(task=None, seed=None, **kwargs):
    return LinearRegression(**kwargs)

@register_model("decision_tree")
def decision_tree(task=None, seed=None, **kwargs):
    if task == "classification":
        return DecisionTreeClassifier(random_state=seed, **kwargs)
    else:
        return DecisionTreeRegressor(random_state=seed, **kwargs)

@register_model("random_forest")
def random_forest(task=None, seed=None, **kwargs):
    if task == "classification":
        return RandomForestClassifier(random_state=seed, **kwargs)
    else:
        return RandomForestRegressor(random_state=seed, **kwargs)

@register_model("gbdt")
def gbdt(task=None, seed=None, **kwargs):
    if task == "classification":
        return GradientBoostingClassifier(random_state=seed, **kwargs)
    else:
        return GradientBoostingRegressor(random_state=seed, **kwargs)

@register_model("svm")
def svm(task=None, seed=None, **kwargs):
    return SVC(probability=True, random_state=seed, **kwargs)

@register_model("knn")
def knn(task=None, seed=None, **kwargs):
    return KNeighborsClassifier(**kwargs)

@register_model("naive_bayes")
def naive_bayes(task=None, seed=None, **kwargs):
    return GaussianNB(**kwargs)

@register_model("kmeans")
def kmeans(task=None, seed=None, **kwargs):
    return KMeans(n_clusters=3, random_state=seed, **kwargs)

@register_model("pca")
def pca(task=None, seed=None, **kwargs):
    return PCA(n_components=2, random_state=seed, **kwargs)

def get_model(name, **kwargs):
    if name not in MODEL_REGISTRY:
        raise ValueError(f"未知模型: {name}")
    return MODEL_REGISTRY[name](**kwargs)
