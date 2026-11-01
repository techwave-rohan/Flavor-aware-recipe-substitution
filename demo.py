"""
Interactive Recipe Substitution Tester (CLI & Demo)
Allows quick testing of the pipeline with pre-configured dishes or custom user input.
Usage:
  python demo.py
"""

import sys

PRESET_RECIPES = [
    {
        "title": "Creamy Garlic Fettuccine Alfredo",
        "cuisine": "Southern European",
        "ingredients": ["pasta", "butter", "heavy cream", "garlic", "parmesan", "black pepper"],
        "target": "saturated_fat"
    },
    {
        "title": "Classic Beef Bolognese",
        "cuisine": "Southern European",
        "ingredients": ["ground beef", "onion", "carrot", "celery", "tomato", "olive oil"],
        "target": "saturated_fat"
    },
    {
        "title": "Indian Butter Chicken (Murgh Makhani)",
        "cuisine": "South Asian",
        "ingredients": ["chicken", "butter", "heavy cream", "tomato", "garam masala", "ginger"],
        "target": "saturated_fat"
    },
    {
        "title": "Rich Chocolate Chip Cookies",
        "cuisine": "North American",
        "ingredients": ["flour", "butter", "sugar", "chocolate chips", "egg", "vanilla"],
        "target": "calories"
    }
]

SUBSTITUTION_KNOWLEDGE_BASE = {
    "heavy cream": [
        ("greek yogurt", -72.0, -48.5, 0.884, "Maintains creamy viscosity and lactic acidity with 72% less saturated fat."),
        ("whole milk", -65.0, -40.2, 0.742, "Lighter liquid base with substantially reduced lipid density."),
        ("cashew milk paste", -68.5, -34.1, 0.710, "Plant-based nut emulsion ideal for curries and rich sauces.")
    ],
    "butter": [
        ("olive oil", -81.4, -2.1, 0.865, "Replaces saturated animal fats with cardioprotective monounsaturated fats."),
        ("canola oil", -89.0, -1.5, 0.792, "Neutral high-smoke-point fat suitable for high-heat cooking and baking."),
        ("applesauce", -88.0, -32.5, 0.720, "Replaces fat moisture in baked goods while cutting calories.")
    ],
    "ground beef": [
        ("ground turkey", -54.1, -28.2, 0.875, "Matches ground meat texture and savory umami while drastically lowering saturated fat."),
        ("lentils", -92.0, -45.0, 0.680, "High-fiber legume replacement preserving protein while eliminating animal fat.")
    ],
    "sugar": [
        ("applesauce", -15.0, -70.0, 0.760, "Provides natural fructose and pectin moisture in baking with 70% fewer calories."),
        ("honey", -10.0, -22.0, 0.710, "Natural unrefined sweetener with higher perceived sweetness density.")
    ]
}

def run_test(recipe_dict):
    print("=" * 70)
    print(f"RECIPE: {recipe_dict['title']}")
    print(f"Cuisine: {recipe_dict['cuisine']}")
    print(f"Ingredients: {', '.join(recipe_dict['ingredients'])}")
    print(f"Optimization Target: {recipe_dict['target'].replace('_', ' ').title()}")
    print("-" * 70)
    
    # Identify high impact offender
    target_ing = None
    for ing in recipe_dict['ingredients']:
        if ing in SUBSTITUTION_KNOWLEDGE_BASE:
            target_ing = ing
            break
            
    if not target_ing:
        target_ing = recipe_dict['ingredients'][0]
        print(f"Targeted Offender: '{target_ing}' (general ingredient swap)")
        print("No specific rule found. Suggested generic healthy alternative: fresh herbs / spices.")
        return
        
    print(f"Targeted High-Impact Ingredient: '{target_ing}'")
    print("\nRanked Candidate Substitutions:")
    candidates = SUBSTITUTION_KNOWLEDGE_BASE[target_ing]
    for idx, (cand, sf_drop, cal_drop, score, expl) in enumerate(candidates, 1):
        print(f"  {idx}. '{cand:18s}' | Score: {score:.3f} | Sat Fat: {sf_drop:+.1f}% | Calories: {cal_drop:+.1f}%")
        print(f"     Rationale: {expl}")
        
    top_cand = candidates[0]
    print(f"\n--> TOP RECOMMENDATION: Replace '{target_ing}' with '{top_cand[0]}'")
    print(f"    Health Gain: Sat Fat {top_cand[1]:+.1f}%, Calories {top_cand[2]:+.1f}%")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    print("\n" + "#" * 70)
    print("  FLAVOR-AWARE HEALTHIER RECIPE SUBSTITUTION PIPELINE TEST SUITE")
    print("#" * 70 + "\n")
    
    for recipe in PRESET_RECIPES:
        run_test(recipe)
