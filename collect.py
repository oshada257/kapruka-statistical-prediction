
import requests
from pathlib import Path

URL = (
    "https://raw.githubusercontent.com/"
    "Ishanoshada/Live-Scrape-Lottery-SL/"
    "refs/heads/main/dlb_txt/kapruka.txt"
)

output = Path("data/kapruka_raw.txt")
output.parent.mkdir(exist_ok=True)

print("Downloading Kapruka historical results...")

response = requests.get(URL, timeout=30)
response.raise_for_status()

output.write_bytes(response.content)

print("\nDownload successful!")
print("File size:", len(response.content), "bytes")
print("\nFirst 15 lines:\n")

with output.open("r", encoding="utf-8-sig") as file:
    for i, line in enumerate(file):
        if i == 15:
            break
        print(line.rstrip())
