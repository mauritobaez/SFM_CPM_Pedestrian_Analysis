import json
import numpy as np

from lib_analisis import acceleration, best_fit, decelar, get_events, get_pastos


FILES_TO_USE = [i for i in range(1,15)]  # Use all files from 01 to 14
EVENTS = [1, 2, 3, 4, 5, 6, 7, 8]
folder_name = 'only_events'
output_file = 'nuevos_pastos'  # 'pastos_with_taus'
output_file_with_no_values = 'taus'
idea = 'acceleration' # 'acceleration' or 'deceleration'
FPS = 60
AMOUNT_ZEROES = 30

def deceleration(v, curr_end, middle):
    best_ecm = float('inf')
    best_tau = None
    best_v_d = None
    best_time_to_zero = None
    v_d = v[middle]

    for i in range(middle, curr_end):
        
        curr_velocities = v[i: curr_end+1]
        t = np.arange(len(curr_velocities)) / FPS
        
        tau_dec, ecm = best_fit(t, curr_velocities, decelar, [v_d])
        
        if ecm < best_ecm:
            best_ecm = ecm
            best_tau = tau_dec
            best_v_d = v_d
            best_time_to_zero = t[-1]
            
        v_d = v_d + (v[i+1] - v_d) / (i+1 - middle + 1)

    target_velocity = v[curr_end]
    time_according_to_equation = best_tau * np.log(best_v_d / target_velocity)
    info = {'ecm': best_ecm, 'tau_dec': best_tau, 'v_d': best_v_d, 'time_to_zero': best_time_to_zero, 'target_velocity': target_velocity, 'time_according_to_equation': time_according_to_equation, 'difference_in_time': abs(best_time_to_zero - time_according_to_equation)}
    
    return info
            

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
    events = get_events(folder_name, key)

    taus = []
    ecms = []
    middles = pastos[key]['middles']
    curr_deceleration_info = {}

    for i, event in enumerate(events):
        v = event['v']
        
        if idea == 'deceleration':
            if i+1 in EVENTS:
                curr_deceleration_info[f'event_{i+1}'] = deceleration(v, len(v) - AMOUNT_ZEROES, middle=middles[i])
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
    

    pastos[key].pop('middles', None)
    
with open(f"analisis/{output_file_with_no_values}.json", "w") as f_out:
    json.dump({'pedestrians': pastos}, f_out, indent=4)

#with open(f"analisis/{output_file}.json", "w") as f_out:
#    json.dump({'pastos': pastos}, f_out, indent=4)

#with open(f"analisis/{output_file}.json", "w") as f_out:
#    json.dump({'deceleration_info': deceleration_info}, f_out, indent=4)   
 
