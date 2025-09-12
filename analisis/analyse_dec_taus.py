

import json
import numpy as np

with open('analisis/dec.json', 'r') as f:
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
        taus.append(event_data['tau'])
    
    
    avg_tau = np.mean(taus) if taus else None
    std_tau = np.std(taus) if taus else None

    
    ped_data['avgs'] = {
        'avg_tau_dec': avg_tau,
        'std_tau_dec': std_tau
    }


with open('analisis/dec.json', 'w') as f:
    json.dump(data, f, indent=4)

