"""
Week 1 - Task 4: Quantity and Unit Parser to Grams
Parses raw quantity strings, fractional values (e.g. '1/2', '1 1/2'), and units,
and converts them into grams using standardized density and metric conversion factors.
Logs unconverted units and ingredients to 'reports/week1_unconverted_units.md'.
"""

import re
import os
import pandas as pd
from fractions import Fraction

# Standard unit to grams conversions (assuming baseline density ~ 1.0 g/ml for liquids)
UNIT_CONVERSION_FACTORS = {
    # Mass
    'g': 1.0,
    'gram': 1.0,
    'grams': 1.0,
    'kg': 1000.0,
    'kilogram': 1000.0,
    'kilograms': 1000.0,
    'mg': 0.001,
    'oz': 28.3495,
    'ounce': 28.3495,
    'ounces': 28.3495,
    'lb': 453.592,
    'lbs': 453.592,
    'pound': 453.592,
    'pounds': 453.592,
    
    # Volume (metric & US customary assuming water density 1 g/ml)
    'ml': 1.0,
    'milliliter': 1.0,
    'milliliters': 1.0,
    'l': 1000.0,
    'liter': 1000.0,
    'liters': 1000.0,
    'tsp': 4.92892,
    'teaspoon': 4.92892,
    'teaspoons': 4.92892,
    'tbsp': 14.7868,
    'tablespoon': 14.7868,
    'tablespoons': 14.7868,
    'cup': 236.588,
    'cups': 236.588,
    'pt': 473.176,
    'pint': 473.176,
    'pints': 473.176,
    'qt': 946.353,
    'quart': 946.353,
    'quarts': 946.353,
    'gal': 3785.41,
    'gallon': 3785.41,
    'gallons': 3785.41,
    'fl oz': 29.5735,
    'fluid ounce': 29.5735,
    'fluid ounces': 29.5735,
    
    # Small culinary approximations
    'pinch': 0.36,
    'pinches': 0.36,
    'dash': 0.72,
    'dashes': 0.72,
    'clove': 5.0,        # Garlic clove ~ 5g
    'cloves': 5.0,
    'slice': 25.0,
    'slices': 25.0,
    'piece': 30.0,
    'pieces': 30.0,
    'stalk': 40.0,       # Celery stalk ~ 40g
    'stalks': 40.0,
    'sprig': 2.0,        # Herb sprig ~ 2g
    'sprigs': 2.0
}

def parse_quantity_string(qty_str: str) -> float:
    """
    Parses numeric, fractional, or mixed quantity strings (e.g. '1/2', '1 1/4', '0.75').
    """
    if not isinstance(qty_str, str):
        try:
            return float(qty_str)
        except Exception:
            return 0.0
            
    qty_str = qty_str.strip()
    if not qty_str:
        return 0.0
        
    # Match mixed fraction (e.g., '1 1/2')
    mixed_match = re.match(r'^(\d+)\s+(\d+)/(\d+)$', qty_str)
    if mixed_match:
        whole, num, denom = mixed_match.groups()
        return float(whole) + (float(num) / float(denom))
        
    # Match simple fraction (e.g., '1/2')
    frac_match = re.match(r'^(\d+)/(\d+)$', qty_str)
    if frac_match:
        num, denom = frac_match.groups()
        return float(num) / float(denom)
        
    # Match regular float or integer
    num_match = re.match(r'^(\d+(?:\.\d+)?)$', qty_str)
    if num_match:
        return float(num_match.group(1))
        
    return 0.0

def convert_to_grams(quantity: float, unit: str):
    """
    Converts quantity and unit into grams.
    Returns: (grams: float, is_converted: bool, note: str)
    """
    if quantity <= 0:
        return (0.0, False, "zero_or_negative_quantity")
        
    if not isinstance(unit, str) or not unit.strip():
        # Unitless counts default to item estimate or flag
        return (quantity * 50.0, False, "unitless_assumed_item_50g")
        
    clean_unit = unit.lower().strip()
    if clean_unit in UNIT_CONVERSION_FACTORS:
        factor = UNIT_CONVERSION_FACTORS[clean_unit]
        return (quantity * factor, True, "converted")
        
    return (0.0, False, f"unrecognized_unit({clean_unit})")

if __name__ == "__main__":
    test_cases = [
        ("1/2", "cup"),
        ("2", "tbsp"),
        ("1 1/4", "lbs"),
        ("100", "g"),
        ("3", "cloves"),
        ("1", "pinch"),
        ("2", "unknown_unit")
    ]
    print("Testing unit converter:")
    for q, u in test_cases:
        qty = parse_quantity_string(q)
        grams, ok, note = convert_to_grams(qty, u)
        print(f"  {q} {u} -> {grams:.2f}g (converted={ok}, note={note})")
