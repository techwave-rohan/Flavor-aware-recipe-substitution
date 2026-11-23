"""
Flavor-Aware Healthier Recipe Substitution Pipeline
Trained Multi-Objective Model with Functional Culinary Category Constraints & Cuisine Awareness
Run: python test_recipe.py
"""

import os
import re
import math
import yaml
import hashlib
import numpy as np
import pandas as pd
from collections import Counter
from itertools import combinations
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# --- Load configuration ---
config_path = "config.yaml" if os.path.exists("config.yaml") else "../config.yaml"
with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

SEED = config["project"]["random_seed"]

print("\n" + "="*75)
print("  INITIALIZING FLAVOR-AWARE HEALTHIER RECIPE SUBSTITUTION PIPELINE...")
print("="*75)

# 1. Load Data
cul_recipes = pd.read_csv("data/raw/culinarydb/01_Recipe_Details.csv")
cul_aliases = pd.read_csv("data/raw/culinarydb/04_Recipe-Ingredients_Aliases.csv")
df_flavordb = pd.read_csv("data/raw/flavordb.csv")

# Clean trailing spaces in CulinaryDB aliases
cul_aliases["clean_ingr"] = cul_aliases["Aliased Ingredient Name"].str.strip().str.lower()

# 2. Vocabulary Bridges (Map User-Friendly Names <-> CulinaryDB Canonical Tokens)
USER_TO_CANONICAL = {
    "olive oil": "olive",
    "extra virgin olive oil": "olive",
    "olive": "olive",
    "butter": "butter",
    "ghee": "butter",
    "heavy cream": "cream",
    "cream": "cream",
    "sour cream": "cream",
    "whipping cream": "cream",
    "greek yogurt": "yogurt",
    "plain yogurt": "yogurt",
    "yogurt": "yogurt",
    "cashew milk paste": "cashew paste",
    "cashew paste": "cashew paste",
    "ground beef": "beef",
    "beef patty": "beef",
    "beef": "beef",
    "ground turkey": "turkey",
    "turkey": "turkey",
    "chicken": "chicken",
    "cheddar cheese": "cheese cheddar",
    "cheddar": "cheese cheddar",
    "parmesan": "cheese parmesan",
    "parmesan cheese": "cheese parmesan",
    "mozzarella": "cheese mozzarella",
    "part-skim mozzarella": "cheese mozzarella",
    "mayonnaise": "mayonnaise",
    "avocado": "avocado",
    "applesauce": "apple",
    "canola oil": "canola oil",
    "vegetable oil": "vegetable oil",
    "coconut oil": "coconut oil",
    "lentils": "lentil",
    "black lentils": "lentil",
    "sugar": "sugar",
    "bacon": "bacon",
    "turkey bacon": "turkey",
}

CANONICAL_TO_DISPLAY = {
    "olive": "olive oil",
    "butter": "butter",
    "cream": "heavy cream",
    "yogurt": "greek yogurt",
    "beef": "ground beef",
    "turkey": "ground turkey",
    "cheese cheddar": "cheddar cheese",
    "cheese parmesan": "parmesan cheese",
    "cheese mozzarella": "part-skim mozzarella",
    "canola oil": "canola oil",
    "vegetable oil": "vegetable oil",
    "coconut oil": "coconut oil",
    "apple": "applesauce",
    "avocado": "avocado",
    "lentil": "lentils",
    "cashew paste": "cashew milk paste",
}

def to_canonical(name):
    clean = str(name).strip().lower()
    return USER_TO_CANONICAL.get(clean, clean)

def to_display(name):
    clean = str(name).strip().lower()
    return CANONICAL_TO_DISPLAY.get(clean, clean)

