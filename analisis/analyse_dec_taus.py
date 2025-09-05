

import json
import numpy as np

with open('analisis/events_dec_info.json', 'r') as f:
    data = json.load(f)
deceleration_info = data['deceleration_info']


for ped_id, ped_data in deceleration_info.items():
    ecms = []
    taus = []
    v_ds = []
    time_to_zeros = []

    
    for event_key, event_data in ped_data.items():
        if event_key == 'avgs':
            continue
        ecms.append(event_data['ecm'])
        taus.append(event_data['tau_dec'])
        v_ds.append(event_data['v_d'])
        time_to_zeros.append(event_data['time_to_zero'])
    
    avg_ecm = sum(ecms) / len(ecms) if ecms else None
    avg_tau = np.mean(taus) if taus else None
    std_tau = np.std(taus) if taus else None
    avg_v_d = sum(v_ds) / len(v_ds) if v_ds else None
    avg_time_to_zero = sum(time_to_zeros) / len(time_to_zeros)

    
    ped_data['avgs'] = {
        'avg_ecm': avg_ecm,
        'avg_tau_dec': avg_tau,
        'std_tau_dec': std_tau,
        'avg_v_d': avg_v_d,
        'avg_time_to_zero': avg_time_to_zero
    }


with open('analisis/events_dec_info.json', 'w') as f:
    json.dump(data, f, indent=4)

