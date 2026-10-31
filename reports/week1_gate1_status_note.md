# Week 1: Gate 1 Status Note & Progress Report

**Date:** 2026-10-31  
**Project:** Flavor-Aware Healthier Recipe Substitution (Roadmap v2)  
**Deliverable:** `reports/week1_gate1_status_note.md`  
**Gate 1 Decision:** **PASS / READY FOR CONFIRMATION**

---

## 1. Executive Summary

In accordance with Section 3 ("Week 1: data, cleaning, mappings, coverage") of the project roadmap, all foundational data engineering, literature review, normalization, unit conversion, and leakage-free dataset splitting tasks have been executed with strict verification against leakage and methodology requirements.

### Key Deliverables Produced:
1. **Data Inventory Report**: [`reports/week1_data_inventory.md`](file:///c:/Aware%20Healthier%20Recipe%20Substitution/reports/week1_data_inventory.md)
   - Profiled Food.com dataset (231,637 recipes, 12 columns, 0% missing on core fields).
   - Documented the exact structure of `nutrition` (recipe-level 7-float vector: calories, total fat, sugar, sodium, protein, saturated fat, carbohydrates) and `tags` (regional cuisines and dietary labels).
   - Confirmed roadmap rule: Food.com is used strictly for co-occurrence and compatibility prototyping, never for ingredient-level health calculations.
2. **Literature Review & Novelty Positioning**: [`reports/week1_literature_note.md`](file:///c:/Aware%20Healthier%20Recipe%20Substitution/reports/week1_literature_note.md)
   - Reviewed Bagler et al. (2015, negative food pairing in Indian cuisine) and Shirai et al. (2021, Knowledge Graph substitutions).
   - Positioned our contribution: a controlled multi-objective health optimization pipeline evaluated under paired bootstrap intervals and human validation (Study 1).
3. **Ingredient Normalization Engine**: [`src/parsing/clean_ingredients.py`](file:///c:/Aware%20Healthier%20Recipe%20Substitution/src/parsing/clean_ingredients.py) & [`data/processed/ingredient_normalization.csv`](file:///c:/Aware%20Healthier%20Recipe%20Substitution/data/processed/ingredient_normalization.csv)
   - Extracted 9,502 raw ingredient strings from training recipes; mapped them into standardized tokens using deterministic disambiguation, compound splitting, preparation word stripping, and singularization rules.
4. **Unit-to-Grams Converter**: [`src/parsing/unit_converter.py`](file:///c:/Aware%20Healthier%20Recipe%20Substitution/src/parsing/unit_converter.py)
   - Supports metric and US customary units (mass and volume) with culinary density baselines and handles mixed fractions (e.g., "1 1/2 cups").
5. **Leakage-Free Dataset Splits**: [`src/parsing/create_splits.py`](file:///c:/Aware%20Healthier%20Recipe%20Substitution/src/parsing/create_splits.py) & [`data/processed/recipe_splits.csv`](file:///c:/Aware%20Healthier%20Recipe%20Substitution/data/processed/recipe_splits.csv)
   - Grouped identical recipe ingredient sets via canonical MD5 signatures.
   - Partitioned into **Train (70%)**, **Validation (15%)**, and **Test (15%)**.
   - Sub-partitioned Train into **Statistics Set $S$ (60%)** and **Model Set $M$ (40%)**.
   - Ensures all vocabulary, co-occurrence, PMI, and cutoffs are computed strictly from $S$, with $M$ reserved for training the supervised model.
6. **50-Recipe Hand-Check Audit**: [`reports/week1_hand_check_50_recipes.md`](file:///c:/Aware%20Healthier%20Recipe%20Substitution/reports/week1_hand_check_50_recipes.md)
   - 476 ingredient lines across 50 randomly sampled recipes from `train_stats_S` were audited line-by-line.
   - Parsing and normalization accuracy achieved: **100.0%** (exceeding the $\ge 90\%$ gate requirement).

---

## 2. Gate 1 Evaluation Checklist

| Requirement | Target | Achieved | Status |
|---|---|---|---|
| Hand-checked parsing accuracy | $\ge 90\%$ | **100.0%** (476/476 lines) | **PASSED** |
| Dataset splits strictly leakage-free | No identical recipes across splits | Enforced via canonical signature clustering | **PASSED** |
| Statistics Set $S$ and Model Set $M$ separated | $S \approx 60\%$, $M \approx 40\%$ of train | $S = 60.0\%$, $M = 40.0\%$ | **PASSED** |
| Central configuration file | Placeholders & seeds in one file | Maintained in `config.yaml` | **PASSED** |
| Code modularity | `src/`, `data/`, `reports/` layout | Initialized and structured | **PASSED** |

---

## 3. Questions to Confirm with the Professor

To begin Week 2 smoothly:
1. **RecipeDB Data Access**: Bulk database dump vs. REST API (and potential rate limits).
2. **Nutrients Available per Ingredient**: Does RecipeDB supply explicit nutrient densities (calories, saturated fat, protein per 100g) for all ingredients?
3. **Servings**: Are servings explicitly specified in RecipeDB, or should changes be computed as whole-recipe percentage deltas?
4. **RecipeDB to FlavorDB Mapping**: Is there an existing ID crosswalk table between RecipeDB ingredients and FlavorDB molecule profiles, or should we build an entity-resolution matcher?
5. **Healthier Thresholds**: Confirm placeholder criteria ($\ge 15\%$ reduction in target negative nutrient, $\pm 20\%$ protein retention, dietary style preservation).
6. **Study 1 Labelling Protocol**: Confirm agreement on ~100 Type B replacement pairs evaluated on a 1-3 scale with recipe context.
