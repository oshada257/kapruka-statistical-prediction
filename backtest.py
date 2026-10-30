
import pandas as pd
import numpy as np
from collections import Counter

# Configuration
FILE = "data/kapruka_clean.csv"
TRAIN_SIZE = 800
SIMULATIONS = 100
rng = np.random.default_rng(42)

df = pd.read_csv(FILE).sort_values("draw_id").reset_index(drop=True)

MAIN = ["n1", "n2", "n3", "n4"]
LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

if len(df) != 1000:
    raise ValueError("Expected exactly 1000 draws")

if df[MAIN + ["super_number", "letter"]].isnull().any().any():
    raise ValueError("Missing values found")

if not df[MAIN].apply(
    lambda row: row.nunique() == 4, axis=1
).all():
    raise ValueError("Duplicate main numbers found")

def weighted_pick(options, freq, count):
    weights = np.array(
        [freq.get(x, 0) + 1 for x in options],
        dtype=float
    )
    weights /= weights.sum()
    return rng.choice(
        options, size=count, replace=False, p=weights
    ).tolist()

def make_ticket(history, method):
    main_values = history[MAIN].values.flatten()
    super_values = history["super_number"].tolist()
    letter_values = history["letter"].str.upper().tolist()

    main_freq = Counter(main_values)
    super_freq = Counter(super_values)
    letter_freq = Counter(letter_values)

    if method == "Frequency":
        numbers = weighted_pick(range(1, 81), main_freq, 4)
        super_no = weighted_pick(range(1, 41), super_freq, 1)[0]
        letter = weighted_pick(LETTERS, letter_freq, 1)[0]

    elif method == "Random":
        numbers = rng.choice(range(1, 81), 4, replace=False).tolist()
        super_no = int(rng.choice(range(1, 41)))
        letter = str(rng.choice(LETTERS))

    else:  # Balanced
        groups = [
            range(1, 41, 2),
            range(2, 41, 2),
            range(41, 81, 2),
            range(42, 81, 2)
        ]

        numbers = [int(rng.choice(list(g))) for g in groups]
        super_no = int(rng.choice(range(1, 41)))
        letter = str(rng.choice(LETTERS))

    return set(numbers), super_no, letter

methods = ["Frequency", "Random", "Balanced"]
results = []

# Walk-forward test
for i in range(TRAIN_SIZE, len(df)):

    history = df.iloc[:i]
    actual = df.iloc[i]

    actual_main = set(actual[MAIN].tolist())
    actual_super = int(actual["super_number"])
    actual_letter = str(actual["letter"]).upper()

    for method in methods:

        for _ in range(SIMULATIONS):

            predicted_main, predicted_super, predicted_letter = (
                make_ticket(history, method)
            )

            matches = len(predicted_main & actual_main)

            results.append({
                "method": method,
                "main_matches": matches,
                "any_main_hit": matches >= 1,
                "four_main_hit": matches == 4,
                "super_hit": predicted_super == actual_super,
                "letter_hit": predicted_letter == actual_letter
            })

# Summary
results_df = pd.DataFrame(results)

summary = results_df.groupby("method").agg(
    average_main_matches=("main_matches", "mean"),
    any_main_hit_pct=("any_main_hit", "mean"),
    four_main_hit_pct=("four_main_hit", "mean"),
    super_hit_pct=("super_hit", "mean"),
    letter_hit_pct=("letter_hit", "mean")
)

summary = summary * 100
summary["average_main_matches"] = (
    results_df.groupby("method")["main_matches"].mean()
)

print("\n===== BACKTEST RESULTS =====")
print(summary.round(4).to_string())

summary.to_csv("data/backtest_report.csv")

print("\nBacktesting completed!")
print("Report saved: data/backtest_report.csv")

