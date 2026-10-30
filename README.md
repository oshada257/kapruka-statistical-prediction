# 🎯 Kapruka Statistical Prediction Model

A Python-based statistical analysis and experimental prediction project using historical Sri Lankan DLB Kotipathi Kapruka lottery results.

## 📌 Project Overview

This project explores historical lottery results using Python, statistical analysis, frequency analysis, and backtesting.

The goal is to:

- Collect historical lottery results.
- Clean and validate datasets.
- Analyze main-number frequencies.
- Analyze extra-number and letter frequencies.
- Generate candidate combinations.
- Compare statistical methods against a random baseline.
- Evaluate results through historical backtesting.

**Disclaimer:** Lottery draws are random. Historical results cannot guarantee future winning numbers or improve winning odds.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Requests
- CSV
- Git & GitHub

## 📂 Project Structure

```text
Kapruka-Prediction/
│
├── data/
│   ├── kapruka_raw.txt
│   ├── kapruka_clean.csv
│   ├── candidate_combinations.csv
│   └── backtest_report.csv
│
├── collect.py
├── parse_results.py
├── analysis.py
├── validate_dataset.py
├── prediction.py
├── backtest.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 📊 Dataset Information

| Description               | Value |
| ------------------------- | ----: |
| Valid unique records      | 1,792 |
| Selected historical draws | 1,000 |
| First draw ID             |  1506 |
| Last draw ID              |  2505 |
| Invalid source lines      |     1 |
| Main-number observations  | 4,000 |

The dataset includes:

- Draw ID
- Date
- Four main numbers
- English letter
- Extra number field

The dataset is sourced from a community-maintained historical archive and has not been independently verified against every official draw.

## 🔍 Statistical Analysis

Implemented analyses:

1. Main number frequency.
2. Hot number analysis.
3. Cold number analysis.
4. Extra number frequency.
5. English letter frequency.
6. Number distribution charts.

### Initial Findings

- Most frequent extra numbers: 30 and 3 (32 appearances each).
- Most frequent letter: S (47 appearances).
- Least frequent letter: N (28 appearances).

These are historical observations, not future predictions.

## 🤖 Prediction Engine V1.0

Three experimental methods:

### 1. Frequency-Based

Uses historical frequency counts as sampling weights.

### 2. Random Baseline

Generates uniformly random combinations.

### 3. Balanced Method

Generates combinations with:

- Two odd and two even numbers.
- Two low and two high numbers.

Total generated candidate combinations: 10.

| Method    | Combinations |
| --------- | -----------: |
| Frequency |            4 |
| Random    |            3 |
| Balanced  |            3 |

## 🧪 Backtesting Results

The initial experiment used:

- 800 training draws.
- 200 testing draws.
- 100 simulated tickets per test draw.
- Walk-forward evaluation.

| Method    | Average Main Matches | At Least One Main Hit |
| --------- | -------------------: | --------------------: |
| Frequency |               0.2114 |               19.975% |
| Balanced  |               0.2053 |               19.400% |
| Random    |               0.1981 |               18.665% |

### Additional Metrics

| Method    | Extra Number Hit | Letter Hit |
| --------- | ---------------: | ---------: |
| Frequency |           2.565% |     3.770% |
| Balanced  |           2.575% |     3.715% |
| Random    |           2.570% |     3.665% |

The frequency method showed a small difference compared with the random baseline. This does not establish a statistically significant predictive advantage.

## 🚀 Installation and Usage

### Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd kapruka-predictor
```

### Create virtual environment

```bash
python -m venv venv
```

### Activate on Windows

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the project

```bash
python collect.py
python parse_results.py
python analysis.py
python validate_dataset.py
python prediction.py
python backtest.py
```

## 🔮 Future Improvements

- Improve historical data collection.
- Verify official draw formats and number ranges.
- Improve dataset validation.
- Add confidence intervals.
- Perform statistical significance testing.
- Test multiple historical windows.
- Build an interactive dashboard.
- Compare different statistical models.

## ⚠️ Disclaimer

This project is developed for educational and statistical experimentation only.

Lottery draws are random events. Historical frequency patterns and generated combinations cannot guarantee future results or winning outcomes.

## 👨‍💻 Author

**Oshada Kaushalya**

Python | Data Analysis | Statistical Modeling

⭐ Feel free to explore this project and its statistical experiments!
