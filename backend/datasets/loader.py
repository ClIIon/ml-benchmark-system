import numpy as np
from sklearn.datasets import (
    load_breast_cancer,
    load_wine,
    fetch_california_housing,
    load_digits,
    fetch_20newsgroups_vectorized,
)
from tensorflow.keras.datasets import fashion_mnist, cifar10, mnist

DATASET_REGISTRY = {}

def register_dataset(name):
    def decorator(fn):
        DATASET_REGISTRY[name] = fn
        return fn
    return decorator


# ✅ 通用采样工具
def sample_if_needed(X, y, sample_size):
    if sample_size is not None and len(X) > sample_size:
        idx = np.random.choice(len(X), size=sample_size, replace=False)
        return X[idx], y[idx]
    return X, y


@register_dataset("breast_cancer")
def load_breast_cancer_dataset(sample_size=None):
    data = load_breast_cancer()
    return data.data, data.target, data.feature_names, data.target_names


@register_dataset("wine")
def load_wine_dataset(sample_size=None):
    data = load_wine()
    return data.data, data.target, data.feature_names, data.target_names


@register_dataset("boston")
def load_boston_dataset(sample_size=None):
    data = fetch_california_housing()
    return data.data, data.target, data.feature_names, ["price"]


@register_dataset("fashion_mnist")
def load_fashion_mnist(sample_size=None):
    (X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
    X = np.concatenate([X_train, X_test]).reshape(-1, 28 * 28) / 255.0
    y = np.concatenate([y_train, y_test])
    X, y = sample_if_needed(X, y, sample_size)
    return X, y, [f"pixel_{i}" for i in range(784)], list(range(10))


@register_dataset("digits")
def load_digits_dataset(sample_size=None):
    data = load_digits()
    return data.data, data.target, [f"pixel_{i}" for i in range(data.data.shape[1])], list(range(10))


@register_dataset("20newsgroups")
def load_newsgroups_dataset(sample_size=None):
    data = fetch_20newsgroups_vectorized(subset="all")
    return (
        data.data.toarray(),
        data.target,
        [f"word_{i}" for i in range(data.data.shape[1])],
        list(range(20)),
    )


@register_dataset("cifar10")
def load_cifar10(sample_size=None):
    (X_train, y_train), (X_test, y_test) = cifar10.load_data()
    X = np.concatenate([X_train, X_test]).reshape(-1, 32 * 32 * 3) / 255.0
    y = np.concatenate([y_train, y_test]).flatten()
    X, y = sample_if_needed(X, y, sample_size)
    return X, y, [f"pixel_{i}" for i in range(32 * 32 * 3)], list(range(10))


@register_dataset("mnist")
def load_mnist(sample_size=None):
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    X = np.concatenate([X_train, X_test]).reshape(-1, 28 * 28) / 255.0
    y = np.concatenate([y_train, y_test])
    X, y = sample_if_needed(X, y, sample_size)
    return X, y, [f"pixel_{i}" for i in range(784)], list(range(10))


def load_dataset(name, **kwargs):
    if name not in DATASET_REGISTRY:
        raise ValueError(f"未知数据集: {name}")
    return DATASET_REGISTRY[name](**kwargs)
