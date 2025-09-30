import json
import numpy as np

from regression import double_linear_regression
from lib_analisis import acceleration, acceleration_with_vd, best_fit, decelar, get_events, get_middles


FILES_TO_USE = [i for i in range(1,15)]  # Use all files from 01 to 14
EVENTS = [i for i in range(1,9)]
folder_name = 'only_events_60_v2'
output_file = 'acc_60'  # 'pastos_with_taus'
idea = 'acceleration' # 'acceleration' or 'deceleration'
USE_WITHOUT_SMOOTH = False
FPS = 60
AMOUNT_ZEROES = 60

def deceleration(v, curr_end, middle):
    # Ignore the padded zeros
    v_data_full = v[AMOUNT_ZEROES : -AMOUNT_ZEROES]
    time = np.arange(len(v_data_full)) / FPS   # reset time axis starting at 0
    
    # Run your double regression on the valid region
    best_time, best_first_m, best_second_m, best_first_b, best_second_b = double_linear_regression(v_data_full, time, middle, curr_end)

    start_index = int(best_time * FPS)

    # Final time and velocity (end of braking, before padding)
    t_final = time[-1]
    v_target = v_data_full[-1] if v_data_full[-1] > 0 else 0.003

    # Slice out the deceleration interval
    t_data = time[start_index:]
    v_data = v_data_full[start_index:]

    # Fit exponential model (anchored at endpoint)
    popt, ecm = best_fit(t_data, v_data, model=decelar, model_args=[v_target, t_final])
    tau = popt[0]

    # Initial condition: velocity at start of braking (theoretical)
    t0 = time[start_index]
    vM = decelar(v_target, t_final)(t0, tau)

    return {
        'best_time': best_time,
        'best_first_m': best_first_m,
        'best_second_m': best_second_m,
        'best_first_b': best_first_b,
        'best_second_b': best_second_b,
        'tau': tau,
        'velocity_at_best_time': vM,
        'ecm': ecm
    }
    
    
def parameters_for_acceleration(i, v, start, middles):
    curr_mid = middles[i]
    
    v_d = np.average(v[curr_mid-30:curr_mid+30 + 1])
    v = v[start:curr_mid + 1]
    t = np.arange(len(v)) / FPS
    return t, v, acceleration_with_vd, [v_d]   

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
                curr_deceleration_info[f'event_{i+1}'] = deceleration(v, len(v) - 2*AMOUNT_ZEROES - 1, middle=middles[i] - AMOUNT_ZEROES)

        elif idea == 'acceleration':
            t, v, func, func_args = parameters_for_acceleration(i, v, AMOUNT_ZEROES, middles)
            popt, ecm = best_fit(t, v, model=func, model_args=func_args)
            tau_fit = popt[0]
            #vd_fit = popt[1]
            taus.append(tau_fit)
            ecms.append(ecm)
            vds.append(func_args[0])
        
        
        
    
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
 
