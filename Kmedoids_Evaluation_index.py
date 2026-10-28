# Kmedoids_Evaluation_index.py
from preprocessing import _get_selected_dataset_name
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

# Loop through the datasets and calculate metrics
for i, embedding in enumerate([X1, X2, X3, X4, X5, X6], start=1):
    print(f"X{i}")

    _, runs, _ = fit_kmedoids_runs_and_evaluate(embedding)

    for metric, label in KMEDOIDS_METRICS:
        print(
            f"{label} for X{i}: "
            f"{format_mean_std((run['scores'][metric] for run in runs), precision=3)}"
        )
    print()