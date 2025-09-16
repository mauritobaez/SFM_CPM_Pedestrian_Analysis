import json
import numpy as np

from regression import double_linear_regression
from lib_analisis import acceleration, best_fit, decelar, get_events, get_pastos


FILES_TO_USE = [i for i in range(1,15)]  # Use all files from 01 to 14
EVENTS = [i for i in range(1,9)]
folder_name = 'only_events'
output_file = 'dec'  # 'pastos_with_taus'
output_file_with_no_values = 'taus_dec'
idea = 'deceleration' # 'acceleration' or 'deceleration'
USE_WITHOUT_SMOOTH = False
FPS = 60
AMOUNT_ZEROES = 30

def deceleration(v, curr_end, middle, positions=[]):
    
    best_time, best_first_m, best_second_m, best_first_b, best_second_b = double_linear_regression(v, np.arange(len(v))/FPS, middle, curr_end)

    start_index = int(best_time*FPS)
    distance = abs(positions[start_index] - positions[-AMOUNT_ZEROES-1]) 
    tau = distance / v[start_index]
    
    return {'best_time': best_time, 'best_first_m': best_first_m, 'best_second_m': best_second_m, 'best_first_b': best_first_b, 'best_second_b': best_second_b, 'tau': tau, 'distance': distance, 'velocity_at_best_time': v[start_index]}            

def parameters_for_acceleration(i, v, start, middles):
    curr_mid = middles[i]
    mid_vel = v[curr_mid]
        
    v = v[start:curr_mid+1]
    t = np.arange(len(v)) / FPS
    return t, v, acceleration, [mid_vel]   

keys = []
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)

pastos = get_pastos()
deceleration_info = {}

for key in keys:
    events = get_events(folder_name, key, USE_WITHOUT_SMOOTH) # True to use the velocity with nothing applied

    taus = []
    ecms = []
    middles = pastos[key]['middles']
    curr_deceleration_info = {}

    for i, event in enumerate(events):
        v = event['v']
        positions = event['y'] if i == 2 or i == 5 else event['x']
        
        if idea == 'deceleration':
            if i+1 in EVENTS:
                curr_deceleration_info[f'event_{i+1}'] = deceleration(v, len(v) - AMOUNT_ZEROES, middle=middles[i], positions=positions)
        elif idea == 'acceleration':
            t, v, func, func_args = parameters_for_acceleration(i, v, AMOUNT_ZEROES, middles)
            tau_fit, ecm = best_fit(t, v, model=func, model_args=func_args)
            ecms.append(ecm)
            taus.append(tau_fit)
        
    
    if idea == 'deceleration':
        deceleration_info[key] = curr_deceleration_info
    elif idea == 'acceleration':
        pastos[key]['taus'] = taus
        pastos[key]['ecms'] = ecms
    

    #pastos[key].pop('middles', None)
    
#with open(f"analisis/{output_file_with_no_values}.json", "w") as f_out:
#    json.dump({'pedestrians': pastos}, f_out, indent=4)

if idea == 'acceleration':
    with open(f"analisis/{output_file}.json", "w") as f_out:
        json.dump({'pastos': pastos}, f_out, indent=4)
elif idea == 'deceleration':
    with open(f"analisis/{output_file}.json", "w") as f_out:
        json.dump({'deceleration_info': deceleration_info}, f_out, indent=4)   
 
