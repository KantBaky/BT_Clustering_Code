from tf_idf import tfidf_X
from preprocessing import get_preprocessed_questions, _get_selected_dataset_name
from difficulty_level import tfidf_x_dif_lev_X
from w2v_tfidf_dl import word2vec_tfidf_dl_embeddings, word2vec_embeddings, df_X_WE, tfidf_wordEmb
from clustering_metrics import KMEANS_METRICS, fit_and_evaluate_runs, format_mean_std


# ── Print selected dataset ─────────────────────────────────────────────────
print(f"\nSelected dataset: {_get_selected_dataset_name()}")
expected_rows = len(get_preprocessed_questions())

X1 = tfidf_X
X2 = tfidf_x_dif_lev_X
X3 = tfidf_wordEmb
X4 = df_X_WE
X5 = word2vec_embeddings
X6 = word2vec_tfidf_dl_embeddings

embeddings = [X1, X2, X3, X4, X5, X6]

# Fit and score each question-level embedding
for i, embedding in enumerate(embeddings, start=1):
    print(f"df{i}")
    if len(embedding) != expected_rows:
        raise ValueError(f"Embedding df{i} has {len(embedding)} rows; expected {expected_rows} questions.")
    _, runs, _ = fit_and_evaluate_runs(embedding)

    for metric, label in KMEANS_METRICS:
        print(
            f"{label} for df{i}: "
            f"{format_mean_std((run['scores'][metric] for run in runs), precision=3)}"
        )
    print()