import json
import numpy as np

from regression import double_linear_regression
from lib_analisis import acceleration, best_fit, decelar, get_events, get_middles


FILES_TO_USE = [i for i in range(1,15)]  # Use all files from 01 to 14
EVENTS = [i for i in range(1,9)]
folder_name = 'only_events_60_fix'
output_file = 'dec_60'  # 'pastos_with_taus'
idea = 'deceleration' # 'acceleration' or 'deceleration'
USE_WITHOUT_SMOOTH = False
FPS = 60
AMOUNT_ZEROES = 60

def deceleration(v, curr_end, middle):
    time = np.arange(len(v))/FPS
    best_time, best_first_m, best_second_m, best_first_b, best_second_b = double_linear_regression(v, time, middle, curr_end)

    start_index = int(best_time*FPS)

    t_final = time[-AMOUNT_ZEROES*2-1]   # Revisar esto
    v_target = v[-AMOUNT_ZEROES-1]
    
    t_data = np.arange(start_index, curr_end) / FPS
    v_data = v[start_index:curr_end]
    
    popt, ecm = best_fit(t_data, v_data, model=decelar, model_args=[v_target, t_final])
    tau = popt[0]
    
    vM = decelar(v_target, t_final)(0,tau)  # Estoy consiguiendo la velocidad que queda justo cuando empieza la aceleración
    
    return {'best_time': best_time, 'best_first_m': best_first_m, 'best_second_m': best_second_m, 'best_first_b': best_first_b, 'best_second_b': best_second_b, 'tau': tau, 'velocity_at_best_time': vM, 'ecm': ecm}            

def parameters_for_acceleration(i, v, start, middles):
    curr_mid = middles[i]
        
    v = v[start:curr_mid+1]
    t = np.arange(len(v)) / FPS
    return t, v, acceleration, []   

keys = []
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)

pastos = get_middles()
deceleration_info = {}

for key in keys:
    events = get_events(folder_name, key, USE_WITHOUT_SMOOTH) # True to use the velocity with nothing applied

    taus = []
    ecms = []
    vds = []
    middles = pastos[key]['middles']
    curr_deceleration_info = {}

    for i, event in enumerate(events):
        v = event['v']
        
        if idea == 'deceleration':
            if i+1 in EVENTS:
                curr_deceleration_info[f'event_{i+1}'] = deceleration(v, len(v) - AMOUNT_ZEROES, middle=middles[i])
        elif idea == 'acceleration':
            t, v, func, func_args = parameters_for_acceleration(i, v, AMOUNT_ZEROES, middles)
            popt, ecm = best_fit(t, v, model=func, model_args=func_args)
            tau_fit = popt[0]
            vd_fit = popt[1]
            taus.append(tau_fit)
            ecms.append(ecm)
            vds.append(vd_fit)
        
        
        
    
    if idea == 'deceleration':
        deceleration_info[key] = curr_deceleration_info
    elif idea == 'acceleration':
        pastos[key]['taus'] = taus
        pastos[key]['ecms'] = ecms
        pastos[key]['vds'] = vds
    


if idea == 'acceleration':
    with open(f"analisis/{output_file}.json", "w") as f_out:
        json.dump({'pastos': pastos}, f_out, indent=4)
elif idea == 'deceleration':
    with open(f"analisis/{output_file}.json", "w") as f_out:
        json.dump({'deceleration_info': deceleration_info}, f_out, indent=4)   
 
