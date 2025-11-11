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
all_ecms = []
all_i2ts = []
all_taus = []
all_double_ecms = []
all_first_taus = []
all_second_taus = []
# iterate sorted so order is 01,02,...
for ped_id in sorted(pastos.keys()):
    ped = pastos[ped_id]
    ecms = ped.get('ecms', [])
    doubles = ped.get('doubles', {})
    i2ts = ped.get('i2ts', [])
    taus = ped.get('taus', [])
    desfase = 0
    if ped_id == '01' or ped_id == '09':
        desfase = 1

    ped_double_ecm = []
    ped_first_tau = []
    ped_second_tau = []

    for event_id in range(0, 8):
        
        
        if (ped_id == '01' or ped_id == '09') and event_id == 0:
            continue
        
        curr_ecm = ecms[event_id - desfase]
        curr_i2t = i2ts[event_id - desfase]
        curr_double_ecm = '-'
        curr_only_tau = taus[event_id - desfase]
        curr_first_tau = '-'
        curr_second_tau = '-'
        if f'event_{event_id + 1}' in doubles:
            curr_double_ecm = doubles[f'event_{event_id + 1}']['best_error']
            curr_first_tau = doubles[f'event_{event_id + 1}']['first_tau']
            curr_second_tau = doubles[f'event_{event_id + 1}']['second_tau']
            ped_double_ecm.append(curr_double_ecm)
            ped_first_tau.append(curr_first_tau)
            ped_second_tau.append(curr_second_tau)


        rows.append({
            'pedestrian': ped_id,
            'event': event_id + 1,
            'MSE (single)': fmt_val(curr_ecm),
            'MSE (double)': fmt_val(curr_double_ecm),
            'i2t': fmt_val(curr_i2t),
            'Tau (single)': fmt_val(curr_only_tau),
            '1st Tau (double)': fmt_val(curr_first_tau),
            '2nd Tau (double)': fmt_val(curr_second_tau),
        })
        
    rows.append({
        'pedestrian': ped_id,
        'event': 'Average',
        'MSE (single)': fmt_val(sum(ecms) / len(ecms)),
    #    'Std Dev (single)': fmt_val(pd.Series(ecms).std()),
        'MSE (double)': fmt_val(sum(ped_double_ecm) / len(ped_double_ecm)) if ped_double_ecm else '-',
     #   'Std Dev (double)': fmt_val(pd.Series(ped_double_ecm).std()) if ped_double_ecm else '-',
        'i2t': fmt_val(sum(i2ts) / len(i2ts)),
        'Tau (single)': fmt_val(sum(taus) / len(taus)),
      #  'Std Dev (single Tau)': fmt_val(pd.Series(taus).std()),
        '1st Tau (double)': fmt_val(sum(ped_first_tau) / len(ped_first_tau)) if ped_first_tau else '-',
        '2nd Tau (double)': fmt_val(sum(ped_second_tau) / len(ped_second_tau)) if ped_second_tau else '-',
       # 'Std Dev (1st Tau)': fmt_val(pd.Series(ped_first_tau).std()) if ped_first_tau else '-',
        #'Std Dev (2nd Tau)': fmt_val(pd.Series(ped_second_tau).std()) if ped_second_tau else '-'
    })
    
    all_ecms.extend(ecms)
    all_i2ts.extend(i2ts)
    all_taus.extend(taus)
    all_double_ecms.extend(ped_double_ecm)
    all_first_taus.extend(ped_first_tau)
    all_second_taus.extend(ped_second_tau)
    
rows.append({
    'pedestrian': 'Overall Average',
    'event': '-',
    'MSE (single)': fmt_val(sum(all_ecms) / len(all_ecms)),
    'MSE (double)': fmt_val(sum(all_double_ecms) / len(all_double_ecms)) if all_double_ecms else '-',
    'i2t': fmt_val(sum(all_i2ts) / len(all_i2ts)),
    'Tau (single)': fmt_val(sum(all_taus) / len(all_taus)),
    '1st Tau (double)': fmt_val(sum(all_first_taus) / len(all_first_taus)) if all_first_taus else '-',
    '2nd Tau (double)': fmt_val(sum(all_second_taus) / len(all_second_taus)) if all_second_taus else '-',
})

# Write CSV
fieldnames = ['pedestrian', 'event', 'MSE (single)', 'MSE (double)', 'i2t', 'Tau (single)', '1st Tau (double)', '2nd Tau (double)']
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


