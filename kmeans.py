from preprocessing import get_preprocessed_questions, _get_selected_dataset_name
import tf_idf
import difficulty_level
from w2v_tfidf_dl import word2vec_tfidf_dl_embeddings, word2vec_embeddings, df_X_WE, tfidf_wordEmb
from clustering_metrics import KMEANS_METRICS, fit_and_evaluate_runs, format_mean_std


# ── Print selected dataset ─────────────────────────────────────────────────
print(f"\nSelected dataset: {_get_selected_dataset_name()}")


X1 = getattr(tf_idf, 'tfidf_X', [])
X2 = getattr(difficulty_level, 'tfidf_x_dif_lev_X', [])
X3 = tfidf_wordEmb
X4 = df_X_WE
X5 = word2vec_embeddings
X6 = word2vec_tfidf_dl_embeddings

# Select which embedding to use
embedding_choice = X1  # Change this to X1, X2, X3, X4, X5, or X6 for each model

# Load preprocessed questions (ensures cache or fetch happens here)
preprocessed_questions = get_preprocessed_questions()

if not hasattr(embedding_choice, '__len__') or len(embedding_choice) == 0:
    print("No embedding data available. Ensure data sources are accessible or precompute/cache data.")
    raise SystemExit(1)
if len(embedding_choice) != len(preprocessed_questions):
    raise ValueError(
        f"Embedding has {len(embedding_choice)} rows, but the selected dataset has "
        f"{len(preprocessed_questions)} questions."
    )

X, runs, _ = fit_and_evaluate_runs(embedding_choice)
best_run = min(runs, key=lambda run: run["scores"]["inertia"])
kmeans = best_run["model"]
clusters = best_run["labels"]

print("\n\033[4;1;3mK-Means:\033[0m")

# # Print the clusters
# for i in range(n_clusters):
#     print(f"\n\033[4;1;3mCluster {i + 1}:\033[0m")
#     # for j, text in enumerate(np.array(preprocessed_questions)[clusters == i]):
#     cluster_texts = [preprocessed_questions[j] for j in range(len(preprocessed_questions)) if clusters[j] == i]
#     for j, text in enumerate(cluster_texts):
#         question_number = preprocessed_questions.index(text) + 1
#         print(f"Question {question_number}. {' '.join(text)}")


# Evaluation metrics calculation
print("\nClustering Metrics:")
for metric, label in KMEANS_METRICS:
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

cluster_labels = clusters

# Scatter plot
plt.figure(figsize=(8, 6))
for i in range(kmeans.n_clusters):
    plt.scatter(
        X_2d[cluster_labels == i, 0],
        X_2d[cluster_labels == i, 1],
        label=f'Cluster {i + 1}'
    )
# plt.title('TF-IDF K-Means Clusters (2D PCA)')
# # plt.title('W2V-TFPOSIDF K-Means Clusters (2D PCA)')
# plt.xlabel('PCA Component 1')
# plt.ylabel('PCA Component 2')
# plt.legend()
# plt.show()
