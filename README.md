Project: KMeans Clustering with Lazy Data Loading

What I changed

- Questions and levels are loaded lazily from `20_01_2022_dataset.xlsx`; Bloom keywords and adverbs are loaded from the database.
- Database calls include retries with exponential backoff and timeouts.
- Results are cached to `data_cache_<worksheet>.json` in the project directory to avoid repeated network calls.
- Preprocessed questions and Bloom verbs are stored in each dataset cache to skip repeated NLP work on later runs.
- Bloom difficulty levels are loaded in one database query, and TF-IDF uses token/document counts instead of rescanning every document.
- `difficulty_level.py` now calls the lazy loader instead of importing precomputed objects.
- `kmeans.py` checks for empty embeddings and exits gracefully with guidance.

How to run

1. Activate your virtualenv (Windows PowerShell):

```powershell
& "my_Venv\Scripts\Activate.ps1"
```

2. Run the clustering script:

```powershell
& "my_Venv\Scripts\python.exe" "kmeans.py"
```

Select a dataset

The clustering scripts use the worksheet named by `BLOOM_DATASET`. Run each dataset in a fresh Python process so its embeddings are built from that worksheet:

```powershell
$env:BLOOM_DATASET = "FSC"  # FSC, FAS, FBF, or FEGT
& ".\my_Venv\Scripts\python.exe" ".\Kmeans_Evaluation_Index.py"
& ".\my_Venv\Scripts\python.exe" ".\Kmedoids_Evaluation_index.py"
```

Each worksheet has its own cache file, tagged with its dataset name and local Excel source. If a cache is missing or belongs to another worksheet or source, the loader reads the requested worksheet from the local workbook. To explicitly refresh a dataset cache:

```powershell
$env:BLOOM_DATASET = "FAS"
& ".\my_Venv\Scripts\python.exe" -c "from preprocessing import get_preprocessed_questions; get_preprocessed_questions(force_reload=True)"
```

Force a fresh fetch (skip cache)

- From Python REPL or a script:

```python
from preprocessing import get_preprocessed_questions
get_preprocessed_questions(force_reload=True)
```

Cache file location

- Cached data is written to a worksheet-specific file next to `preprocessing.py`: `data_cache_fsc.json`, `data_cache_fas.json`, `data_cache_fbf.json`, or `data_cache_fegt.json`.
- To clear a cache, delete the file for the worksheet you want to reload.

Setup

Install the Excel workbook reader in the project environment:

```powershell
& ".\my_Venv\Scripts\python.exe" -m pip install openpyxl
```

Behavior notes

- If the DB cannot be reached, the loader will retry up to 3 times with exponential backoff. Partial results (if any) are cached.
- If no embedding data is available when running `kmeans.py`, the script will exit with a clear message instructing you to check the data sources.

Troubleshooting

- Missing workbook: ensure `20_01_2022_dataset.xlsx` is next to `preprocessing.py` and contains the worksheet selected by `BLOOM_DATASET`.
- DB connection issues: confirm the `bloom_taxonomy` database and tables exist and that the MySQL server is running.
- If you expect no network/DB access, pre-generate the matching `data_cache_<worksheet>.json` with the expected structure:

```json
{
  "dataset": "FAS",
  "questions": ["Q1, ...", "Q2, ..."],
  "bloom_keywords": ["remember", "calculate"],
  "adverbs": ["carefully", "briefly"],
  "timestamp": 1690000000
}
```

Next steps I can do (pick any):

- Add structured logging to `preprocessing.py` (file + console).
- Add unit tests for the loader and cache behavior.
- Improve cache invalidation policy (TTL-based).

If you want, I can add logging and a small test now.
