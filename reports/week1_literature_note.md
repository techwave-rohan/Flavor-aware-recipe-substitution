# Week 1: Literature Review & Novelty Positioning Note

**Date:** 2026-10-31  
**Deliverable:** `reports/week1_literature_note.md`  
**Status:** Completed Task 2 of Week 1 according to `Agent Roadmap v2`.

---

## 1. Key Prior Work Analyzed

### 1.1 Jain, Rakhi, & Bagler (2015) — *Analysis of Food Pairing in Regional Cuisines of India* (PLOS ONE)
- **Core Finding**: Investigated the food-pairing hypothesis (ingredients sharing flavor compounds tend to co-occur) across regional Indian cuisines. Found a characteristic **negative food pairing pattern** in Indian cuisine (ingredients co-occur *less* frequently than expected by chance if they share flavor compounds), contrasting sharply with Western cuisines (which exhibit positive food pairing).
- **Relevance to our project**:
  - Highlights that flavor compound sharing alone cannot be treated as a universal positive indicator of culinary compatibility.
  - Dictates that our compatibility metrics must evaluate **both co-occurrence (PMI)** and **flavor sharing (FlavorDB Jaccard)**, broken down per cuisine.
  - Emphasizes the need for cuisine-stratified evaluation rather than pooling all global recipes into an aggregate metric.

### 1.2 Shirai et al. (2021) — *Identifying Ingredient Substitutions Using a Knowledge Graph of Food* (Frontiers in AI)
- **Core Finding**: Leveraged a food Knowledge Graph (FoodKG) combining RecipeDB, FlavorDB, and USDA nutrition data to infer ingredient substitutions using graph embeddings and relation prediction. Evaluated substitutions primarily by culinary plausibility and functional category matching.
- **Relevance & Overlaps**:
  - Shirai et al. established that culinary taxonomy/category is the strongest constraint for function-safe substitution (e.g., swapping a fat for another fat, a leafy green for a leafy green).
  - Evaluated substitutions using ranking metrics (MRR, Hits@K).
- **Key Limitations in Shirai et al. addressed by our work**:
  - Did not formalize a constrained, quantitative **health optimization pipeline** ($\ge 15\%$ drop in target negative nutrient, $\pm 20\%$ protein preservation, dietary style retention).
  - Lacked rigorous paired bootstrap confidence intervals to establish statistical significance between competing measures.
  - Did not perform an independent human validation study stratified across disagreement quadrants of PMI vs. Flavor sharing (our Study 1).

### 1.3 Batra et al. (2020) — *RecipeDB: A Resource for Exploring Recipes* (Database, Oxford)
- **Core Contribution**: Structured resource parsing 118,171 recipes across 26 geopolitical regions into ingredient quantities, units, preparation states, 29 functional categories, and estimated nutrient profiles.
- **Role in our project**: Serves as the primary ground truth for ingredient gram quantities, categories, and nutrient density calculations.

---

## 2. Direct Overlap vs. Novelty Boundaries

| Dimension | Prior Work (Shirai 2021 / Bagler 2015) | Our Research Pipeline | Novelty & Positioning |
|---|---|---|---|
| **Objective** | Unconstrained substitution discovery or standalone food pairing analysis | Targeted **healthier substitution** under strict multi-objective constraints ($\Delta\text{Nutrient} \ge 15\%$, $\Delta\text{Protein} \le 20\%$) | **Primary Novelty**: Joint optimization of health gain, culinary function, and flavor compatibility |
| **Compatibility Modeling** | Pure embedding similarity or graph link prediction | Comparative benchmark: Popularity vs. PMI vs. FlavorDB Jaccard vs. Learned Embeddings vs. Supervised Model | **Systematic Benchmark**: Quantifies exactly when and where flavor compound data adds value over co-occurrence |
| **Statistical Rigor** | Point estimates (mean MRR / Hits@K) | Paired bootstrap 95% confidence intervals ($\ge 1,000$ iterations) on differences | **Methodological Rigor**: Explicitly reports null results when differences cross zero |
| **Human Validation** | Anecdotal checks or unstratified crowdsourced ratings | **Study 1**: Manual evaluation of ~100 Type B replacement pairs stratified across 4 quadrants of PMI $\times$ Flavor sharing | **Independent Ground Truth**: Directly measures model agreement with human cooks in conflict zones |
| **Cuisine Stratification** | Mostly Western or standalone Indian studies | Unified per-cuisine comparison testing positive vs. negative food-pairing regimes | **Novel Insight**: Documents where flavor sharing helps vs. hurts across diverse cuisines |

---

## 3. Threats to Novelty & Risk Mitigations

1. **Risk of Overclaiming Novelty**:
   - *Mitigation*: We do not claim novelty for the concept of ingredient substitution or food pairing analysis. We explicitly frame our contribution as a **controlled, multi-objective evaluation pipeline** with pre-registered baseline comparisons and human alignment in disagreement strata.
2. **Risk that Flavor Sharing Does Not Outperform Co-occurrence**:
   - *Mitigation*: As instructed by the roadmap, if FlavorDB Jaccard fails to beat simple co-occurrence (PMI) or the popularity baseline, we report this honestly as a **valuable negative/null finding** reflecting the nuances of food pairing across world cuisines.
3. **Risk of Popularity Shortcut**:
   - *Mitigation*: We incorporate the popularity baseline (ingredient frequency in $S$) in every hide-and-recover and pair scoring comparison to ensure models do not merely exploit common ingredient priors.
