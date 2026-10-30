
import csv
from pathlib import Path
from datetime import datetime

INPUT_FILE = Path("data/kapruka_raw.txt")
OUTPUT_FILE = Path("data/kapruka_clean.csv")
ERROR_FILE = Path("data/invalid_records.csv")

valid_records = []
invalid_records = []

with INPUT_FILE.open("r", encoding="utf-8-sig") as file:
    reader = csv.reader(file)

    for line_no, row in enumerate(reader, start=1):
        try:
            # Expected: 7 fields or 8 fields
            if len(row) not in (7, 8):
                raise ValueError(
                    f"Expected 7 or 8 fields, got {len(row)}"
                )

            draw_id = int(row[0].strip())

            date_text = row[1].strip().split()[0]
            draw_date = datetime.strptime(
                date_text, "%Y-%b-%d"
            ).strftime("%Y-%m-%d")

            letter = row[2].strip().upper()

            if len(letter) != 1 or not letter.isalpha() or not letter.isascii():
                raise ValueError("Invalid English letter")

            numbers = [int(x.strip()) for x in row[3:7]]

            if len(set(numbers)) != 4:
                raise ValueError("Duplicate main numbers")

            if any(n < 1 for n in numbers):
                raise ValueError("Invalid main number")

            # Extra number is optional in older records
            super_number = (
                int(row[7].strip()) if len(row) == 8 else None
            )

            if super_number is not None and super_number < 1:
                raise ValueError("Invalid extra number")

            valid_records.append({
                "draw_id": draw_id,
                "date": draw_date,
                "letter": letter,
                "n1": numbers[0],
                "n2": numbers[1],
                "n3": numbers[2],
                "n4": numbers[3],
                "super_number": super_number
            })

        except Exception as error:
            invalid_records.append({
                "line": line_no,
                "raw_data": ",".join(row),
                "reason": str(error)
            })

# Remove duplicate draw IDs
unique_records = {}

for record in valid_records:
    unique_records[record["draw_id"]] = record

records = sorted(
    unique_records.values(),
    key=lambda x: x["draw_id"],
    reverse=True
)

# Select latest 1000 records
latest_1000 = records[:1000]

# Save in chronological order
latest_1000.reverse()

OUTPUT_FILE.parent.mkdir(exist_ok=True)

columns = [
    "draw_id", "date", "letter",
    "n1", "n2", "n3", "n4", "super_number"
]

with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(latest_1000)

# Save invalid records for inspection
with ERROR_FILE.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["line", "raw_data", "reason"]
    )
    writer.writeheader()
    writer.writerows(invalid_records)

print("\n===== KAPRUKA DATA REPORT =====")
print("Valid unique draws:", len(records))
print("Selected draws:", len(latest_1000))
print("Invalid lines:", len(invalid_records))
print("Records with extra number:", sum(
    r["super_number"] is not None for r in latest_1000
))
print("Records without extra number:", sum(
    r["super_number"] is None for r in latest_1000
))
print("First draw:", latest_1000[0]["draw_id"] if latest_1000 else "None")
print("Last draw:", latest_1000[-1]["draw_id"] if latest_1000 else "None")
print("CSV saved:", OUTPUT_FILE)
