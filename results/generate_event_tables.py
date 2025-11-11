import json
import csv
from pathlib import Path

INPUT = Path("analisis/acc_60_I2T.json")
OUT_CSV = Path(__file__).parent / "event_tables.csv"
OUT_XLSX = Path(__file__).parent / "event_tables.xlsx"
import pandas as pd

def fmt_val(x):
    if x == '-' or x is None:
        return '-'
    try:
        return f"{float(x):.4f}"
    except Exception:
        return str(x)


with open(INPUT, 'r', encoding='utf-8') as f:
    data = json.load(f)

pastos = data.get('pastos', {})

# Build rows for CSV/Excel
rows = []
# iterate sorted so order is 01,02,...
for ped_id in sorted(pastos.keys()):
    ped = pastos[ped_id]
    ecms = ped.get('ecms', [])
    doubles = ped.get('doubles', {})
    i2ts = ped.get('i2ts', [])
    desfase = 0
    if ped_id == '01' or ped_id == '09':
        desfase = 1

    for event_id in range(0, 8):
        
        
        if (ped_id == '01' or ped_id == '09') and event_id == 0:
            continue
        
        curr_ecm = ecms[event_id - desfase]
        curr_i2t = i2ts[event_id - desfase]
        curr_double_ecm = '-'
        if f'event_{event_id + 1}' in doubles:
            curr_double_val = doubles[f'event_{event_id + 1}']['best_error']
         

        rows.append({
            'pedestrian': ped_id,
            'event': event_id + 1,
            'ecm_normal': fmt_val(curr_ecm),
            'ecm_double': fmt_val(curr_double_ecm),
            'i2t': fmt_val(curr_i2t),
        })

# Write CSV
fieldnames = ['pedestrian', 'event', 'ecm_normal', 'ecm_double', 'i2t']
with open(OUT_CSV, 'w', encoding='utf-8', newline='') as csvf:
    writer = csv.DictWriter(csvf, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

print(f"Wrote CSV: {OUT_CSV.resolve()}")

# Try to write Excel using pandas if available
try:

    df = pd.DataFrame(rows)
    # convert event column to int if possible
    try:
        df['event'] = df['event'].astype(int)
    except Exception:
        pass
    df.to_excel(OUT_XLSX, index=False)
    print(f"Wrote Excel: {OUT_XLSX.resolve()}")
except Exception as e:
    print("pandas not available; skipped Excel output.")
    print("To enable Excel output: pip install pandas openpyxl")


