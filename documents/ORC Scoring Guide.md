# Operational Readiness Checklist (ORC): Technical Scoring Guide

## Research Paper: *AI for Mental Health: A Survey of Models Leveraging Textual and Behavioral Data*

---

## 1. Overview

The **Operational Readiness Checklist (ORC)** is a standardized diagnostic framework used in this survey to evaluate the gap between **theoretical model performance** and **real-world clinical utility**. While systematic reviews typically emphasize statistical outcomes (e.g., accuracy or F1-score), the ORC explicitly audits **methodological transparency**, **validation rigor**, and **deployment feasibility** of Anxiety, Depression, and Stress (ADS) detection models.

---

## 2. The 5-Point Scoring Framework

A **binary score (0 or 1)** is assigned to each of the following technical dimensions. The total ORC score ranges from **0 to 5**.

### 1. Provenance — Dataset Source Disclosure

**Requirement for Score = 1**
The study must explicitly name the dataset (e.g., WESAD, Dreaddit, DAIC-WOZ) or provide a persistent identifier.

**Goal**
Prevent opaque or "black-box" training on unverified or proprietary datasets that cannot be audited for clinical bias.

---

### 2. Modality — Sample Unit Transparency

**Requirement for Score = 1**
The model must clearly define its input granularity (e.g., single social media post, multi-day timeline, or physiological signal windows such as 60-second intervals).

**Goal**
Ensure clinical interpretability and contextual validity of the reported predictions.

---

### 3. Rigor — Advanced Validation Protocols

**Requirement for Score = 1**
A point is awarded only if the model employs **k-fold cross-validation**, **Leave-One-Out (LOO)** validation, or **nested validation**. Studies relying solely on a single hold-out split (e.g., 80/20) do not meet this criterion.

**Goal**
Verify that reported performance is not an artifact of a favorable random split.

---

### 4. Bias Control — Avoidance of Synthetic Augmentation

**Requirement for Score = 1**
The study must avoid synthetic minority over-sampling techniques (e.g., SMOTE) or generative data augmentation for performance reporting.

**Goal**
Clinical environments are inherently imbalanced; models must demonstrate robustness under real-world prevalence distributions without artificial balancing.

---

### 5. Metadata — Numeric N-Disclosure

**Requirement for Score = 1**
The exact sample size (**N**) must be reported as a verifiable integer. Vague descriptors such as "large cohort" without precise counts fail this criterion.

**Goal**
Enable reproducibility, meta-analysis, and statistical power assessment.

---

## 3. Revised Interpretation Thresholds

Based on the empirical distribution of ORC scores in the current survey (**N = 27**), model readiness is categorized as follows:

### Score 5/5 — CLINICAL GRADE

The **gold standard**. These models exhibit complete transparency, strict bias control, and rigorous validation. They are suitable for immediate pilot testing in clinical decision-support systems.

### Score 4/5 — TRANSITIONAL PROTOTYPE

High-quality research models that typically miss only one criterion (often advanced validation) or exhibit minimal augmentation. These represent the current **state of the art**, pending one final deployment-level validation hurdle.

### Score ≤ 3 — RESEARCH PROTOTYPE

Proof-of-concept models. Despite potentially high reported accuracy, methodological gaps or reliance on synthetic data render their real-world clinical utility unverified.

---

## 4. Audit Log Generation

The ORC audit report can be reproduced automatically using the provided script:

```
python scripts/generate_orc.py
```

This script audits the following file:

```
data/study_extraction.csv
```

and generates the final readiness report:

```
data/orc_report.csv
```