# 3. Scientific Nutritional Density Table (USDA SR Legacy Lab Values per 100g)
# [sat_fat_g, calories_kcal, protein_g]
NUTRIENT_DATABASE = {
    "butter":             {"sat_fat": 50.5, "calories": 717, "protein": 0.9, "category": "cooking_fat"},
    "olive":              {"sat_fat": 13.8, "calories": 884, "protein": 0.0, "category": "cooking_fat"},
    "canola oil":         {"sat_fat":  7.1, "calories": 884, "protein": 0.0, "category": "cooking_fat"},
    "vegetable oil":      {"sat_fat": 15.6, "calories": 884, "protein": 0.0, "category": "cooking_fat"},
    "coconut oil":        {"sat_fat": 82.5, "calories": 862, "protein": 0.0, "category": "cooking_fat"},
    "apple":              {"sat_fat":  0.1, "calories":  68, "protein": 0.2, "category": "baking_moisture"},
    "cream":              {"sat_fat": 23.0, "calories": 345, "protein": 2.1, "category": "dairy_cream"},
    "yogurt":             {"sat_fat":  1.1, "calories":  73, "protein": 10.0, "category": "dairy_cream"},
    "cashew paste":       {"sat_fat":  4.6, "calories": 160, "protein": 5.0, "category": "dairy_cream"},
    "beef":               {"sat_fat":  7.6, "calories": 254, "protein": 17.2, "category": "minced_meat"},
    "turkey":             {"sat_fat":  2.5, "calories": 149, "protein": 19.7, "category": "minced_meat"},
    "lentil":             {"sat_fat":  0.4, "calories": 116, "protein": 9.0, "category": "minced_meat"},
    "cheese cheddar":     {"sat_fat": 21.1, "calories": 403, "protein": 24.9, "category": "cheese"},
    "cheese mozzarella":  {"sat_fat": 10.9, "calories": 254, "protein": 24.3, "category": "cheese"},
    "cheese parmesan":    {"sat_fat": 15.4, "calories": 431, "protein": 38.5, "category": "cheese"},
    "mayonnaise":         {"sat_fat": 11.7, "calories": 680, "protein": 1.0, "category": "emulsion"},
    "avocado":            {"sat_fat":  2.1, "calories": 160, "protein": 2.0, "category": "emulsion"},
    "sugar":              {"sat_fat":  0.0, "calories": 387, "protein": 0.0, "category": "sweetener"},
    "flour":              {"sat_fat":  0.2, "calories": 364, "protein": 10.3, "category": "grain"},
    "pasta":              {"sat_fat":  0.3, "calories": 158, "protein": 5.8, "category": "grain"},
    "chicken":            {"sat_fat":  1.1, "calories": 165, "protein": 31.0, "category": "poultry"},
    "tomato":             {"sat_fat":  0.0, "calories":  18, "protein": 0.9, "category": "produce"},
    "garlic":             {"sat_fat":  0.1, "calories": 149, "protein": 6.4, "category": "aromatic"},
    "ginger":             {"sat_fat":  0.2, "calories":  80, "protein": 1.8, "category": "aromatic"},
    "bacon":              {"sat_fat": 14.0, "calories": 541, "protein": 37.0, "category": "cured_meat"},
    "bun":                {"sat_fat":  0.7, "calories": 279, "protein": 8.9, "category": "grain"},
}

def get_nutrient(ingr, target_nutrient="saturated_fat"):
    canon = to_canonical(ingr)
    key = "sat_fat" if target_nutrient == "saturated_fat" else "calories"
    if canon in NUTRIENT_DATABASE:
        return NUTRIENT_DATABASE[canon][key]
    return 0.1

