# Flavor-Aware Healthier Recipe Substitution (Roadmap v2)

A computational research pipeline to build and evaluate a flavor-aware, healthier recipe substitution system.

Based on the project specification: [`Agent Roadmap v2 Flavor-Aware Healthier Recipe Substitution.pdf`](./Agent%20Roadmap%20v2%20Flavor-Aware%20Healthier%20Recipe%20Substitution.pdf).

---

## 1. Project Mission & Deliverables Summary

Given an arbitrary recipe, this pipeline replaces 1 to 2 ingredients contributing disproportionately to negative health metrics (specifically **calories** and **saturated fat**) with healthier functional alternatives while maintaining:
1. **Flavor compatibility** (via FlavorDB / Nature Flavor Network molecule sharing and PMI co-occurrence).
2. **Culinary function and texture constraints** (function-safe categories, curated substitutions, and exclusions).
3. **Dietary style and culinary coherence** (preserving overall dish identity across world cuisines).

### Completed Weekly Jupyter Notebooks:
- **Week 1**: [`notebooks/week1_data_cleaning_and_splits.ipynb`](./notebooks/week1_data_cleaning_and_splits.ipynb) — Multi-source data ingestion (CulinaryDB, USDA FoodData Central, FlavorDB), linguistic normalization engine, unit-to-grams converter, and leakage-free dataset splitting ($S$ vs. $M$).
- **Week 2**: [`notebooks/week2_nutrition_compatibility_and_pairs.ipynb`](./notebooks/week2_nutrition_compatibility_and_pairs.ipynb) — USDA macronutrient mapping, high-impact ingredient targeting, function-safe candidate generation, PMI co-occurrence, Flavor Jaccard, Word2Vec embeddings, Hide-and-Recover benchmark, and freezing Study 1 replacement pairs.
- **Week 3**: [`notebooks/week3_supervised_model_and_swaps.ipynb`](./notebooks/week3_supervised_model_and_swaps.ipynb) — Supervised Logistic Regression classifier on $M$, Study 1 human agreement evaluation (Cohen's $\kappa = 0.782$), Pareto trade-off curve sweeps, baseline benchmarking (B1–B5), and 10 showcased recipe transformations.
- **Week 4**: [`notebooks/week4_final_evaluation_and_demo.ipynb`](./notebooks/week4_final_evaluation_and_demo.ipynb) — Single frozen test run on untouched test set (6,841 recipes), 1,000 paired bootstrap 95% confidence intervals, cuisine-wise food-pairing analysis, failure modes, and an end-to-end interactive recipe substitution demo.

### Key Reports & Presentation Materials:
- **Comprehensive Research Report**: [`reports/final_research_report.md`](./reports/final_research_report.md)
- **12-Slide Final Presentation**: [`reports/presentation_slides.md`](./reports/presentation_slides.md)
- **Gate 1 Status Note**: [`reports/week1_gate1_status_note.md`](./reports/week1_gate1_status_note.md)
- **Gate 2 Status Note**: [`reports/week2_gate2_status_note.md`](./reports/week2_gate2_status_note.md)
- **Gate 3 Status Note**: [`reports/week3_gate3_status_note.md`](./reports/week3_gate3_status_note.md)
- **Data Inventory**: [`reports/week1_data_inventory.md`](./reports/week1_data_inventory.md)
- **Literature Review**: [`reports/week1_literature_note.md`](./reports/week1_literature_note.md)

---

## 2. Open Gastronomy Data Architecture

To ensure 100% open-science reproducibility without restricted database dependencies, the pipeline integrates:
- **CulinaryDB (IIIT-Delhi CoSyLab)**: 45,772 recipes with 20+ regional cuisines and 985 categorized ingredients (`data/raw/culinarydb/`).
- **USDA FoodData Central SR Legacy**: 7,793 standard reference foods with laboratory-verified nutrients per 100g (`data/raw/usda/`).
- **FlavorDB & Nature Flavor Network**: Chemical compound profiles mapped to culinary foods (`data/raw/flavordb.csv` & `data/raw/flavor_network/`).
- **Food.com**: 231k recipes used for empirical co-occurrence prior scaling.

---

## 3. Key Research Findings & Benchmarks

### Primary Statistical Comparisons (1,000 Paired Bootstrap 95% CIs on Test Set):
- **P1 (PMI vs. Popularity MRR)**: Mean Diff = +0.0362, 95% CI [-0.0179, +0.0864] (*Difference within noise; unconditioned popularity remains highly competitive*).
- **P2 (Supervised Model vs. PMI AUROC)**: Mean Diff = +0.0642, 95% CI [+0.0410, +0.0875] (**Statistically Significant**).
- **P3 (Flavor Jaccard vs. Random MRR)**: Mean Diff = +0.0313, 95% CI [+0.0050, +0.0568] (**Statistically Significant**).
- **P4 (Model vs. Random on Humans)**: Mean Diff = +0.3700, 95% CI [+0.2150, +0.5250] (**Statistically Significant**).

### Substitution Outcomes (Test Set):
- **Caloric Reduction**: **-24.8%** (comfortably exceeding the 15% threshold).
- **Saturated Fat Reduction**: **-38.5%**.
- **Compliance with Health Criterion**: **92.4%** of recipes.
- **Protein Preservation**: **91.8%** stay within $\pm 20\%$ of original recipe.
- **Culinary Plausibility (Model Prob)**: **0.826** (vs. 0.324 for Healthiest-Only B2).

---

## 4. Reproducibility & Environment

- **Python**: 3.13+
- **Core Dependencies**: `pandas`, `numpy`, `scipy`, `scikit-learn`, `gensim==4.4.0`, `pyyaml`, `pypdf`
- **Random Seed**: Fixed at `42` across all splits, models, and resamples in `config.yaml`.
- **Run Order**:
  1. Open and execute `notebooks/week1_data_cleaning_and_splits.ipynb`
  2. Open and execute `notebooks/week2_nutrition_compatibility_and_pairs.ipynb`
  3. Open and execute `notebooks/week3_supervised_model_and_swaps.ipynb`
  4. Open and execute `notebooks/week4_final_evaluation_and_demo.ipynb`
