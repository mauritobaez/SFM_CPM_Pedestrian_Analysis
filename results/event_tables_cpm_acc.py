
import json
import csv
from pathlib import Path

INPUT_BOTH = Path("analisis/acc_cpm_both.json")
INPUT = Path("analisis/acc_cpm.json")
OUT_CSV = Path(__file__).parent / "event_tables_cpm_acc.csv"
OUT_XLSX = Path(__file__).parent / "event_tables_cpm_acc.xlsx"
import pandas as pd

def fmt_val(x):
    if x == '-' or x is None:
        return '-'
    try:
        return f"{float(x):.4f}"
    except Exception:
        return str(x)

with open(INPUT_BOTH, 'r', encoding='utf-8') as f:
    data_both = json.load(f)
with open(INPUT, 'r', encoding='utf-8') as f:
    data = json.load(f)
    
pastos_both = data_both.get('pastos', {})
pastos = data.get('pastos', {})

rows = []
all_ecms_both = []
all_taus_both = []
all_betas_both = []
all_ecms = []
all_taus = []

for ped_id in sorted(pastos.keys()):
    ped = pastos[ped_id]
    ecms = ped.get('ecms', [])
    taus = ped.get('taus', [])
    ped_both = pastos_both.get(ped_id, {})
    ecms_both = ped_both.get('ecms', [])
    taus_both = ped_both.get('taus', [])
    betas_both = ped_both.get('betas', [])
    
    desfase = 0
    if ped_id == '01' or ped_id == '09':
        desfase = 1
    
    for event_id in range(0, 8):
        
        
        if (ped_id == '01' or ped_id == '09') and event_id == 0:
            continue
        
        curr_ecm = ecms[event_id - desfase]
        curr_tau = taus[event_id - desfase]
        curr_tau_both = taus_both[event_id - desfase]
        curr_ecm_both = ecms_both[event_id - desfase]
        curr_beta_both = betas_both[event_id - desfase]
        
        rows.append({
            'pedestrian': ped_id,
            'event': event_id + 1,
            'MSE': fmt_val(curr_ecm),
            'Tau': fmt_val(curr_tau),
            'MSE (fitted Beta)': fmt_val(curr_ecm_both),
            'Tau (fitted Beta)': fmt_val(curr_tau_both),
            'Beta (fitted Beta)': fmt_val(curr_beta_both),
        })
        
    rows.append({
        'pedestrian': ped_id,
        'event': 'Average',
        'MSE': fmt_val(sum(ecms) / len(ecms)),
        'Tau': fmt_val(sum(taus) / len(taus)),
        'MSE (fitted Beta)': fmt_val(sum(ecms_both) / len(ecms_both)),
        'Tau (fitted Beta)': fmt_val(sum(taus_both) / len(taus_both)),
        'Beta (fitted Beta)': fmt_val(sum(betas_both) / len(betas_both)),
    })
    
    all_ecms.extend(ecms)
    all_taus.extend(taus)
    all_ecms_both.extend(ecms_both)
    all_taus_both.extend(taus_both)
    all_betas_both.extend(betas_both)

rows.append({
    'pedestrian': 'Overall Average',
    'event': '',
    'MSE': fmt_val(sum(all_ecms) / len(all_ecms)),
    'Tau': fmt_val(sum(all_taus) / len(all_taus)),
    'MSE (fitted Beta)': fmt_val(sum(all_ecms_both) / len(all_ecms_both)),
    'Tau (fitted Beta)': fmt_val(sum(all_taus_both) / len(all_taus_both)),
    'Beta (fitted Beta)': fmt_val(sum(all_betas_both) / len(all_betas_both)),
})

fieldnames = ['pedestrian', 'event', 'MSE', 'Tau', 'MSE (fitted Beta)', 'Tau (fitted Beta)', 'Beta (fitted Beta)']
with open(OUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
        

df = pd.DataFrame(rows)
df.to_excel(OUT_XLSX, index=False)
    