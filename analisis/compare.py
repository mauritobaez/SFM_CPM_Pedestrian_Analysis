import json
import numpy as np
import plotly.graph_objects as go

from lib_analisis import acceleration, best_fit, decelar, get_events, get_pastos


FILES_TO_USE = [i for i in range(1,15)]  # Use all files from 01 to 14
EVENTS = [1, 2, 3, 4, 5, 6, 7, 8]
folder_name = 'trans_events_by_ped'
output_file = 'events_dec_info'  # 'pastos_with_taus'
output_file_with_no_values = 'taus'
idea = 'deceleration' # 'acceleration' or 'deceleration'
FPS = 60

# En lugar de esto, agarrar los distintos V, y calcular el mejor tau
def deceleration(v, curr_end):
    best_ecm = float('inf')
    best_tau = None
    best_v_d = None
    info = {}
    for tau in np.arange(0.4, 1.1, 0.05):
        curr_info = {}
        for v_d in np.arange(0.1, 2.1, 0.1):
            comparison = []
            curr_velocities = v[curr_end-int(tau*v_d*60): curr_end+1]
            t = np.arange(len(curr_velocities)) / FPS
            dec_func = decelar(v_d, tau)
            for j, curr_t in enumerate(t):
                v_fit = dec_func(curr_t)
                comparison.append((curr_velocities[j]-v_fit)**2)

            ecm = np.mean(comparison)
            if ecm < best_ecm:
                best_ecm = ecm
                best_tau = tau
                best_v_d = v_d
            curr_info[f'{v_d:.2f}'] = {'ecm': ecm, 'tau': tau, 'v_d': v_d}
        info[f'{tau:.2f}'] = curr_info
    info['best'] = {'ecm': best_ecm, 'tau': best_tau, 'v_d': best_v_d}
    return info

def decelerationv2(v, curr_end, min_index, middle):
    best_ecm = float('inf')
    best_tau = None
    best_v_d = None
    best_time_to_zero = None
    #info = {}
    MIN_TIME = 3 # segundos antes de llegar al final
    MAX_TIME = 1
    for i in range(0, int(min_index - 60*MAX_TIME)):
        curr_velocities = v[middle + i: curr_end+1]
        v_d = curr_velocities[0]
        t = np.arange(len(curr_velocities)) / FPS
        
        comparison = []
        curr_info = {}
        time_to_zero = t[-1]
        tau = time_to_zero / v_d
        dec_func = decelar(v_d, tau)
        
        for j, curr_t in enumerate(t):
            v_fit = dec_func(curr_t)
            comparison.append((curr_velocities[j]-v_fit)**2)
        
        ecm = np.mean(comparison)
        if ecm < best_ecm:
            best_ecm = ecm
            best_tau = tau
            best_v_d = v_d
            best_time_to_zero = time_to_zero
       # curr_info[f'v_d={v_d:.2f}'] = {'ecm': ecm, 'tau': tau, 'v_d': v_d, 'time_to_zero': time_to_zero}
       # info[f'tau={tau:.2f}'] = curr_info
    info = {'ecm': best_ecm, 'tau_dec': best_tau, 'v_d': best_v_d, 'time_to_zero': best_time_to_zero}
    
    return info
            

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
deceleration_info = {}

for key in keys:
    events = get_events(folder_name, key)

    curr_pastos = pastos[key]['values']
    start = 0 # pastos[key]['start']
    curr_end = curr_pastos[0] - start
    taus = []
    ecms = []
    middles = pastos[key]['middles']
    curr_deceleration_info = {}

    for i, event in enumerate(events):
        v = event['v']
        
        if idea == 'deceleration':
            if i+1 in EVENTS:
                min_index = curr_end - middles[i]
                curr_deceleration_info[f'event_{i+1}'] = decelerationv2(v, curr_end, min_index, middle=middles[i])
            curr_end = curr_pastos[2*(i+1)] - curr_pastos[2*i] if i != len(events) - 1 else 0   # If last event, no need to set curr_end
        elif idea == 'acceleration':
            t, v, func, func_args = parameters_for_accleration(i, v, middles)
            tau_fit, ecm = best_fit(t, v, model=func, model_args=func_args)
            ecms.append(ecm)
            taus.append(tau_fit)
        
        if i != len(events) - 1:
            start = curr_pastos[2*i + 1] - curr_pastos[2*i]
    
    if idea == 'deceleration':
        deceleration_info[key] = curr_deceleration_info
    elif idea == 'acceleration':
        pastos[key]['taus'] = taus
        pastos[key]['ecms'] = ecms
    

#    pastos[key].pop('start', None)
#    pastos[key].pop('values', None)
#    pastos[key].pop('middles', None)
#    
#with open("analisis/{output_file_with_no_values}.json", "w") as f_out:
#    json.dump({'pedestrians': pastos}, f_out, indent=4)

#with open(f"analisis/{output_file}.json", "w") as f_out:
#    json.dump({'pastos': pastos}, f_out, indent=4)

with open(f"analisis/{output_file}.json", "w") as f_out:
    json.dump({'deceleration_info': deceleration_info}, f_out, indent=4)   
 