# 4. Culinary Substitution Rules & Functional Category Mapping
CULINARY_RULES = {
    # Butter / Fats
    "butter": [
        ("olive", "olive oil", "Replaces animal saturated fat with cardioprotective monounsaturated oleic acid."),
        ("canola oil", "canola oil", "Neutral high-smoke-point liquid fat reducing saturated fat by 85%."),
        ("vegetable oil", "vegetable oil", "Plant-based neutral cooking fat cutting saturated fat by 69%."),
        ("apple", "applesauce", "Replaces solid fat moisture in baking while cutting calories by 90%."),
        ("cashew paste", "cashew milk paste", "Traditional rich Indian curry tempering paste without dairy fat."),
        ("yogurt", "greek yogurt", "Creamy texture and lactic acidity with 98% less saturated fat."),
    ],
    # Creams
    "cream": [
        ("yogurt", "greek yogurt", "Maintains velvety sauce emulsion and tang with 95% less saturated fat."),
        ("cashew paste", "cashew milk paste", "Provides luxurious gravy viscosity and richness without dairy butterfat."),
        ("olive", "olive oil", "Lighter emulsion base for savory sauces cutting cholesterol and saturated fat."),
    ],
    # Minced Meats
    "beef": [
        ("turkey", "ground turkey", "Direct 1:1 poultry replacement preserving savory umami with 67% less saturated fat."),
        ("lentil", "lentils", "High-protein legume alternative eliminating cholesterol and saturated fat."),
    ],
    # Cheeses
    "cheese cheddar": [
        ("cheese mozzarella", "part-skim mozzarella", "Maintains meltability and salinity with 50% lower saturated fat."),
        ("cheese parmesan", "parmesan cheese", "Strong umami allows using 50% less quantity for equivalent flavor."),
    ],
    # Condiments
    "mayonnaise": [
        ("avocado", "avocado mash", "Replaces emulsified egg/oil fat with healthy monounsaturated plant lipids."),
        ("yogurt", "greek yogurt spread", "Tangy, thick spread cutting calories by 80% with zero saturated fat."),
    ],
}

# 5. Build Leakage-Free PMI Matrix from Statistics Set S
cul_recipe_ingrs = cul_aliases.groupby("Recipe ID")["clean_ingr"].apply(lambda x: sorted(list(set(x)))).reset_index()
cul_df = pd.merge(cul_recipes, cul_recipe_ingrs, on="Recipe ID")
cul_df["sig"] = cul_df["clean_ingr"].apply(lambda il: hashlib.md5("||".join(il).encode()).hexdigest())

rng = np.random.RandomState(SEED)
shuffled = cul_df["sig"].unique()
rng.shuffle(shuffled)
n_train = int(round(config["splits"]["train_ratio"] * len(shuffled)))
train_sigs = list(shuffled[:n_train])
rng.shuffle(train_sigs)
n_s = int(round(config["splits"]["train_stats_s_ratio"] * len(train_sigs)))
s_sigs = set(train_sigs[:n_s])
m_sigs = set(train_sigs[n_s:])

S_df = cul_df[cul_df["sig"].isin(s_sigs)]
M_df = cul_df[cul_df["sig"].isin(m_sigs)]

all_lists = S_df["clean_ingr"].tolist()
n_rec = len(all_lists)
freq, pair_freq = Counter(), Counter()
for ingrs in all_lists:
    s = list(set(ingrs))
    for i in s:
        freq[i] += 1
    for a, b in combinations(sorted(s), 2):
        pair_freq[(a, b)] += 1

valid = {k for k, v in freq.items() if v >= 5}
pmi_dict = {}
for (a, b), cc in pair_freq.items():
    if a in valid and b in valid:
        val = math.log2((cc / n_rec + 1e-9) / (freq[a] / n_rec * freq[b] / n_rec + 1e-9))
        pmi_dict[(a, b)] = val
        pmi_dict[(b, a)] = val

# FlavorDB Jaccard
mol_col = [c for c in df_flavordb.columns if any(x in c.lower() for x in ["mol", "compound", "pubchem", "flavor"])][0]
alias_col = "alias" if "alias" in df_flavordb.columns else df_flavordb.columns[0]
flavor_mol_map = {}
for _, row in df_flavordb.iterrows():
    name = str(row[alias_col]).strip().lower()
    mols = frozenset(x.strip().lower() for x in re.split(r"[,;|]", str(row[mol_col])) if x.strip())
    if mols:
        flavor_mol_map[name] = mols

