# Week 1: Data Access and Inspection Report
**Date:** 2026-10-31
**Deliverable:** `reports/week1_data_inventory.md`
**Status:** Completed Task 1 of Week 1 according to `Agent Roadmap v2`.

## 1. Data Sources Inventory & Access Status

| Source | Description | Access Status | Storage / Location |
|---|---|---|---|
| **Food.com** | 231k recipes with recipe-level nutrition & ingredient lists | **Available** | `data/raw/RAW_recipes.csv` |
| **RecipeDB** | Recipes with gram quantities, 29 categories, 5 dietary styles | **Pending Confirmation** | API / bulk dump to confirm with professor |
| **FlavorDB** | Flavor molecules per ingredient (chemical profiles) | **Pending Mapping** | FlavorDB mapping to confirm with professor |
| **Foodoscope API** | Substitution & flavor API (Baseline B6) | **Pending Access** | Optional (IF TIME) |

## 2. Food.com Dataset Profile (`RAW_recipes.csv`)

- **Total Recipes (Rows):** 231,637
- **Total Columns:** 12

### 2.1 Columns, Dtypes, and Missing Rates

| Column Name | Data Type | Non-Null Count | Missing Count | Missing Rate (%) |
|---|---|---|---|---|
| `name` | `object` | 231,636 | 1 | 0.000% |
| `id` | `int64` | 231,637 | 0 | 0.000% |
| `minutes` | `int64` | 231,637 | 0 | 0.000% |
| `contributor_id` | `int64` | 231,637 | 0 | 0.000% |
| `submitted` | `object` | 231,637 | 0 | 0.000% |
| `tags` | `object` | 231,637 | 0 | 0.000% |
| `nutrition` | `object` | 231,637 | 0 | 0.000% |
| `n_steps` | `int64` | 231,637 | 0 | 0.000% |
| `steps` | `object` | 231,637 | 0 | 0.000% |
| `description` | `object` | 226,658 | 4,979 | 2.149% |
| `ingredients` | `object` | 231,637 | 0 | 0.000% |
| `n_ingredients` | `int64` | 231,637 | 0 | 0.000% |

### 2.2 Nutrient Availability Analysis

- **Per-Ingredient Nutrients:** **NOT AVAILABLE in Food.com.** Food.com only records recipe-level summary nutrition.
- **Per-Recipe Nutrition Format:** Vector of 7 float values stored as string `[calories, total_fat, sugar, sodium, protein, saturated_fat, carbohydrates]`.
- **Sample Raw Nutrition String:** `[51.5, 0.0, 13.0, 0.0, 2.0, 0.0, 4.0]`
- **Interpretation:** Value 0 is calories; values 1-6 are % Daily Value (PDV).
> **Important Rule from Roadmap:** Because Food.com lacks per-ingredient gram quantities and nutrient breakdowns, it **must never be used for health gain calculations**; it serves strictly as a fallback prototype for co-occurrence and compatibility measures.

### 2.3 Servings Availability

- **Servings Column Present:** `False`
- **Roadmap Rule:** When servings are absent, relative changes in target nutrients are calculated over the whole-recipe total. Since ingredient replacements are evaluated at equal weight, the percentage change is mathematically identical per serving.

### 2.4 Cuisine & Dietary Labels

- **Tag Field:** Stored in `tags` as stringified Python list.
- **Identified Cuisine & Regional Tags (Sample 10k):**
  - `cuisine`: 4,069 recipes
  - `north-american`: 2,112 recipes
  - `european`: 956 recipes
  - `asian`: 751 recipes
  - `italian`: 287 recipes
  - `mexican`: 211 recipes
  - `indian`: 110 recipes
  - `french`: 89 recipes
  - `chinese`: 61 recipes
  - `greek`: 60 recipes
  - `japanese`: 31 recipes
  - `thai`: 23 recipes

### 2.5 Ingredient Name Format

- **Raw Format:** Stringified list of strings without units or quantities. Example: `['winter squash', 'mexican seasoning', 'mixed spice', 'honey', 'butter', 'olive oil', 'salt']`
- **Pre-cleaned Pickle (`recipes_ingredients_cleaned.pkl`):** Contains column `ingredients_clean` with normalized tokens.

## 3. Immediate Action Items & Questions for the Professor

According to the Week 1 milestone checklist, the following questions must be confirmed with the professor:
1. **RecipeDB Access**: Bulk database dump vs. REST API (and potential rate limits).
2. **Nutrients per Ingredient**: Verify whether RecipeDB provides per-ingredient macronutrient densities (calories, saturated fat, protein per 100g) and whether servings are explicitly listed.
3. **RecipeDB to FlavorDB Mapping**: Confirm whether a pre-computed mapping between RecipeDB ingredient IDs and FlavorDB molecule profiles exists or needs to be constructed via entity resolution.
4. **Definition of 'Healthier'**: Confirm the placeholder thresholds ($\ge 15\%$ reduction in target nutrient, protein within $20\%$, dietary style preserved).
5. **Study 1 Labelling Protocol**: Confirm the manual replacement pair evaluation format (~100 Type B replacement pairs with recipe context, 1-3 scale).
