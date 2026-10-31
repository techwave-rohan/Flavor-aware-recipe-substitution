"""
Week 1 - Task 7: Leakage-Free Dataset Splitting
Implements the non-negotiable splitting protocol from Roadmap v2:
1. Group recipes with identical ingredient sets together so they never cross splits.
2. Split recipe groups into Train (70%), Validation (15%), and Test (15%) with a fixed seed (42).
3. Split the Train set into Statistics Set S (60%) and Model-Training Set M (40%).
4. All statistics (frequencies, PMI, embeddings, popularity baseline) will come strictly from S.
5. Supervised compatibility model will be trained strictly on M using features from S.

Outputs: data/processed/recipe_splits.csv
"""

import os
import ast
import yaml
import hashlib
import numpy as np
import pandas as pd

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def compute_ingredient_signature(ingr_list):
    """
    Computes a sorted canonical hash signature for an ingredient list
    to group recipes with identical ingredients.
    """
    if isinstance(ingr_list, str):
        try:
            ingr_list = ast.literal_eval(ingr_list)
        except Exception:
            ingr_list = [ingr_list]
    if not isinstance(ingr_list, list):
        return ""
    sorted_tokens = sorted([str(x).strip().lower() for x in ingr_list if str(x).strip()])
    joined = "||".join(sorted_tokens)
    return hashlib.md5(joined.encode("utf-8")).hexdigest()

def create_splits(recipes_csv_path: str, output_csv_path: str, max_recipes: int = None):
    config = load_config()
    seed = config['splits']['split_seed']
    train_ratio = config['splits']['train_ratio']
    val_ratio = config['splits']['val_ratio']
    test_ratio = config['splits']['test_ratio']
    s_ratio = config['splits']['train_stats_s_ratio']
    
    print(f"Loading recipes from {recipes_csv_path}...")
    df = pd.read_csv(recipes_csv_path, nrows=max_recipes, usecols=['id', 'name', 'ingredients'])
    total_recipes = len(df)
    print(f"Loaded {total_recipes:,} recipes.")
    
    print("Computing canonical ingredient signatures for grouping...")
    df['ingr_sig'] = df['ingredients'].apply(compute_ingredient_signature)
    
    # Group recipes by signature
    unique_sigs = df['ingr_sig'].unique()
    print(f"Found {len(unique_sigs):,} unique ingredient signatures across {total_recipes:,} recipes.")
    
    # Shuffle unique signatures reproducibly
    rng = np.random.RandomState(seed)
    shuffled_sigs = unique_sigs.copy()
    rng.shuffle(shuffled_sigs)
    
    n_sigs = len(shuffled_sigs)
    n_train_sigs = int(round(train_ratio * n_sigs))
    n_val_sigs = int(round(val_ratio * n_sigs))
    
    train_sigs = set(shuffled_sigs[:n_train_sigs])
    val_sigs = set(shuffled_sigs[n_train_sigs:n_train_sigs + n_val_sigs])
    test_sigs = set(shuffled_sigs[n_train_sigs + n_val_sigs:])
    
    # Assign split to each signature
    sig_split_map = {}
    for sig in train_sigs:
        sig_split_map[sig] = 'train'
    for sig in val_sigs:
        sig_split_map[sig] = 'val'
    for sig in test_sigs:
        sig_split_map[sig] = 'test'
        
    df['split'] = df['ingr_sig'].map(sig_split_map)
    
    # Now split train into S (60%) and M (40%)
    train_sig_list = list(train_sigs)
    rng.shuffle(train_sig_list)
    n_s_sigs = int(round(s_ratio * len(train_sig_list)))
    
    s_sigs = set(train_sig_list[:n_s_sigs])
    m_sigs = set(train_sig_list[n_s_sigs:])
    
    sub_split_map = {}
    for sig in s_sigs:
        sub_split_map[sig] = 'train_stats_S'
    for sig in m_sigs:
        sub_split_map[sig] = 'train_model_M'
    for sig in val_sigs:
        sub_split_map[sig] = 'val'
    for sig in test_sigs:
        sub_split_map[sig] = 'test'
        
    df['sub_split'] = df['ingr_sig'].map(sub_split_map)
    
    # Print summary statistics
    print("\n--- DATASET SPLIT SUMMARY ---")
    split_counts = df['split'].value_counts()
    for split_name, count in split_counts.items():
        pct = (count / total_recipes) * 100
        print(f"  {split_name:6s}: {count:,} recipes ({pct:.2f}%)")
        
    print("\n--- SUB-SPLIT (S vs M) SUMMARY ---")
    sub_counts = df['sub_split'].value_counts()
    for sub_name, count in sub_counts.items():
        pct = (count / total_recipes) * 100
        print(f"  {sub_name:15s}: {count:,} recipes ({pct:.2f}%)")
        
    # Save mapping file
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    out_cols = ['id', 'name', 'split', 'sub_split', 'ingr_sig']
    df[out_cols].to_csv(output_csv_path, index=False)
    print(f"\nSaved recipe splits to {output_csv_path}")

if __name__ == "__main__":
    recipes_in = os.path.join("data", "raw", "RAW_recipes.csv")
    splits_out = os.path.join("data", "processed", "recipe_splits.csv")
    create_splits(recipes_in, splits_out, max_recipes=50000)
