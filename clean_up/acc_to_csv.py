import json
import csv


# Paths
input_json = 'analisis/acc_60_04.json'
output_all = 'Acel_1_Tau_All.csv'
output_good_1tau = 'Acel_1_Tau_Good.csv'
output_good_2tau = 'Acel_2_Tau.csv'

# Load data
with open(input_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Prepare rows
rows_all = []
rows_good_1tau = []
rows_good_2tau = []

for ped_id, ped_data in data.get('pastos', {}).items():
    taus = ped_data.get('taus', [])
    ecms = ped_data.get('ecms', [])
    doubles = ped_data.get('doubles', {})

    # All 1 Tau (each event)
    for i, (tau, ecm) in enumerate(zip(taus, ecms), start=1 if ped_id != '09' and ped_id != '01' else 2):
        event_id = f"{ped_id}{i:02}"
        rows_all.append([event_id, tau, ecm])
        if f'event_{i}' not in doubles:
            rows_good_1tau.append([event_id, tau, ecm])

    # Good 2 Tau (from doubles)
    for event_name, double_data in doubles.items():
        tau_1 = double_data.get('first_tau', '')
        tau_2 = double_data.get('second_tau', '')
        ecm = double_data.get('best_error', '')
        event_id = f"{ped_id}0{event_name.split('_')[1]}"
        rows_good_2tau.append([event_id, tau_1, tau_2, ecm])

# Write CSVs
header = ['id', 'Tau', 'ECM']

with open(output_all, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows_all)

with open(output_good_1tau, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows_good_1tau)

header = ['id', 'Tau_1', 'Tau_2', 'ECM']

with open(output_good_2tau, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows_good_2tau)

