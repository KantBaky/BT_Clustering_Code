from preprocessing import _get_selected_dataset_name
from tf_idf import tfidf_X
from difficulty_level import tfidf_x_dif_lev_X
from w2v_tfidf_dl import word2vec_tfidf_dl_embeddings, word2vec_embeddings, df_X_WE, tfidf_wordEmb
from true_labels import true_labels_3, true_labels_6

import numpy as np
from clustering_metrics import (
    KMEANS_METRICS,
    fit_and_evaluate_runs,
    format_mean_std,
    purity_score,
)

# ── Print selected dataset ─────────────────────────────────────────────────
print(f"\nSelected dataset: {_get_selected_dataset_name()}")

# ── List all embeddings with descriptive names ──────────────────────────────
embeddings = [
    ("TF‑IDF", tfidf_X),
    ("TF‑IDF + Difficulty", tfidf_x_dif_lev_X),
    ("TF‑IDF + WordEmb", tfidf_wordEmb),
    ("Word2Vec (average)", df_X_WE),
    ("Word2Vec", word2vec_embeddings),
    ("Word2Vec + TF‑IDF + Diff", word2vec_tfidf_dl_embeddings)
]

# ── Convert true labels to numpy arrays ─────────────────────────────────────
true_3 = np.array(true_labels_3)
true_6 = np.array(true_labels_6)

# ── Store results ────────────────────────────────────────────────────────────
results = []

for name, X_raw in embeddings:
    raw_matrix = np.asarray(X_raw, dtype=float)
    if len(raw_matrix) != len(true_3) or len(raw_matrix) != len(true_6):
        raise ValueError(
            f"{name} has {len(raw_matrix)} question rows, but the selected worksheet has "
            f"{len(true_3)} 3-class and {len(true_6)} 6-class labels."
        )
    _, runs, sample_indices = fit_and_evaluate_runs(raw_matrix)
    pur3 = [
        purity_score(true_3[sample_indices], run["labels"])
        for run in runs
    ]
    pur6 = [
        purity_score(true_6[sample_indices], run["labels"])
        for run in runs
    ]

    results.append({
        'Model': name,
        **{
            label: format_mean_std(
                (run["scores"][metric] for run in runs),
                precision=3,
            )
            for metric, label in KMEANS_METRICS
        },
        'Purity 3 summary': format_mean_std(pur3),
        'Purity 6 summary': format_mean_std(pur6),
    })

# ── Print summary table ──────────────────────────────────────────────────────
print("\n" + "="*90)
print("K‑Means Clustering Evaluation – All Embeddings")
print("="*90)
metric_columns = [label for _, label in KMEANS_METRICS]
headers = ["Model", *metric_columns, "Purity 3 mean ± SD", "Purity 6 mean ± SD"]
widths = [30, *(max(24, len(header) + 2) for header in metric_columns), 22, 22]
print(" ".join(f"{header:>{width}}" if i else f"{header:<{width}}"
              for i, (header, width) in enumerate(zip(headers, widths))))
print("-" * sum(widths))
for r in results:
    values = [r["Model"], *(r[label] for label in metric_columns),
              r["Purity 3 summary"], r["Purity 6 summary"]]
    print(" ".join(f"{value:>{width}}" if i else f"{value:<{width}}"
                  for i, (value, width) in enumerate(zip(values, widths))))
print("=" * sum(widths))