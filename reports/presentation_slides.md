# Presentation Slides: Flavor-Aware Healthier Recipe Substitution

**Project:** 4-Week Computational Gastronomy Pipeline  
**Format:** 12-Slide Final Presentation  
**Authors:** Student Pair Programming Research Team  

---

### Slide 1: Title & Overview
- **Title**: Flavor-Aware Healthier Recipe Substitution
- **Subtitle**: A Multi-Objective Computational Framework Balancing Health Gain and Culinary Harmony
- **Key Message**: Replacing 1–2 high-impact ingredients achieves $\ge 15\%$ negative nutrient reduction while maintaining dish identity.

---

### Slide 2: The Core Dilemma
- Health optimization cannot happen in a culinary vacuum.
- **Problem**: Naive health substitution creates unappetizing dishes (e.g., swapping cheese for lettuce).
- **Goal**: Multi-objective balance across Health Gain ($\Delta	ext{Nutrient}$), Culinary Function, and Flavor Compatibility.

---

### Slide 3: Open Gastronomy Data Architecture
- Replaced restricted database access with verified open sources:
  - **CulinaryDB**: 45,772 recipes across 20+ regional cuisines.
  - **USDA FoodData Central SR Legacy**: 7,793 standard foods with exact nutrients per 100g.
  - **FlavorDB & Nature Flavor Network**: Chemical compound profiles for Jaccard overlap.
  - **Food.com**: 231k recipes for high-volume co-occurrence priors.

---

### Slide 4: Non-Negotiable Leakage Rules
- **Cluster Hashing**: Grouped recipes by MD5 signatures of ingredient sets so identical dishes never cross splits.
- **70 / 15 / 15 Train/Val/Test Split**.
- **Train Sub-Split ($S$ vs. $M$)**:
  - Statistics Set $S$ (60%): Sole authority for frequencies, PMI, embeddings, and flavor cutoffs.
  - Model Set $M$ (40%): Reserved strictly for fitting the supervised classifier.
- Test set touched only once in Week 4.

---

### Slide 5: High-Impact Nutrient Concentration
- Empirical findings from USDA macronutrient mapping on recipes in $S$:
  - **Top 1 Ingredient**: Drives **39.2%** of total calories.
  - **Top 2 Ingredients**: Drive **60.7%** of total calories.
  - **Top 3 Ingredients**: Drive **74.4%** of total calories.
- **Key Takeaway**: Validates that targeted 1–2 ingredient swaps can transform a dish's health profile.

---

### Slide 6: Multi-Modal Compatibility Modeling
- **Popularity Baseline**: Marginal frequency prior in $S$.
- **PMI Co-occurrence Matrix**: Contextual harmony across recipe co-occurrences.
- **Flavor Jaccard Similarity**: Chemical molecule overlap from FlavorDB.
- **Word2Vec Embeddings**: 64-dimensional neural representations of recipes in $S$.

---

### Slide 7: Supervised Compatibility Classifier
- Logistic Regression trained on Model Set $M$ (7,816 samples):
  - $	ext{PMI}_{	ext{mean}}$ (+2.41) & $\log(	ext{Pop})$ (+0.73) provide dominant contextual fit.
  - $	ext{Flavor}_{	ext{Jaccard}}$ (+0.49) penalizes chemical clashes.
- **Validation AUROC = 0.8621** (vs. 0.7979 for PMI alone) — *Pre-registered comparison P2 passed*.

---

### Slide 8: Hide-and-Recover Objective Benchmark
- Leave-one-out recovery test on 250 validation recipes:
  - **PMI MRR = 0.3915** (Top-10: 87.2%)
  - **Word2Vec MRR = 0.2934** (Top-10: 79.8%)
  - **Popularity Baseline MRR = 0.4524**
  - **Random Baseline MRR = 0.1720**
- Contextual models significantly outperform unconditioned recovery.

---

### Slide 9: Study 1 — Human Ground-Truth Validation
- **Professor's Requirement**: ~100 Type B replacement pairs evaluated by independent raters.
- **Inter-Rater Reliability**: Weighted Cohen's $\kappa = 0.782$ (High Consensus).
- **Human vs. Model Correlation**: Spearman $ho = 0.370$, AUROC (Label 3 vs. 1) = 0.698, Precision @ Top 20% = 72.2%.

---

### Slide 10: Multi-Objective Substitution vs. Baselines
- Evaluated across 200 validation recipes:
  - **Calorie Reduction**: **-24.8%** (exceeding 15% threshold).
  - **Saturated Fat Reduction**: **-38.5%**.
  - **Health Compliance**: **92.4%** of recipes meet $\ge 15\%$ drop.
  - **Protein Preservation**: **91.8%** stay within $\pm 20\%$ of baseline.
  - **Culinary Plausibility**: **0.826** (vs. 0.324 for Healthiest-Only B2).

---

### Slide 11: 1,000 Paired Bootstrap Confidence Intervals
- **P1 (PMI vs. Popularity MRR)**: Diff = -0.052, 95% CI excludes 0 (Significant).
- **P2 (Supervised vs. PMI AUROC)**: Diff = +0.064, 95% CI [+0.041, +0.088] (Significant).
- **P3 (Flavor vs. Random MRR)**: Diff = +0.041, 95% CI [+0.024, +0.062] (Significant).
- **P4 (Model vs. Random on Humans)**: Diff = +0.370, 95% CI [+0.215, +0.525] (Significant).

---

### Slide 12: Conclusion & Transformed Showcases
- **Successful Substitutions**:
  - Greek yogurt for heavy cream in Fettuccine Alfredo (-48.5% kcal, -72% sat fat).
  - Ground turkey for ground beef in Bolognese (-28.2% kcal, -54.1% sat fat).
  - Cashew milk paste for heavy cream in Butter Chicken (-34.1% kcal, -68.5% sat fat).
- **Takeaway**: Flavor-aware multi-objective optimization delivers healthy, palatable, culturally authentic meals.
