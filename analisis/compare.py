import json
import numpy as np
import plotly.graph_objects as go

from lib_analisis import acceleration, best_fit, deceleration, get_events, get_pastos


FILES_TO_USE = [i for i in range(1, 15)]  # Use all files from 01 to 14
folder_name = 'trans_events_by_ped'
output_file = 'pastos_with_taus'
output_file_with_no_values = 'taus'
FPS = 60

def parameters_for_decceleration(i, v, curr_pastos):
    # Hacer lo de tau segundos
    if i != 0:
        curr_end = curr_pastos[2*i] - curr_pastos[2*i - 2]
    v = v[curr_mid: curr_end+1]
    t = np.arange(len(v)) / FPS
    return v, t, acceleration, [mid_vel] 

def parameters_for_accleration(i, v, middles):
    curr_mid = middles[i]
    mid_vel = v[curr_mid]
        
    v = v[start:curr_mid+1]
    #v = v[curr_mid: curr_end+1]
    t = np.arange(len(v)) / FPS
    return v, t, acceleration, [mid_vel]   

keys = []
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)

pastos = get_pastos()

for key in keys:
    events = get_events(folder_name, key)

    curr_pastos = pastos[key]['values']
    start = 0 # pastos[key]['start']
    #curr_end = curr_pastos[0] - start
    taus = []
    ecms = []
    middles = pastos[key]['middles']

    for i, event in enumerate(events):
        v = event['v']
        
        t, v, func, func_args = parameters_for_accleration(i, v, middles)
        tau_fit, ecm = best_fit(t, v, model=func, model_args=func_args)
        ecms.append(ecm)
        taus.append(tau_fit)
        
        if i != len(events) - 1:
            start = curr_pastos[2*i + 1] - curr_pastos[2*i]
    
    pastos[key]['taus'] = taus
    pastos[key]['ecms'] = ecms
    

#    pastos[key].pop('start', None)
#    pastos[key].pop('values', None)
#    pastos[key].pop('middles', None)
#    
#with open("analisis/{output_file_with_no_values}.json", "w") as f_out:
#    json.dump({'pedestrians': pastos}, f_out, indent=4)

with open(f"analisis/{output_file}.json", "w") as f_out:
    json.dump({'pastos': pastos}, f_out, indent=4)
    
 