def jaccard_flavor(a, b):
    ma = flavor_mol_map.get(a, frozenset())
    mb = flavor_mol_map.get(b, frozenset())
    if not ma or not mb:
        return 0.0
    return len(ma & mb) / len(ma | mb)

def extract_features(cand, ctx):
    pmi_vals = [pmi_dict.get((cand, c), pmi_dict.get((c, cand), 0.0)) for c in ctx]
    jac_vals = [jaccard_flavor(cand, c) for c in ctx]
    return [
        float(np.mean(pmi_vals)) if pmi_vals else 0.0,
        float(max(pmi_vals)) if pmi_vals else 0.0,
        float(np.mean(jac_vals)) if jac_vals else 0.0,
        math.log1p(freq.get(cand, 0))
    ]

# Train Model on M
vocab_list = sorted([k for k, v in freq.items() if v >= 5])
X_tr, y_tr = [], []
for _, row in M_df.sample(n=min(1500, len(M_df)), random_state=SEED).iterrows():
    ingrs = row["clean_ingr"]
    if len(ingrs) < 2:
        continue
    for idx, tgt in enumerate(ingrs):
        ctx = [x for i, x in enumerate(ingrs) if i != idx]
        X_tr.append(extract_features(tgt, ctx))
        y_tr.append(1)
        neg_cand = rng.choice(vocab_list)
        if neg_cand not in set(ingrs):
            X_tr.append(extract_features(neg_cand, ctx))
            y_tr.append(0)

scaler = StandardScaler()
X_tr_sc = scaler.fit_transform(X_tr)
clf = LogisticRegression(C=1.0, max_iter=300, random_state=SEED)
clf.fit(X_tr_sc, y_tr)
print("  Supervised Multi-Objective Classifier Fitted on Set M!\n")

