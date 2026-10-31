# Flavor-Aware Healthier Recipe Substitution (Roadmap v2)

A computational research pipeline to build and evaluate a flavor-aware, healthier recipe substitution system.

Based on the project specification: [`Agent Roadmap v2 Flavor-Aware Healthier Recipe Substitution.pdf`](./Agent%20Roadmap%20v2%20Flavor-Aware%20Healthier%20Recipe%20Substitution.pdf).

---

## 1. Project Mission & Scope

- **Core Goal**: Given a recipe, replace 1 to 3 ingredients contributing disproportionately to specific health concerns (primary targets: **calories** and **saturated fat**; sugar and sodium *if available*) with healthier functional alternatives while maintaining:
  1. **Flavor compatibility** (via FlavorDB molecule sharing, PMI co-occurrence, and learned embeddings).
  2. **Culinary function and texture constraints** (function-safe categories, curated exclusions).
  3. **Dietary style and culinary coherence** (preserving overall dish identity).
- **Explicitly Out of Scope**: Project 2 from the proposal (constraint-aware recipe generation with a checker, LLM prompting, LoRA fine-tuning). Do not build any of it.

---

## 2. Key Definitions & Ground Rules

### 2.1 Definition of "Healthier"
- The targeted nutrient drops by **$\ge 15\%$** (relative per serving/recipe).
- Protein stays within **$20\%$** of the original.
- The dietary style is preserved (e.g., vegetarian, vegan, gluten-free).
- *All thresholds are configured centrally in `config.yaml`.*

### 2.2 Leakage Rules (Non-Negotiable)
1. **Recipe-Level Split**: Split recipes into **Train (70%)**, **Validation (15%)**, and **Test (15%)** with a fixed seed. Recipes with identical ingredient sets stay in the same split.
2. **Train Sub-Split ($S$ / $M$)**: Train set is split into:
   - **Statistics set ($S$, ~60%)**: Used to compute all statistics, frequencies, PMI, embeddings, cutoffs, and the popularity baseline.
   - **Model-training set ($M$, ~40%)**: Used solely to fit the supervised compatibility model using features derived from $S$.
3. **Evaluation Integrity**: Hyperparameters and weights tuned strictly on validation. Test set is touched only once for the final run. Human labels are used exclusively for evaluation, never for training or tuning.

### 2.3 Statistical Standards
- **Paired Bootstrap**: All method comparisons use paired bootstrap resampling ($\ge 1,000$ iterations). Differences are reported with 95% confidence intervals; a difference is significant only if the interval excludes 0.
- **Primary Comparisons (Pre-registered)**:
  - **P1**: PMI vs. Popularity baseline on hide-and-recover MRR.
  - **P2**: Supervised compatibility model vs. PMI alone.
  - **P3**: Flavor sharing vs. Random baseline on hide-and-recover MRR.
  - **P4**: Agreement of all methods with human labels (Study 1).

---

## 3. Four-Week Milestone Plan & Gates

### Week 1: Data, Cleaning, Mappings, & Coverage
- **Data Inspection**: Load and profile RecipeDB, FlavorDB, and Food.com (fallback for prototyping compatibility only). Report counts, missing values, column schemas (`reports/week1_data_inventory.md`).
- **Literature Review**: Note key findings and overlaps with prior work (Shirai et al. 2021, Bagler lab 2015).
- **Ingredient Standardization**: Normalization rules, unit-to-grams conversion, mapping to FlavorDB IDs (`data/processed/ingredient_normalization.csv`, `ingredient_master.csv`).
- **Coverage & Splits**: Establish coverage requirements; generate train/val/test and $S$/$M$ splits.
- **Hand-Check**: Review 50 random parsed recipes (target: $\ge 90\%$ accuracy).
- **Gate 1**: Verified parser, acceptable coverage, approved data splits.

### Week 2: Nutrition, Compatibility Measures, & Pair Set
- **Track A (Health)**: Nutrition calculation (quantity $\times$ nutrient density), identify high-impact ingredients, candidate generator (same-category + curated function-safe alternatives).
- **Track B (Compatibility - computed strictly on $S$)**:
  - Popularity baseline (frequency in $S$).
  - PMI co-occurrence scores (mean and max with recipe).
  - Flavor sharing (Jaccard similarity of FlavorDB molecules).
  - Learned embeddings (Word2Vec / neural representations over recipes).
  - Hide-and-recover benchmark (Top-1, Top-5, Top-10, MRR overall and per cuisine).
