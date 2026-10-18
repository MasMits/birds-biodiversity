# Birds biodiversity

Descriptive analysis of Martinique bird observations, 2014–2025.

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_notebook.py
```

Or open `notebooks/01_data_preparation_and_indicators.ipynb` in an editor with
Jupyter support, select this environment and run all cells. The notebook can run
from the project root or the `notebooks/` directory.

The notebook contains the whole analysis: loading, cleaning, point-survey
indicators, annual means and plots. The runner only executes and saves it.
The notebook includes generated tables and figures; running it refreshes them.
Its plots share the presentation style and use a dark background for viewing.
Generated CSVs and PNGs are excluded from Git.

- Input: `data/raw/Observations 2012-2025.xlsx` (read-only).
- Tables: `data/processed/` and `results/`.
- Plots: `figures/`.

For separate presentation charts with green accents (`#75CB6D`), run
`python scripts/plot_figures.py` after the notebook. The seven transparent PNGs
are saved in `figures/presentation/`. Their light labels suit a dark slide
background, for example `#102015`.

Annual estimates average point surveys within each route/year, then give each
route equal weight. Missing or inconsistent counts invalidate a survey;
unidentified groups also invalidate richness and Shannon. Remaining repeated
species entries are summed after exact-copy removal.

This version keeps the main indicators, effort summaries, data-quality
flags and three figures. Detailed audit exports, duplicate-treatment sensitivity
analyses and environment/hash reports were removed. Output table schemas are
smaller, and point surveys use explicit route/date/visit/point columns instead of
a concatenated survey ID. Confidence intervals, trend inference and species-level
analysis remain future work; this is only the descriptive first stage.
