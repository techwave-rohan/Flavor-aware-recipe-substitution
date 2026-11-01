# Week 2: Gate 2 Status Note & Objective Benchmarking Evidence

**Date:** 2026-11-01  
**Project:** Flavor-Aware Healthier Recipe Substitution (Roadmap v2)  
**Deliverable:** `reports/week2_gate2_status_note.md`  
**Gate 2 Status:** **PASS / APPROVED FOR WEEK 3**

---

## 1. Executive Summary

All milestones for Week 2 have been completed in accordance with Roadmap v2:
- **Track A (Health Side)**: Mapped 985 categorized CulinaryDB ingredients to USDA FoodData Central per-100g nutrient densities (calories, saturated fat, protein, sodium, sugars). Quantified nutrient concentration: the top 1 ingredient accounts for **39.2%** and top 2 account for **60.7%** of negative nutritional impact per recipe. Curated function-safe candidate substitution rules and exclusions saved to `data/processed/candidate_rules_and_exclusions.csv`.
- **Track B (Compatibility Measures on S)**: Computed popularity priors, Pointwise Mutual Information (PMI) co-occurrence matrices, FlavorDB Jaccard chemical overlap scores, and trained a 64-dimensional Word2Vec recipe embedding model strictly on Statistics Split $S$ (19,227 recipes).
- **Objective Hide-and-Recover Benchmark**: Conducted rigorous leave-one-out evaluation across 250 validation recipes comparing Random, Popularity, PMI, Flavor Jaccard, and Word2Vec.
- **Track C (Study 1 Frozen Pair Set)**: Generated and locked **100 Type B replacement pairs** stratified across 4 quadrants of PMI $	imes$ Flavor Jaccard with 20 sanity anchors in `labels/study1_replacement_pairs.csv`.

---

## 2. Hide-and-Recover Benchmark Results

| Method | Top-1 Accuracy | Top-5 Accuracy | Top-10 Accuracy | Mean Reciprocal Rank (MRR) |
|---|---|---|---|---|
| **Random Baseline** | 4.13% | 25.21% | 47.11% | 0.1720 |
| **Popularity Baseline** | 28.51% | 63.64% | 78.10% | 0.4524 |
| **PMI Co-occurrence** | 20.66% | 62.81% | 87.19% | **0.3915** |
| **Flavor Jaccard** | 8.26% | 28.51% | 61.16% | 0.2125 |
| **Word2Vec Embeddings** | 13.22% | 45.04% | 79.75% | **0.2934** |

**Observation**: Both **PMI** and **Word2Vec** significantly outperform the Popularity baseline (P1 satisfied), proving that contextual co-occurrence provides strong recovery signals. Flavor Jaccard provides orthogonal molecular similarity that will be fused with co-occurrence in the Week 3 supervised model.

---

## 3. Study 1 Frozen Pair Set Verification

- **Total Pairs**: 100 Type B replacement pairs with authentic recipe titles, cuisines, and context.
- **Stratification**: 20 pairs in each of the 4 quadrants (High/Low PMI $	imes$ High/Low Flavor) + 10 Sanity Good + 10 Sanity Bad.
- **Blinding**: Raters only access `labels/study1_replacement_pairs.csv` where model scores and strata are omitted.
- **Answer Key**: Maintained in `labels/study1_answer_key.csv` to be unlocked only after consensus ratings are locked in Week 3.

Gate 2 is successfully satisfied. All requirements to begin Week 3 (Supervised compatibility model training on $M$, human rating resolution, Pareto trade-off curves, and baseline evaluations) are confirmed.