- **Track C (Study 1 Preparation)**: Stratify, construct, and freeze the replacement pair set (~100 Type B pairs).
- **Gate 2**: Hide-and-recover runs end-to-end, nutrition validation matches within tolerance, Study 1 pair set frozen.

### Week 3: Supervised Model, Swaps, Baselines, & Evaluation
- **Supervised Compatibility Model**: Train logistic regression on $M$ using features from $S$. (LightGBM if time).
- **Study 1 Human vs. Model**: Compute weighted Cohen's $\kappa$, resolve consensus labels, evaluate Spearman correlation, AUROC, and precision@20%.
- **Multi-Objective Scoring Function**:
  $$\text{Score} = a \cdot \Delta\text{Health} + b \cdot \text{Sim}(\text{original}) + c \cdot \text{Compat}(\text{recipe})$$
  Sweep Pareto trade-off curve on validation recipes to select operating point.
- **Substitution Pipeline**: Apply up to 3 swaps per recipe at equal weight; record before/after outcomes.
- **Baselines**: Compare against B1 (random same-category), B2 (healthiest-only), B3 (co-occurrence only), B4 (flavor sharing only), B5 (popularity-compatible), and B6 (Foodoscope API, if access granted).
- **Gate 3**: Human labels locked, model-vs-human benchmark complete, baselines evaluated on validation set.

### Week 4: Final Test Run, Analysis, & Deliverables
- **Frozen Test Run**: Single run on test set with frozen models and thresholds.
- **Statistical Analysis**: Paired bootstrap 95% CIs, per-cuisine breakdown, failure mode analysis, and null results.
- **10 Transformed Recipe Showcases**: Detailed before/after nutrient and compatibility breakdown.
- **Deliverables**: Final report, slides (10-12 slides), interactive demo notebook (web demo if time), and reproducibility scripts.
- **Gate 4 (Final)**: All deliverables in place, verified runnable in clean environment.

---

## 4. Study 1: Manual Pair Labelling (Professor's Requirement)

To provide ground-truth validation of culinary plausibility beyond hide-and-recover:
- **Type B (Replacement Pairs - MUST, ~100 pairs)**: Original ingredient, candidate replacement, and recipe context.
- **Type A (Compatibility Pairs - IF TIME, ~40 pairs)**: Pairwise compatibility without specific replacement context.
- **Stratified Sampling**: 4 quadrants based on Candidate-to-Rest PMI ($\text{High}/\text{Low}$) $\times$ Candidate-to-Original Flavor Jaccard ($\text{High}/\text{Low}$), plus 10 sanity good and 10 sanity bad anchors.
- **Scale**: `1` (does not work), `2` (possible/unusual), `3` (works well), and `?` (unknown).
- **Blinded Protocol**: Raters label independently with hidden answer keys; agreement quantified via weighted Cohen's $\kappa$.

---

## 5. Repository Structure

```text
├── README.md                                                   <- Project overview, run order, seeds, and versions
├── config.yaml                                                 <- Thresholds, seeds, paths, nutrient parameters
├── Agent Roadmap v2 Flavor-Aware Healthier Recipe Substitution.pdf <- Official roadmap specification
├── data/
│   ├── raw/                                                    <- Unmodified source datasets (RecipeDB, FlavorDB, etc.)
│   └── processed/                                              <- Cleaned tables, mappings, train/val/test & S/M splits
├── src/                                                        <- Modular source code
│   ├── parsing/                                                <- Ingredient line parsing and unit-to-grams conversion
│   ├── nutrition/                                              <- Nutrition calculation and high-impact ranking
│   ├── compatibility/                                          <- PMI, Flavor Jaccard, Word2Vec, Supervised model
│   ├── candidates/                                             <- Candidate generation & function-safe filters
│   └── evaluation/                                             <- Hide-and-recover, bootstrap CI, Study 1 metrics
├── notebooks/                                                  <- Weekly exploratory and demo notebooks
├── labels/                                                     <- Study 1 pair sheets, rater sheets, hidden answer key
├── results/                                                    <- Tables, figures, bootstrap outputs, trade-off curves
└── reports/                                                    <- Weekly status notes (Gates 1-4) and final report
```

---

## 6. Software Stack & Dependencies

- **Language**: Python 3.13+
- **Data & Computation**: `pandas`, `numpy`, `scipy`
- **Machine Learning**: `scikit-learn`, `gensim` (Word2Vec) / PyTorch, `lightgbm` (optional)
- **Visualization**: `matplotlib`, `seaborn`
- **PDF & Processing**: `pypdf`
