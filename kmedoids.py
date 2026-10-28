# kmedoids.py
import numpy as np
from preprocessing import get_preprocessed_questions, _get_selected_dataset_name
from tf_idf import tfidf_X
from difficulty_level import tfidf_x_dif_lev_X
from w2v_tfidf_dl import word2vec_tfidf_dl_embeddings, word2vec_embeddings, df_X_WE, tfidf_wordEmb
from clustering_metrics import (
    KMEDOIDS_METRICS,
    fit_kmedoids_runs_and_evaluate,
    format_mean_std,
)


# ── Print selected dataset ─────────────────────────────────────────────────
print(f"\nSelected dataset: {_get_selected_dataset_name()}")


X1 = tfidf_X
X2 = tfidf_x_dif_lev_X
X3 = tfidf_wordEmb
X4 = df_X_WE  
X5 = word2vec_embeddings
X6 = word2vec_tfidf_dl_embeddings

# Select which embedding to use
embedding_choice = 1  # Change this to 1, 2, 3, 4, 5, or 6 for each model
embeddings = [X1, X2, X3, X4, X5, X6]
if not 1 <= embedding_choice <= len(embeddings):
    raise ValueError(f"embedding_choice must be between 1 and {len(embeddings)}.")

preprocessed_questions = get_preprocessed_questions()
raw_embedding = np.asarray(embeddings[embedding_choice - 1], dtype=float)
if len(raw_embedding) != len(preprocessed_questions):
    raise ValueError(
        f"Embedding has {len(raw_embedding)} rows, but the selected dataset has "
        f"{len(preprocessed_questions)} questions."
    )

X, runs, sample_indices = fit_kmedoids_runs_and_evaluate(raw_embedding)
best_run = min(runs, key=lambda run: run["scores"]["inertia"])
kmedoids = best_run["model"]
clusters = best_run["labels"]
filtered_questions = [preprocessed_questions[index] for index in sample_indices]

# print(f"Shape of filtered X: {X.shape}")
# print(f"Unique rows in filtered X: {np.unique(X, axis=0).shape[0]}")

# # Print the clusters
# for cluster_id in range(kmedoids.n_clusters):
#     print(f"\n\033[4;1;3mCluster {cluster_id + 1}:\033[0m")
#     for row_index, question_index in enumerate(sample_indices):
#         if clusters[row_index] == cluster_id:
#             text = filtered_questions[row_index]
#             print(f"Question {question_index + 1}. {' '.join(text)}")

print("\nClustering Metrics:")
for metric, label in KMEDOIDS_METRICS:
    print(
        f"{label}: "
        f"{format_mean_std((run['scores'][metric] for run in runs), precision=3)}"
    )


# Scatter plot code
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
# Reduce X to 2D for visualization
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X)

# Scatter plot using clusters from kmedoids
plt.figure(figsize=(8, 6))
for i in range(kmedoids.n_clusters):
    cluster_indices = np.where(clusters == i)[0]
    plt.scatter(
        X_2d[cluster_indices, 0],
        X_2d[cluster_indices, 1],
        label=f'Cluster {i + 1}'
    )
# plt.title('TF-IDF K-Medoids Clusters (2D PCA)')
# # plt.title('W2V-TFPOSIDF K-Medoids Clusters (2D PCA)')
# plt.xlabel('PCA Component 1')
# plt.ylabel('PCA Component 2')
# plt.legend()
# plt.show()