# --- Recommendation Engine ---
def test_recipe(title, cuisine, raw_ingredients, target_nutrient="saturated_fat", alpha=0.5, gamma=0.5, top_n=4):
    canonical_ingrs = [to_canonical(i) for i in raw_ingredients]
    
    # 1. Identify high-impact offender
    target_canon = max(canonical_ingrs, key=lambda x: get_nutrient(x, target_nutrient))
    target_display = to_display(target_canon)
    tval = get_nutrient(target_canon, target_nutrient)
    
    total_val = sum(get_nutrient(x, target_nutrient) for x in canonical_ingrs) + 1e-9
    tpct = (tval / total_val) * 100
    context = [x for x in canonical_ingrs if x != target_canon]
    
    unit = "g/100g" if target_nutrient == "saturated_fat" else "kcal/100g"
    
    print("\n" + "="*75)
    print(f"  RECIPE: {title.upper()} ({cuisine})")
    print("="*75)
    print(f"  Ingredients   : {', '.join(raw_ingredients)}")
    print(f"  Target Metric : {target_nutrient.replace('_', ' ').title()}")
    print(f"  Top Offender  : '{target_display}' ({tval:.1f} {unit}) -> accounts for {tpct:.1f}% of recipe total")
    
    # 2. Functional Category Substitution Pool
    candidate_rules = CULINARY_RULES.get(target_canon, [])
    if not candidate_rules:
        # Fallback: find any category-matched items in database
        target_cat = NUTRIENT_DATABASE.get(target_canon, {}).get("category", "other")
        candidate_rules = [
            (c, to_display(c), f"Alternative {target_cat.replace('_',' ')} substitute.")
            for c, d in NUTRIENT_DATABASE.items()
            if d.get("category") == target_cat and c != target_canon and get_nutrient(c, target_nutrient) < tval
        ]
    
    if not candidate_rules:
        print("  [!] No function-safe healthier substitutes found in knowledge base.")
        return

    # 3. Cuisine-Specific Affinity Adjustments
    # e.g., Southern European loves olive oil; South Asian loves yogurt/cashew paste/canola oil; Baking loves applesauce
    cuisine_lower = cuisine.lower()
    
    scored = []
    for cand_canon, cand_display, rationale in candidate_rules:
        cval = get_nutrient(cand_canon, target_nutrient)
        h_drop = max(0.0, (tval - cval) / (tval + 1e-9))
        jac = jaccard_flavor(target_canon, cand_canon)
        
        feats = extract_features(cand_canon, context)
        comp = float(clf.predict_proba(scaler.transform([feats]))[0, 1])
        
        # Contextual Cuisine & Functional Prior:
        prior = 0.0
        if "italian" in cuisine_lower or "european" in cuisine_lower:
            if cand_canon == "olive": prior = 0.25
        elif "indian" in cuisine_lower or "south asian" in cuisine_lower:
            if cand_canon in ["yogurt", "cashew paste", "canola oil"]: prior = 0.20
        elif "cookie" in title.lower() or "cake" in title.lower():
            if cand_canon in ["apple", "canola oil"]: prior = 0.25
        elif "mexican" in cuisine_lower or "latin" in cuisine_lower:
            if cand_canon in ["avocado", "cheese mozzarella"]: prior = 0.20
        
        final_score = alpha * h_drop + 0.1 * jac + gamma * comp + prior
        scored.append((cand_display, final_score, h_drop, comp, jac, rationale))
    
    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:top_n]
    
    print("-" * 75)
    print(f"  {'Rank':<5} {'Candidate':<24} {'Score':>7} {'Nutrient Drop':>15} {'Taste Compat':>14} {'Flavor Jaccard':>15}")
    print("  " + "-"*83)
    for r, (c_name, score, h_drop, comp, jac, _) in enumerate(top, 1):
        print(f"  #{r:<4} {c_name:<24} {score:>7.3f} {h_drop*100:>14.1f}% {comp*100:>13.1f}% {jac:>15.4f}")
    
    best_name, best_score, best_drop, best_comp, best_jac, best_rationale = top[0]
    
    print("="*75)
    print(f"  >>> BEST RECOMMENDATION: Replace '{target_display}' with '{best_name}'")
    print(f"      - Health Improvement  : -{best_drop*100:.1f}% {target_nutrient.replace('_',' ')}")
    print(f"      - Taste Compatibility : {best_comp*100:.1f}%")
    print(f"      - Culinary Rationale  : {best_rationale}")
    print("="*75 + "\n")


if __name__ == "__main__":
    demo_list = [
        ("Creamy Garlic Fettuccine", "Southern European", ["pasta", "butter", "heavy cream", "garlic", "parmesan"]),
        ("Traditional Butter Chicken", "South Asian", ["chicken", "butter", "heavy cream", "tomato", "garlic", "ginger"]),
        ("Classic Chocolate Chip Cookies", "North American", ["butter", "sugar", "flour", "chocolate chips", "eggs"]),
        ("Spaghetti Bolognese", "Southern European", ["pasta", "ground beef", "tomato", "onion", "olive oil", "garlic", "parmesan"]),
        ("Dal Makhani", "South Asian", ["black lentils", "kidney beans", "heavy cream", "butter", "tomato", "garlic", "ginger"])
    ]

    print("Choose how to test:")
    print("  1. Run 5 Showcase Recipes (Italian, Indian, Baking, Dal Makhani)")
    print("  2. Test Your Own Custom Recipe")
    choice = input("\nEnter choice (1 or 2, default is 1): ").strip()

    if choice == "2":
        title = input("Enter recipe title (e.g. Creamy Potato Soup): ").strip() or "Custom Recipe"
        cuisine = input("Enter cuisine (e.g. Italian, Indian, American): ").strip() or "General"
        raw_ingrs = input("Enter ingredients separated by commas: ").strip()
        ingrs = [i.strip() for i in raw_ingrs.split(",") if i.strip()]
        if not ingrs:
            ingrs = ["pasta", "butter", "heavy cream", "garlic"]
        test_recipe(title, cuisine, ingrs)
    else:
        for title, cuisine, ingrs in demo_list:
            test_recipe(title, cuisine, ingrs)
