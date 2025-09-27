

import json

import numpy as np


FILES_TO_USE = [i for i in range(1, 15)]  # Use all files from 01 to 14
FILE = 'acc_60'  # 'pastos_with_taus'

keys = []
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)

with open(f"analisis/{FILE}.json", "r") as f:
    pastos_data = json.load(f)
    if 'pastos' in pastos_data:
        data = pastos_data['pastos']
    else:
        raise KeyError("Key 'pastos' not found in pastos.json")

all_taus = []
for key in keys:
    curr_taus = data[key]['taus']
    # El primero y el noveno son medio raros, sus primeros eventos son muy cortos. Ojo con el quinto pedestrian
    if key == '01' or key == '09':
        curr_taus = curr_taus[1:]
        
    mean, std = np.mean(curr_taus), np.std(curr_taus)
    data[key]['mean_tau'] = mean
    data[key]['std_tau'] = std
    all_taus += curr_taus

mean_all, std_all = np.mean(all_taus), np.std(all_taus)

data['all'] = {
    'mean_tau': mean_all,
    'std_tau': std_all
}

with open(f"analisis/{FILE}.json", "w") as f_out:
    json.dump({'pastos': data}, f_out, indent=4)

    