# AI for Mental Health
## A Survey of Models Leveraging Textual and Behavioral Data

This repository contains the **complete reproduction package** for the systematic survey:

> **“AI for Mental Health: A Survey of Models Leveraging Textual and Behavioral Data”**

The work examines AI-based detection of **Anxiety, Depression, and Stress (ADS)** using textual and behavioral signals, with a particular focus on **methodological rigor**, **evaluation validity**, and **deployment readiness** rather than headline accuracy improvements.

---

## 📌 Abstract

Recent advances in Deep Learning for ADS detection frequently report substantial performance gains over classical approaches. However, through a systematic review and paired statistical analysis, we identify a **performance saturation plateau**—where increasingly complex architectures yield **diminishing returns** once controls for **data leakage**, **evaluation protocol rigor**, and **sample provenance** are enforced.

Using paired within-study comparisons, we observe statistically significant saturation:

- **Wilcoxon Signed-Rank Test:** p = 0.0244  
- **Cliff’s Delta:** 0.5950 (large effect size)

To address the persistent gap between **research prototypes** and **deployable clinical systems**, we introduce an **Operational Readiness Checklist (ORC)**—a structured auditing framework for assessing whether a model meets minimum standards for responsible deployment.

---

## 📂 Repository Structure

```text
Research-Paper_AI-for-Mental-Health/
├── data/
│   ├── screening_log.csv       # PRISMA screening records (N=92)
│   ├── study_extraction.csv    # Extracted features & metrics (N=27)
│   └── paired_comparisons.csv  # Data pairs for saturation hypothesis testing
│
├── scripts/
│   ├── validate_prism.py       # Validates data integrity & synchronization
│   ├── analyze_saturation.py   # Statistical engine (Wilcoxon / Cliff's Delta)
│   └── generate_orc.py         # Generates Operational Readiness reports
│
├── figures/
│   ├── saturation_plot.pdf     # Visual evidence of the performance plateau
│   └── prisma_flow.pdf         # PRISMA 2020 inclusion flowchart
│
├── refs/                       # PDF artifacts & metadata placeholders
└── README.md                   # This file
```

---

## 🚀 Reproduction Workflow

### 1. Environment Setup

```bash
git clone https://github.com/auraflaa/Research-Paper_AI-for-Mental-Health-A-Survey-of-Models-Leveraging-Textual-and-Behavioral-Data.git
cd Research-Paper_AI-for-Mental-Health-A-Survey-of-Models-Leveraging-Textual-and-Behavioral-Data
pip install -r requirements.txt
```

### 2. Data Integrity Check

Verify that the PRISMA screening log is synchronized with the extraction ledger.

```bash
python scripts/validate_prism.py
```

**Expected output:**

```
[PASS] All data artifacts verified for archive
```

### 3. Statistical Analysis (Saturation Hypothesis)

Compute paired statistical tests to evaluate performance saturation.

```bash
python scripts/analyze_saturation.py
```

**Validated results:**

- p-value: 0.0244 (significant at α = 0.05)  
- Cliff’s Delta: 0.5950 (large effect)

### 4. Operational Readiness Audit

Generate model-level readiness classifications.

```bash
python scripts/generate_orc.py
```

---

## 🛠 Operational Readiness Checklist (ORC)

Models are evaluated on a 5-point scale across the following criteria:

1. **Provenance** — Clear disclosure of dataset origin  
2. **Modality** — Diversity and independence of input units  
3. **Rigor** — Use of cross-validation or leave-one-out protocols  
4. **Bias Mitigation** — Avoidance of synthetic oversampling (e.g., SMOTE)  
5. **Transparency** — Explicit reporting of sample size (N)

A score of **≥ 4 / 5** is required for a model to be classified as **CLINICAL READY**.

---

## 📄 Citation

If you use this repository or its findings, please cite:

```bibtex
@article{MukherjeePandey2025ADS,
  title   = {AI for Mental Health: A Survey of Models Leveraging Textual and Behavioral Data},
  author  = {Mukherjee, Priyangshu and Pandey, Khusboo},
  journal = {Systematic Review Repository},
  year    = {2025},
  url     = {https://github.com/auraflaa/Research-Paper_AI-for-Mental-Health-A-Survey-of-Models-Leveraging-Textual-and-Behavioral-Data}
}
```

---

**Maintainer:** Priyangshu Mukherjee
