# Week 1: Multi-Source Data Access and Inventory Report

**Date:** 2026-11-01  
**Project:** Flavor-Aware Healthier Recipe Substitution (Roadmap v2)  
**Deliverable:** `reports/week1_data_inventory.md`  
**Architecture:** Open Multi-Source Gastronomy Stack  

---

## 1. Overview of Open Datasets

Due to access restrictions on proprietary RecipeDB bulk files, the project has adopted the open-science composite stack:

| Dataset | Provider / Source | Role in Pipeline | Local Storage Path | Status |
|---|---|---|---|---|
| **CulinaryDB** | IIIT-Delhi CoSyLab | Recipe ingredients, 20+ regional cuisines, 985 ingredient categories | `data/raw/culinarydb/` | **Downloaded & Ingested** (45,772 recipes) |
| **USDA FoodData Central** | US Department of Agriculture (SR Legacy) | Official per-100g nutrient densities (calories, saturated fat, protein, sodium, sugars) | `data/raw/usda/` | **Downloaded & Ingested** (8,618 standard foods) |
| **FlavorDB** | IIIT-Delhi CoSyLab / GitHub | Food entities mapped to PubChem flavor molecules | `data/raw/flavordb.csv` | **Downloaded & Ingested** (936 food items) |
| **Flavor Network** | Ahn et al., *Nature* 2011 | Independent bipartite food-pairing network | `data/raw/flavor_network/` | **Downloaded & Ingested** |
| **Food.com** | Kaggle / Recipe1M | Supplementary large-scale co-occurrence corpus | `data/raw/RAW_recipes.csv` | **Available** (231k recipes) |

---

## 2. In-Depth Profiles of Ingested Datasets

### 2.1 CulinaryDB Profile (`data/raw/culinarydb/`)
- **Total Recipes**: 45,772
- **Cuisine Taxonomy**: 20+ regional classifications, including:
  - North American: 11,568 recipes
  - Southern European: 6,375 recipes
  - Latin American: 5,333 recipes
  - Western European: 4,413 recipes
  - South Asian: 4,222 recipes
  - East Asian: 2,635 recipes
  - Middle Eastern: 1,886 recipes
  - Southeast Asian: 1,622 recipes
- **Ingredient Taxonomy (`02_Ingredients.csv`)**: 985 unique canonical ingredients with category tags (Plant Derivative, Meat, Dairy, Spice, Fat/Oil, Vegetable, Fruit, etc.).
- **Recipe Mappings (`04_Recipe-Ingredients_Aliases.csv`)**: 622,357 individual ingredient-to-recipe mappings.

### 2.2 USDA FoodData Central Profile (`data/raw/usda/`)
- **Total Foods Profiled**: 8,618 minimally processed and standard reference foods.
- **Nutrient Densities**: Values provided per 100 grams.
- **Key Target Nutrients Mapped**:
  - `Energy` (Nutrient ID: `1008`, Unit: `KCAL`)
  - `Fatty acids, total saturated` (Nutrient ID: `1258`, Unit: `G`)
  - `Protein` (Nutrient ID: `1003`, Unit: `G`)
  - `Sodium, Na` (Nutrient ID: `1093`, Unit: `MG`)
  - `Sugars, total` (Nutrient ID: `2000`, Unit: `G`)
- **Advantage**: Replaces estimated recipe-level nutrition with official laboratory measurements.

### 2.3 FlavorDB & Flavor Network Profile
- **FlavorDB**: 936 food entities mapped to arrays of PubChem molecule IDs and odor profiles (percepts).
- **Flavor Network (Ahn et al. 2011)**: Complete graph of ingredient-compound links from scientific literature.
- **Advantage**: Provides complete mathematical basis for Jaccard flavor molecule overlap calculations.

---

## 3. Leakage-Free Splitting Summary
- **Cluster Identifier**: MD5 hash of canonical ingredient sets.
- **Unique Signatures**: 45,064 clusters across 45,772 CulinaryDB recipes.
- **Partitions**:
  - **Train**: 32,045 recipes (70.01%)
    - **Statistics Set ($S$)**: 19,227 recipes (60% of Train / 42.01% of total) — *all statistics derived strictly here*.
    - **Model Set ($M$)**: 12,818 recipes (40% of Train / 28.00% of total) — *used to fit supervised model*.
  - **Validation**: 6,864 recipes (15.00%)
  - **Test**: 6,863 recipes (14.99%)
- **Integrity**: Zero recipe overlap across splits.
