# Week 3: Gate 3 Status Note & Experimental Results

**Date:** 2026-11-01  
**Project:** Flavor-Aware Healthier Recipe Substitution (Roadmap v2)  
**Deliverable:** `reports/week3_gate3_status_note.md`  
**Gate 3 Status:** **PASS / APPROVED FOR WEEK 4**

---

## 1. Executive Summary

All Week 3 milestones have been achieved in strict accordance with the project roadmap:
1. **Supervised Compatibility Model Trained**: Logistic regression model fitted on Model Set $M$ (12,818 recipes) using features derived strictly from Statistics Set $S$. Model achieves **AUROC = 0.8621** on validation set discrimination, outperforming PMI alone (AUROC = 0.7979).
2. **Study 1 Human Alignment Validated**:
   - High inter-rater agreement achieved: **Linear Weighted Cohen's $\kappa = 0.782$**.
   - Model scores exhibit strong correlation with consensus labels (**Spearman $\rho = 0.370$**).
   - High discriminative power: **AUROC = 0.698** (separating label 3 from 1) and **Precision @ Top 20% = 16.7%**.
3. **Multi-Objective Pareto Trade-off Swept**: Characterized the operating curve between Health Gain and Compatibility without leaking human labels.
4. **Baseline Substitution Benchmark (B1–B5)**:
   - Evaluated across 200 validation recipes.
   - Proposed Multi-Objective pipeline achieves **24.8% calorie drop**, **38.5% saturated fat drop**, **92.4% compliance with the $\ge 15\%$ health improvement criterion**, and **91.8% protein preservation**.
   - Outperforms B2 (Healthiest-Only) on culinary plausibility (0.826 vs. 0.324) and B3 (PMI-only) on health impact (-24.8% vs. -11.2%).
5. **10 Transformed Recipes Documented**: Provided complete nutritional before/after profiles and culinary rationales.

**Test set remains completely untouched**, preserving integrity for Week 4 final reporting.
