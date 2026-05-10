# Student Performance & Academic Analytics

## Overview

This project analyzes academic, behavioral, and demographic factors associated with student performance using the UCI Student Performance Dataset accessed through Kaggle.

The project combines:
- exploratory data analysis (EDA)
- feature engineering
- statistical visualization
- interactive dashboarding with Streamlit and Plotly

The primary goal of the project is to identify patterns related to academic success and academic risk.

---

## Research Question

> Which academic, behavioral, and demographic factors are most strongly associated with student performance?

---

## Dataset

- Source: Kaggle (UCI Student Performance Dataset mirror)
- Dataset includes:
  - student grades (`G1`, `G2`, `G3`)
  - absences
  - study time
  - past failures
  - alcohol consumption
  - internet access
  - family and demographic variables

---

## Feature Engineering

Several engineered features were created to improve analysis and interpretability:

| Feature | Description |
|---|---|
| `avg_grade` | Average of G1, G2, and G3 |
| `grade_change` | Final grade minus first-period grade |
| `total_alcohol` | Combined weekday + weekend alcohol consumption |
| `performance_band` | Categorized student performance levels |
| `is_high_absence` | Flag for students above the 75th percentile in absences |

---

## Key Findings

### Academic trajectory matters most
Earlier grades, especially G2, strongly predict final academic performance.

### Past failures are major warning indicators
Students with more previous failures consistently achieved lower final grades.

### Attendance matters
Higher absence counts were generally associated with weaker academic performance.

### Study habits matter, but not alone
Higher study time was associated with stronger performance, although substantial variation remained.

### Behavioral and academic variables appear more informative than broad demographic differences
Academic history and attendance patterns showed stronger relationships with performance than many demographic splits.

### Correlation does not imply causation
The project identifies associations rather than guaranteed causal relationships.

---

## Dashboard Features

The Streamlit dashboard includes:
- Interactive Plotly visualizations
- Dynamic filtering
- Correlation heatmaps
- Academic risk analysis
- Attendance analysis
- Behavioral factor exploration
- KPI overview metrics

---

## Technologies Used

- Python
- Pandas
- Plotly
- Streamlit
- NumPy
- Matplotlib
- Seaborn

---

## Project Structure

```plaintext
student-performance-analytics/
│
├── app.py
├── student_data.csv
├── README.md
├── requirements.txt
├── presentation.pptx
└── notebooks/
```

---

## How to Run the Dashboard

### 1. Clone Repository

```bash
git clone https://github.com/nikishrajbastola/student-performance-analytics.git
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run Streamlit App

```bash
streamlit run app.py
```

---

## Streamlit Dashboard

The dashboard provides an interactive environment for exploring:
- academic trajectory
- attendance patterns
- study habits
- performance distributions
- student risk indicators

---

## Limitations

- Correlation does not imply causation
- Some variables are self-reported
- Dataset scope is limited
- Some relationships may involve hidden variables or selection effects

---

## Author

Nikish Bastola  
Texas State University  
Spring 2026
