import json
import csv
from pathlib import Path

INPUT = Path("analisis/dec_60.json")
OUT_CSV = Path(__file__).parent / "event_tables_sfm_dec.csv"
OUT_XLSX = Path(__file__).parent / "event_tables_sfm_dec.xlsx"


def fmt_val(x):
    if x == '-' or x is None:
        return '-'
    try:
        return f"{float(x):.6f}"
    except Exception:
        return str(x)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


data = load(INPUT)
dec_info = data.get('deceleration_info', {})

rows = []

# Scan all events to find all possible ECM keys
all_ecm_keys = set()
for ped_id, ped_data in dec_info.items():
    for event_key, event_data in ped_data.items():
        if event_key != 'avgs':  # skip averages entry
            for k in event_data.keys():
                if 'ecm' in k.lower():
                    all_ecm_keys.add(k)

# Sort for consistent column ordering
all_ecm_keys = sorted(all_ecm_keys)

# Build rows for each pedestrian/event
for ped_id in sorted(dec_info.keys()):
    ped_data = dec_info[ped_id]
    
    for ev_num in range(1, 9):
        event_key = f'event_{ev_num}'
        event_data = ped_data.get(event_key, {})
        
        row = {
            'pedestrian': ped_id,
            'event': ev_num,
        }
        
        # Add all ECM columns
        for ecm_key in all_ecm_keys:
            val = event_data.get(ecm_key, '-')
            row[ecm_key] = fmt_val(val)
        
        rows.append(row)

# Write CSV
fieldnames = ['pedestrian', 'event'] + list(all_ecm_keys)
with open(OUT_CSV, 'w', newline='', encoding='utf-8') as csvf:
    writer = csv.DictWriter(csvf, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

print(f"Wrote CSV: {OUT_CSV.resolve()}")

try:
    import pandas as pd
    df = pd.DataFrame(rows)
    df.to_excel(OUT_XLSX, index=False)
    print(f"Wrote Excel: {OUT_XLSX.resolve()}")
except Exception:
    print("pandas not available; skipped Excel output. To enable: pip install pandas openpyxl")
