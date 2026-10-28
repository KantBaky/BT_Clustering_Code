import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.preprocessing import normalize
from sklearn_extra.cluster import KMedoids


N_CLUSTERS = 3
RANDOM_STATE = 40
N_INIT = 10

KMEANS_METRICS = (
    ("davies_bouldin", "Davies-Bouldin Index"),
    ("silhouette", "Silhouette Score"),
    ("calinski_harabasz", "Calinski-Harabasz Index"),
    ("inertia", "Inertia"),
)
KMEDOIDS_METRICS = KMEANS_METRICS


def _prepare_embedding(embedding):
    matrix = np.asarray(embedding, dtype=float)
    if matrix.ndim != 2 or matrix.shape[1] == 0:
        raise ValueError(f"Expected a 2D embedding with at least one feature; received shape {matrix.shape}.")
    if not np.isfinite(matrix).all():
        raise ValueError("Embedding contains NaN or infinite values.")

    sample_indices = np.flatnonzero(np.any(matrix != 0, axis=1))
    matrix = matrix[sample_indices]
    if len(matrix) < N_CLUSTERS:
        raise ValueError(
            f"Clustering needs at least {N_CLUSTERS} nonzero rows; found {len(matrix)}."
        )
    return normalize(matrix, norm="l2"), sample_indices


def _score_clusters(matrix, labels, inertia):
    distinct_clusters = np.unique(labels).size
    scores = {
        "davies_bouldin": np.nan,
        "silhouette": np.nan,
        "calinski_harabasz": np.nan,
        "inertia": inertia,
    }
    if 1 < distinct_clusters < len(labels):
        scores["davies_bouldin"] = davies_bouldin_score(matrix, labels)
        scores["silhouette"] = silhouette_score(
            matrix, labels, metric="euclidean"
        )
        scores["calinski_harabasz"] = calinski_harabasz_score(matrix, labels)
    return scores


def _get_random_states(random_states):
    if isinstance(random_states, (int, np.integer)):
        random_states = (int(random_states),)
    else:
        random_states = tuple(random_states)
    if not random_states:
        raise ValueError("At least one random state is required.")
    return random_states


def fit_and_evaluate_runs(embedding, random_states=RANDOM_STATE):
    """Fit and score K-Means once per seed on normalized question vectors."""
    matrix, sample_indices = _prepare_embedding(embedding)

    runs = []
    for seed in _get_random_states(random_states):
        model = KMeans(
            n_clusters=N_CLUSTERS,
            random_state=seed,
            n_init=N_INIT,
            init="k-means++",
            algorithm="lloyd",
        )
        labels = model.fit_predict(matrix)
        runs.append({
            "model": model,
            "labels": labels,
            "scores": _score_clusters(matrix, labels, model.inertia_),
        })
    return matrix, runs, sample_indices


def fit_and_evaluate(embedding):
    """Return the lowest-inertia K-Means run and its normalized input matrix."""
    matrix, runs, sample_indices = fit_and_evaluate_runs(embedding)
    best_run = min(runs, key=lambda run: run["scores"]["inertia"])
    return (
        matrix,
        best_run["model"],
        best_run["labels"],
        best_run["scores"],
        sample_indices,
    )


def fit_kmedoids_runs_and_evaluate(embedding, random_states=RANDOM_STATE):
    """Fit exact PAM K-Medoids once per seed on normalized question vectors."""
    matrix, sample_indices = _prepare_embedding(embedding)

    runs = []
    for seed in _get_random_states(random_states):
        model = KMedoids(
            n_clusters=N_CLUSTERS,
            metric="euclidean",
            method="pam",
            init="k-medoids++",
            random_state=seed,
        )
        labels = model.fit_predict(matrix)
        runs.append({
            "model": model,
            "labels": labels,
            "scores": _score_clusters(matrix, labels, model.inertia_),
        })
    return matrix, runs, sample_indices


def fit_kmedoids_and_evaluate(embedding):
    """Return the lowest-inertia PAM run on normalized question vectors."""
    matrix, runs, sample_indices = fit_kmedoids_runs_and_evaluate(embedding)
    best_run = min(runs, key=lambda run: run["scores"]["inertia"])
    return (
        matrix,
        matrix,
        sample_indices,
        best_run["model"],
        best_run["labels"],
        best_run["scores"],
    )


def mean_std(values):
    """Return mean and sample standard deviation, ignoring undefined scores."""
    values = np.asarray(list(values), dtype=float)
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return np.nan, np.nan
    return float(np.mean(values)), float(np.std(values, ddof=1)) if len(values) > 1 else 0.0


def format_mean_std(values, precision=4):
    mean, standard_deviation = mean_std(values)
    if not np.isfinite(mean):
        return f"{'nan':>{precision + 3}} ± {'nan':>{precision + 3}}"
    return f"{mean:.{precision}f} ± {standard_deviation:.{precision}f}"


def purity_score(true_labels, cluster_labels):
    true_labels = np.asarray(true_labels)
    cluster_labels = np.asarray(cluster_labels)
    if len(true_labels) != len(cluster_labels):
        raise ValueError("True labels and cluster labels must have the same number of rows.")

    valid = true_labels >= 0
    true_labels = true_labels[valid]
    cluster_labels = cluster_labels[valid]
    if len(true_labels) == 0:
        return np.nan

    correct = sum(
        np.bincount(true_labels[cluster_labels == cluster_id]).max()
        for cluster_id in np.unique(cluster_labels)
    )
    return correct / len(cluster_labels)