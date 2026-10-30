
import pandas as pd

df = pd.read_csv("data/kapruka_clean.csv")

main_cols = ["n1", "n2", "n3", "n4"]

print("===== DATA VALIDATION =====")

# Main number range
main = df[main_cols].values.flatten()

print("Main numbers range:", main.min(), "-", main.max())
print("Main numbers outside 1-77:", ((main < 1) | (main > 77)).sum())

# Super number range
super_numbers = df["super_number"]

print("Super range:", super_numbers.min(), "-", super_numbers.max())
print("Super numbers outside 1-40:",
      ((super_numbers < 1) | (super_numbers > 40)).sum())

# Duplicate main numbers within a draw
duplicates = df[main_cols].apply(
    lambda row: row.nunique() != 4, axis=1
)

print("Draws with repeated main numbers:", duplicates.sum())

# Duplicate draw IDs
print("Duplicate draw IDs:", df["draw_id"].duplicated().sum())

# Missing values
print("Missing values:\n", df.isnull().sum())

# Frequency totals
print("Total main number observations:", len(main))
print("Total Super Number observations:", super_numbers.count())

# Most frequent main numbers
print("\nTOP 10 HOT NUMBERS")
print(pd.Series(main).value_counts().head(10))

# Most frequent Super Numbers
print("\nTOP 10 HOT SUPER NUMBERS")
print(super_numbers.value_counts().head(10))

print("\nValidation completed!")
