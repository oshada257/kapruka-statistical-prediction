
import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter

# ==================================
# KAPRUKA PREDICTION ENGINE V1.0
# ==================================

DATA_FILE = Path("data/kapruka_clean.csv")
OUTPUT_FILE = Path("data/candidate_combinations.csv")

MAIN_MIN, MAIN_MAX = 1, 80
SUPER_MIN, SUPER_MAX = 1, 40

NUMBER_COLUMNS = ["n1", "n2", "n3", "n4"]

rng = np.random.default_rng(42)

# Load historical dataset
df = pd.read_csv(DATA_FILE)

required = NUMBER_COLUMNS + ["super_number", "letter"]

if not all(col in df.columns for col in required):
    raise ValueError("Required columns are missing from CSV.")

if df[required].isnull().any().any():
    raise ValueError("Dataset contains missing values.")

# Validate number ranges
main_values = df[NUMBER_COLUMNS].to_numpy().flatten()
super_values = df["super_number"].astype(int)

if not np.all((main_values >= MAIN_MIN) & (main_values <= MAIN_MAX)):
    raise ValueError("Main numbers outside 1-80. Check lottery rules.")

if not np.all((super_values >= SUPER_MIN) & (super_values <= SUPER_MAX)):
    raise ValueError("Super numbers outside 1-40. Check lottery rules.")

if df["letter"].astype(str).str.fullmatch(r"[A-Za-z]").eq(False).any():
    raise ValueError("Invalid English letters found.")

if df[NUMBER_COLUMNS].apply(
    lambda row: row.nunique() != 4, axis=1
).any():
    raise ValueError("Duplicate main numbers found in a draw.")

# Calculate frequencies
main_freq = Counter(main_values)
super_freq = Counter(super_values)
letter_freq = Counter(df["letter"].str.upper())

all_main = np.arange(MAIN_MIN, MAIN_MAX + 1)
all_super = np.arange(SUPER_MIN, SUPER_MAX + 1)
all_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def weighted_pick(options, frequencies, count=1):
    """Select unique values using historical frequency weights."""
    weights = np.array(
        [frequencies.get(x, 0) for x in options],
        dtype=float
    )

    if weights.sum() == 0:
        weights = np.ones(len(options))

    weights = weights / weights.sum()

    return rng.choice(
        options,
        size=count,
        replace=False,
        p=weights
    ).tolist()


def generate_frequency():
    numbers = weighted_pick(all_main, main_freq, 4)
    numbers.sort()

    super_number = weighted_pick(all_super, super_freq)[0]
    letter = weighted_pick(all_letters, letter_freq)[0]

    return numbers, super_number, letter


def generate_random():
    numbers = sorted(
        rng.choice(all_main, size=4, replace=False).tolist()
    )

    super_number = int(rng.choice(all_super))
    letter = str(rng.choice(all_letters))

    return numbers, super_number, letter


def generate_balanced():
    # One number from each group:
    # Low odd, Low even, High odd, High even

    groups = [
        np.arange(1, 41, 2),
        np.arange(2, 41, 2),
        np.arange(41, 81, 2),
        np.arange(42, 81, 2)
    ]

    numbers = [
        int(rng.choice(group))
        for group in groups
    ]

    numbers.sort()

    super_number = int(rng.choice(all_super))
    letter = str(rng.choice(all_letters))

    return numbers, super_number, letter


# Generate 10 candidate combinations
results = []

methods = [
    ("Frequency", generate_frequency, 4),
    ("Random", generate_random, 3),
    ("Balanced", generate_balanced, 3)
]

for method_name, generator, quantity in methods:

    for i in range(quantity):

        numbers, super_number, letter = generator()

        results.append({
            "method": method_name,
            "combination": i + 1,
            "n1": numbers[0],
            "n2": numbers[1],
            "n3": numbers[2],
            "n4": numbers[3],
            "super_number": super_number,
            "letter": letter
        })


# Display results
output = pd.DataFrame(results)

print("\n====================================")
print("     KAPRUKA PREDICTION ENGINE")
print("====================================")

print("\nHistorical draws analysed:", len(df))

for method in ["Frequency", "Random", "Balanced"]:

    print(f"\n===== {method.upper()} =====")

    print(
        output[output["method"] == method]
        .to_string(index=False)
    )

# Save CSV
OUTPUT_FILE.parent.mkdir(exist_ok=True)

output.to_csv(OUTPUT_FILE, index=False)

print("\n====================================")
print("Total combinations:", len(output))
print("Saved to:", OUTPUT_FILE)
print("====================================")
