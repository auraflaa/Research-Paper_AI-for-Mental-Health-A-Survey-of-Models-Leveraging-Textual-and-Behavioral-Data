# Quality Assessment (QA) Scoring Rubric

## Research Paper: *AI for Mental Health: A Survey of Models Leveraging Textual and Behavioral Data*

---

## 1. Introduction

This rubric defines the standardized criteria used to evaluate the methodological quality and risk of bias for studies included in the survey **AI for Mental Health: A Survey of Models Leveraging Textual and Behavioral Data**. The quality assessment framework ensures that findings contributing to the performance saturation analysis are grounded in rigorous, transparent, and reproducible scientific evidence.

---

## 2. Scoring Criteria (5-Point Scale)

Each study is evaluated across **five distinct quality domains**. For each domain, a **binary score** is assigned:

* **1** — Criteria Met
* **0** — Criteria Not Met

The **total QA score** is calculated as the sum of these values.

> **Maximum Possible Score:** 5

### Quality Domains

| Domain          | Identifier (CSV) | Requirement for Score = 1                                                                                           |
| --------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Validity**    | `QA_V`           | Clear definition of the clinical construct (e.g., Anxiety, Depression, Stress) and appropriate labeling methodology |
| **Methodology** | `QA_M`           | Transparent description of model architecture, feature engineering, and hyperparameter selection                    |
| **Data**        | `QA_D`           | Disclosure of dataset provenance, collection environment (Lab vs. Wild), and sample characteristics                 |
| **Bias**        | `QA_B`           | Evidence of mitigation strategies for data leakage, synthetic over-sampling artifacts, or demographic skew          |
| **Rigor**       | `QA_R`           | Use of robust evaluation protocols (e.g., cross-validation) and standard performance metrics                        |

---

## 3. Quality Interpretation Thresholds

Based on the QA scores recorded during the study extraction phase, papers are categorized according to their scientific reliability and analytical utility.

### High Quality (Score: 4–5)

* Minimal risk of bias
* High methodological transparency
* Results considered reliable for clinical or near-clinical benchmarking

### Moderate Quality (Score: 3)

* Minor reporting gaps or limited methodological constraints
* Included for trend-level analysis with explicitly stated caveats

### Low Quality (Score: < 3)

* Significant concerns related to validation rigor, bias control, or metadata disclosure
* Included primarily for landscape completeness and weighted lower in qualitative synthesis

---

## 4. Implementation

The total quality score for each study is computed as:

```
QA_Total = QA_V + QA_M + QA_D + QA_B + QA_R
```

This information is stored in:

```
data/screening_log.csv
```

The resulting QA scores are used to filter, stratify, and weight candidate studies for inclusion in the final analytical synthesis.
