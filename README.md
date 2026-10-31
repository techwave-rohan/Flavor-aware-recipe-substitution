# Flavor-Aware Healthier Recipe Substitution

A computational research pipeline to build and evaluate flavor-aware, healthier recipe substitutions.

## Overview

Given a recipe, this project aims to replace 1 to 3 ingredients contributing disproportionately to specific health concerns (e.g., high sugar, sodium, or saturated fat) with healthier functional alternatives while preserving:
- **Flavor compatibility** (evaluated using flavor networks / FlavorDB, PMI co-occurrence, and embedding similarity)
- **Culinary function and texture constraints**
- **Dietary style and overall culinary coherence**

## Project Roadmap

This project follows a 4-week structured milestone roadmap:
- **Week 1**: Data Access & Inspection, Normalization, Literature Check, and Baseline Setup (RecipeDB, FlavorDB, Food.com).
- **Week 2**: Nutrition per serving calculation, high-impact ingredient targeting, candidate generation, compatibility measures, and hide-and-recover validation.
- **Week 3**: Supervised model training, baselines, end-to-end swap pipeline, and human evaluation.
- **Week 4**: Frozen test run, statistical significance & bootstrap analysis, final report, and demonstration.

## Reference Material

- See [`Antigravity Agent Roadmap Flavor-Aware Healthier Recipe Substitution.pdf`](./Antigravity%20Agent%20Roadmap%20Flavor-Aware%20Healthier%20Recipe%20Substitution.pdf) for the comprehensive project specification and evaluation gates.
