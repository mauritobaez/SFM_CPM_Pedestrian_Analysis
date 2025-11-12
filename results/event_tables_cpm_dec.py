import json
import csv
from pathlib import Path
import pandas as pd

INPUT_BOTH = Path("analisis/dec_cpm_both.json")
INPUT = Path("analisis/dec_cpm_both_half.json")
OUT_CSV = Path(__file__).parent / "event_tables_cpm_dec.csv"
OUT_XLSX = Path(__file__).parent / "event_tables_cpm_dec.xlsx"


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


data_both = load(INPUT_BOTH)
data = load(INPUT)

dec_both = data_both.get('deceleration_info', {})
dec = data.get('deceleration_info', {})

rows = []
all_norm_ecms = []
all_both_ecms = []
all_norm_taus = []
all_both_taus = []
all_both_betas = []


for ped_id in sorted(dec.keys()):
    ped_base = dec.get(ped_id, {})
    ped_both = dec_both.get(ped_id, {})

    ped_norm_ecms = []
    ped_norm_taus = []
    
    ped_both_ecms = []
    ped_both_taus = []
    ped_both_betas = []

    for ev in range(1, 9):
        key = f'event_{ev}'
        base_entry = ped_base.get(key, {})
        both_entry = ped_both.get(key, {})

        ecm_norm = base_entry.get('ecm', '-')
        tau_norm = base_entry.get('tau', '-')

        ecm_both = both_entry.get('ecm', '-')
        tau_both = both_entry.get('tau', '-')
        beta_both = both_entry.get('beta', '-')

        rows.append({
            'pedestrian': ped_id,
            'event': ev,
            'ecm_normal': fmt_val(ecm_norm),
            'tau_normal': fmt_val(tau_norm),
            'ecm_both': fmt_val(ecm_both),
            'tau_both': fmt_val(tau_both),
            'beta_both': fmt_val(beta_both),
        })

        # accumulate numeric for averages
        
        ped_norm_ecms.append(float(ecm_norm))
        all_norm_ecms.append(float(ecm_norm))
        ped_norm_taus.append(float(tau_norm))
        all_norm_taus.append(float(tau_norm))
        
        ped_both_ecms.append(float(ecm_both))
        all_both_ecms.append(float(ecm_both))
        ped_both_taus.append(float(tau_both))
        all_both_taus.append(float(tau_both))
        ped_both_betas.append(float(beta_both))
        all_both_betas.append(float(beta_both))
        
    # add per-pedestrian averages (for the events we included)
    if ped_norm_ecms or ped_both_ecms:
        avg_norm = sum(ped_norm_ecms) / len(ped_norm_ecms) if ped_norm_ecms else '-'
        avg_both = sum(ped_both_ecms) / len(ped_both_ecms) if ped_both_ecms else '-'
        avg_tau_norm = sum(ped_norm_taus) / len(ped_norm_taus) if ped_norm_taus else '-'
        avg_tau_both = sum(ped_both_taus) / len(ped_both_taus) if ped_both_taus else '-'
        avg_beta_both = sum(ped_both_betas) / len(ped_both_betas) if ped_both_betas else '-'
        
        rows.append({
            'pedestrian': ped_id,
            'event': 'Average',
            'ecm_normal': fmt_val(avg_norm),
            'tau_normal': fmt_val(avg_tau_norm),
            'ecm_both': fmt_val(avg_both),
            'tau_both': fmt_val(avg_tau_both),
            'beta_both': fmt_val(avg_beta_both),
        })

# overall average
overall_norm = (sum(all_norm_ecms) / len(all_norm_ecms)) if all_norm_ecms else '-'
overall_both = (sum(all_both_ecms) / len(all_both_ecms)) if all_both_ecms else '-'
overall_both_taus = (sum(all_both_taus) / len(all_both_taus)) if all_both_taus else '-'
overall_both_betas = (sum(all_both_betas) / len(all_both_betas)) if all_both_betas else '-'
overall_norm_taus = (sum(all_norm_taus) / len(all_norm_taus)) if all_norm_taus else '-'

rows.append({
    'pedestrian': 'Overall Average',
    'event': '',
    'ecm_normal': fmt_val(overall_norm),
    'tau_normal': fmt_val(overall_norm_taus),
    'ecm_both': fmt_val(overall_both),
    'tau_both': fmt_val(overall_both_taus),
    'beta_both': fmt_val(overall_both_betas),
})

fieldnames = ['pedestrian', 'event', 'ecm_normal', 'tau_normal', 'ecm_both', 'tau_both', 'beta_both']
with open(OUT_CSV, 'w', newline='', encoding='utf-8') as csvf:
    writer = csv.DictWriter(csvf, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)


df = pd.DataFrame(rows)
df.to_excel(OUT_XLSX, index=False)
