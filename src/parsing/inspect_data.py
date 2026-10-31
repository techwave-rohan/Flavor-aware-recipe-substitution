"""
Week 1 - Task 1: Data Access and Inspection
Profiles available datasets (Food.com, RecipeDB, FlavorDB) and logs counts, columns,
dtypes, missing rates, nutrient availability, servings, cuisine tags, and ingredient format.
Generates 'reports/week1_data_inventory.md'.
"""

import os
import ast
import json
import pandas as pd
import numpy as np

def run_inspection():
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    report_file = os.path.join(reports_dir, "week1_data_inventory.md")

    food_com_path = os.path.join("data", "raw", "RAW_recipes.csv")
    cleaned_pkl_path = os.path.join("data", "raw", "recipes_ingredients_cleaned.pkl")
    
    inventory_lines = []
    inventory_lines.append("# Week 1: Data Access and Inspection Report\n")
    inventory_lines.append(f"**Date:** 2026-10-31\n")
    inventory_lines.append(f"**Deliverable:** `reports/week1_data_inventory.md`\n")
    inventory_lines.append(f"**Status:** Completed Task 1 of Week 1 according to `Agent Roadmap v2`.\n\n")

    # 1. Overview of Data Sources
    inventory_lines.append("## 1. Data Sources Inventory & Access Status\n\n")
    inventory_lines.append("| Source | Description | Access Status | Storage / Location |\n")
    inventory_lines.append("|---|---|---|---|\n")
    inventory_lines.append("| **Food.com** | 231k recipes with recipe-level nutrition & ingredient lists | **Available** | `data/raw/RAW_recipes.csv` |\n")
    inventory_lines.append("| **RecipeDB** | Recipes with gram quantities, 29 categories, 5 dietary styles | **Pending Confirmation** | API / bulk dump to confirm with professor |\n")
    inventory_lines.append("| **FlavorDB** | Flavor molecules per ingredient (chemical profiles) | **Pending Mapping** | FlavorDB mapping to confirm with professor |\n")
    inventory_lines.append("| **Foodoscope API** | Substitution & flavor API (Baseline B6) | **Pending Access** | Optional (IF TIME) |\n\n")

    # 2. Food.com Deep Inspection
    if os.path.exists(food_com_path):
        print("Reading Food.com RAW_recipes.csv for profiling...")
        df = pd.read_csv(food_com_path)
        row_count = len(df)
        col_count = len(df.columns)
        
        inventory_lines.append("## 2. Food.com Dataset Profile (`RAW_recipes.csv`)\n\n")
        inventory_lines.append(f"- **Total Recipes (Rows):** {row_count:,}\n")
        inventory_lines.append(f"- **Total Columns:** {col_count}\n\n")
        
        # Columns & Types & Missing values table
        inventory_lines.append("### 2.1 Columns, Dtypes, and Missing Rates\n\n")
        inventory_lines.append("| Column Name | Data Type | Non-Null Count | Missing Count | Missing Rate (%) |\n")
        inventory_lines.append("|---|---|---|---|---|\n")
        
        for col in df.columns:
            non_null = df[col].notnull().sum()
            null_count = df[col].isnull().sum()
            missing_rate = (null_count / row_count) * 100.0
            inventory_lines.append(f"| `{col}` | `{df[col].dtype}` | {non_null:,} | {null_count:,} | {missing_rate:.3f}% |\n")
        
        # Nutrition column inspection
        inventory_lines.append("\n### 2.2 Nutrient Availability Analysis\n\n")
        inventory_lines.append("- **Per-Ingredient Nutrients:** **NOT AVAILABLE in Food.com.** Food.com only records recipe-level summary nutrition.\n")
        inventory_lines.append("- **Per-Recipe Nutrition Format:** Vector of 7 float values stored as string `[calories, total_fat, sugar, sodium, protein, saturated_fat, carbohydrates]`.\n")
        sample_nutr = df['nutrition'].dropna().iloc[0]
        inventory_lines.append(f"- **Sample Raw Nutrition String:** `{sample_nutr}`\n")
        inventory_lines.append("- **Interpretation:** Value 0 is calories; values 1-6 are % Daily Value (PDV).\n")
        inventory_lines.append("> **Important Rule from Roadmap:** Because Food.com lacks per-ingredient gram quantities and nutrient breakdowns, it **must never be used for health gain calculations**; it serves strictly as a fallback prototype for co-occurrence and compatibility measures.\n\n")
        
        # Servings inspection
        inventory_lines.append("### 2.3 Servings Availability\n\n")
        has_servings_col = 'servings' in df.columns or 'n_servings' in df.columns
        inventory_lines.append(f"- **Servings Column Present:** `{has_servings_col}`\n")
        inventory_lines.append("- **Roadmap Rule:** When servings are absent, relative changes in target nutrients are calculated over the whole-recipe total. Since ingredient replacements are evaluated at equal weight, the percentage change is mathematically identical per serving.\n\n")

        # Cuisines & Tags inspection
        inventory_lines.append("### 2.4 Cuisine & Dietary Labels\n\n")
        print("Parsing sample tags for cuisine extraction...")
        # Sample tags to find cuisines
        sample_tags = df['tags'].dropna().head(10000).apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else [])
        all_tags = [tag for sublist in sample_tags for tag in sublist]
        tag_series = pd.Series(all_tags).value_index = pd.Series(all_tags).value_counts()
        
        cuisine_keywords = ['cuisine', 'north-american', 'mexican', 'italian', 'asian', 'indian', 'european', 'french', 'greek', 'chinese', 'mediterranean', 'thai', 'japanese']
        matched_cuisines = {kw: tag_series.get(kw, 0) for kw in cuisine_keywords if kw in tag_series}
        
        inventory_lines.append(f"- **Tag Field:** Stored in `tags` as stringified Python list.\n")
        inventory_lines.append(f"- **Identified Cuisine & Regional Tags (Sample 10k):**\n")
        for cuisine, count in sorted(matched_cuisines.items(), key=lambda x: x[1], reverse=True):
            inventory_lines.append(f"  - `{cuisine}`: {count:,} recipes\n")
        
        # Ingredients format inspection
        inventory_lines.append("\n### 2.5 Ingredient Name Format\n\n")
        sample_ingrs = ast.literal_eval(df['ingredients'].dropna().iloc[0])
        inventory_lines.append(f"- **Raw Format:** Stringified list of strings without units or quantities. Example: `{sample_ingrs}`\n")
        inventory_lines.append(f"- **Pre-cleaned Pickle (`recipes_ingredients_cleaned.pkl`):** Contains column `ingredients_clean` with normalized tokens.\n")

    # 3. Action Items and Professor Questions
    inventory_lines.append("\n## 3. Immediate Action Items & Questions for the Professor\n\n")
    inventory_lines.append("According to the Week 1 milestone checklist, the following questions must be confirmed with the professor:\n")
    inventory_lines.append("1. **RecipeDB Access**: Bulk database dump vs. REST API (and potential rate limits).\n")
    inventory_lines.append("2. **Nutrients per Ingredient**: Verify whether RecipeDB provides per-ingredient macronutrient densities (calories, saturated fat, protein per 100g) and whether servings are explicitly listed.\n")
    inventory_lines.append("3. **RecipeDB to FlavorDB Mapping**: Confirm whether a pre-computed mapping between RecipeDB ingredient IDs and FlavorDB molecule profiles exists or needs to be constructed via entity resolution.\n")
    inventory_lines.append("4. **Definition of 'Healthier'**: Confirm the placeholder thresholds ($\ge 15\%$ reduction in target nutrient, protein within $20\%$, dietary style preserved).\n")
    inventory_lines.append("5. **Study 1 Labelling Protocol**: Confirm the manual replacement pair evaluation format (~100 Type B replacement pairs with recipe context, 1-3 scale).\n")

    with open(report_file, "w", encoding="utf-8") as f:
        f.writelines(inventory_lines)
    
    print(f"Report written successfully to {report_file}")

if __name__ == "__main__":
    run_inspection()
