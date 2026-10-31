"""
Week 1 - Task 3: Ingredient Cleaning and Normalization
Standardizes ingredient strings by applying deterministic linguistic rules:
1. Lowercasing and whitespace normalization
2. Disambiguation (e.g., clove of garlic vs. spice clove)
3. Compound splitting (e.g., 'salt and pepper')
4. Stripping preparation adjectives (e.g., 'diced', 'chopped', 'freshly ground')
5. Singularization / lemmatization

Outputs: data/processed/ingredient_normalization.csv (raw_name, clean_name, rule_applied)
"""

import re
import os
import ast
import pandas as pd

PREP_WORDS = [
    'fresh', 'freshly', 'diced', 'chopped', 'minced', 'sliced', 'crushed',
    'grated', 'shredded', 'peeled', 'melted', 'toasted', 'roasted', 'cooked',
    'uncooked', 'raw', 'ground', 'finely', 'coarsely', 'roughly', 'thinly',
    'thickly', 'frozen', 'canned', 'dried', 'warm', 'cold', 'hot', 'softened',
    'pureed', 'drained', 'rinsed', 'divided', 'optional', 'trimmed', 'sifted',
    'beaten', 'whipped', 'steamed', 'baked', 'boiled', 'boneless', 'skinless'
]

COMPOUND_SPLITS = [
    (r'\bsalt and (?:freshly ground )?(?:black )?pepper\b', ['salt', 'black pepper']),
    (r'\boil and vinegar\b', ['oil', 'vinegar']),
    (r'\bbutter and oil\b', ['butter', 'oil'])
]

AMBIGUOUS_TERMS = [
    (r'\bcloves? of garlic\b', 'garlic'),
    (r'\bgarlic cloves?\b', 'garlic'),
    (r'\bwhole cloves?\b', 'clove'),
    (r'\bground cloves?\b', 'clove')
]

def clean_single_ingredient(raw_name: str):
    """
    Cleans a single ingredient string and tracks rules applied.
    Returns: list of (clean_name, rule_applied)
    """
    if not isinstance(raw_name, str) or not raw_name.strip():
        return [("", "empty_or_null")]
    
    text = raw_name.lower().strip()
    rules_applied = []
    
    # Rule 1: Disambiguation
    for pattern, replacement in AMBIGUOUS_TERMS:
        if re.search(pattern, text):
            text = re.sub(pattern, replacement, text)
            rules_applied.append(f"disambiguation({replacement})")
    
    # Rule 2: Compound splitting
    for pattern, split_items in COMPOUND_SPLITS:
        if re.search(pattern, text):
            rules_applied.append("compound_split")
            results = []
            for item in split_items:
                res = clean_single_ingredient(item)
                results.extend(res)
            return results
    
    # Rule 3: Strip parentheses and punctuation
    cleaned = re.sub(r'\(.*?\)', '', text)
    cleaned = re.sub(r'[,;:\*]', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    if cleaned != text:
        rules_applied.append("strip_punctuation")
    
    # Rule 4: Strip preparation words
    words = cleaned.split()
    filtered_words = [w for w in words if w not in PREP_WORDS]
    if len(filtered_words) < len(words) and len(filtered_words) > 0:
        cleaned = " ".join(filtered_words)
        rules_applied.append("strip_prep_words")
    
    # Rule 5: Simple singularization (safe plural stripping)
    if cleaned.endswith('ies') and len(cleaned) > 4:
        cleaned = cleaned[:-3] + 'y'
        rules_applied.append("singularize_ies")
    elif cleaned.endswith('es') and not cleaned.endswith(('cheese', 'sauce', 'puree')) and len(cleaned) > 4:
        if cleaned.endswith(('tomatoes', 'potatoes')):
            cleaned = cleaned[:-2]
        else:
            cleaned = cleaned[:-1]
        rules_applied.append("singularize_es")
    elif cleaned.endswith('s') and not cleaned.endswith(('ss', 'couscous', 'hummus', 'molasses', 'citrus', 'asparagus')) and len(cleaned) > 3:
        cleaned = cleaned[:-1]
        rules_applied.append("singularize_s")
    
    if not rules_applied:
        rules_applied.append("lowercase_identity")
        
    return [(cleaned.strip(), "; ".join(rules_applied))]

def generate_ingredient_normalization(recipes_csv_path: str, output_csv_path: str, sample_limit: int = 50000):
    """
    Extracts raw ingredient strings, applies cleaning rules, and generates normalization table.
    """
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    print(f"Loading raw ingredients from {recipes_csv_path}...")
    
    # Read sample or full recipes
    df = pd.read_csv(recipes_csv_path, nrows=sample_limit, usecols=['ingredients'])
    
    unique_raw_ingredients = set()
    for row in df['ingredients'].dropna():
        try:
            items = ast.literal_eval(row)
            if isinstance(items, list):
                for item in items:
                    unique_raw_ingredients.add(item.strip())
        except Exception:
            pass
            
    print(f"Extracted {len(unique_raw_ingredients):,} unique raw ingredient strings.")
    
    records = []
    for raw in sorted(unique_raw_ingredients):
        results = clean_single_ingredient(raw)
        for clean_name, rule in results:
            records.append({
                'raw_name': raw,
                'clean_name': clean_name,
                'rule_applied': rule
            })
            
    norm_df = pd.DataFrame(records)
    norm_df.to_csv(output_csv_path, index=False)
    print(f"Saved {len(norm_df):,} ingredient normalization records to {output_csv_path}")
    return norm_df

if __name__ == "__main__":
    raw_path = os.path.join("data", "raw", "RAW_recipes.csv")
    out_path = os.path.join("data", "processed", "ingredient_normalization.csv")
    generate_ingredient_normalization(raw_path, out_path, sample_limit=50000)
