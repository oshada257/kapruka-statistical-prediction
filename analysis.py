
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load dataset
df = pd.read_csv("data/kapruka_clean.csv")

# Main number frequency
main_numbers = df[["n1", "n2", "n3", "n4"]].values.flatten()

main_freq = (
    pd.Series(main_numbers)
    .value_counts()
    .sort_values(ascending=False)
)

print("\n===== MAIN NUMBER FREQUENCY =====")
print(main_freq.head(15))

print("\n===== TOP 10 COLD NUMBERS =====")
print(main_freq.tail(10))

# Extra number frequency
extra_freq = df["super_number"].value_counts()

print("\n===== EXTRA NUMBER FREQUENCY =====")
print(extra_freq.sort_values(ascending=False).head(10))

# Letter frequency
letter_freq = df["letter"].value_counts()

print("\n===== LETTER FREQUENCY =====")
print(letter_freq)

# Main number chart
main_freq.sort_index().plot(
    kind="bar",
    figsize=(14, 5),
    title="Kapruka Main Number Frequency"
)

plt.xlabel("Number")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("data/main_frequency.png")
plt.show()

# Extra number chart
extra_freq.sort_index().plot(
    kind="bar",
    figsize=(12, 5),
    title="Kapruka Extra Number Frequency"
)

plt.xlabel("Extra Number")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("data/extra_frequency.png")
plt.show()

# Letter chart
letter_freq.sort_index().plot(
    kind="bar",
    figsize=(12, 5),
    title="Kapruka Letter Frequency"
)

plt.xlabel("Letter")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("data/letter_frequency.png")
plt.show()

print("\nAnalysis completed!")
