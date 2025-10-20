import json
import numpy as np

from lib_analisis import best_fit, cpm_parameters_for_acceleration, cpm_parameters_for_acceleration_both, deceleration, deceleration_cpm, double_acceleration, get_events, get_middles, parameters_for_acceleration


FILES_TO_USE = [i for i in range(1,15)]  # Use all files from 01 to 14
EVENTS = [i for i in range(1,9)]
folder_name = 'only_events_60_v2'
output_file = 'dec_CPM_both'  # 'pastos_with_taus'
idea = 'deceleration' # 'acceleration' or 'deceleration'
USE_WITHOUT_SMOOTH = False
FPS = 60
AMOUNT_ZEROES = 60
i2t_min_threshold = 0.5
model = 'CPM'  # 'CPM' or 'SFM'



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
    i2ts = []
    doubles = {}
    betas = []
    middles = pastos[key]['middles']
    curr_deceleration_info = {}

    for i, event in enumerate(events):
        v = event['v']
        
        if idea == 'deceleration':
            if model == 'CPM':
                curr_deceleration_info[f'event_{i+1}'] = deceleration_cpm(v, len(v) - 2*AMOUNT_ZEROES - 1, middle=middles[i] - AMOUNT_ZEROES)
            else:
                positions = event['y'] if i == 2 or i == 5 else event['x']
                curr_deceleration_info[f'event_{i+1}'] = deceleration(v, len(v) - 2*AMOUNT_ZEROES - 1, middle=middles[i] - AMOUNT_ZEROES, positions=positions)

        elif idea == 'acceleration':
            if (key == '09' or key == '01') and i+1 == 1:
                continue
            
            if model == 'CPM':
                t, v, func, func_args = cpm_parameters_for_acceleration_both(i, v, AMOUNT_ZEROES, middles)
                popt, ecm = best_fit(t, v, model=func, model_args=func_args)
                tau_fit = popt[0]
                
                taus.append(tau_fit)
                ecms.append(ecm)
                vds.append(func_args[0])
                betas.append(popt[1])
                
            else:
                t, v, func, func_args = parameters_for_acceleration(i, v, AMOUNT_ZEROES, middles)
                popt, ecm = best_fit(t, v, model=func, model_args=func_args)
                tau_fit = popt[0]
                
                # t y v ya fueron trimeados en parameters_for_acceleration
                #if ecm > ECM_THRESHOLD:
                best_index, first_tau, second_tau, first_vd, second_vd, best_error = double_acceleration(t, v, 0, len(v)-1, last_vd=func_args[0])
                curr_i2t = (ecm - best_error) / ecm
                if curr_i2t > i2t_min_threshold:
                    doubles[f'event_{i+1}'] = {
                        'best_index': best_index,
                        'first_tau': first_tau,
                        'second_tau': second_tau,
                        'first_vd': first_vd,
                        'second_vd': second_vd,
                        'best_error': best_error
                    }
                    
                i2ts.append(curr_i2t)
                taus.append(tau_fit)
                ecms.append(ecm)
                vds.append(func_args[0])
        
        
        
    
    if idea == 'deceleration':
        deceleration_info[key] = curr_deceleration_info
    elif idea == 'acceleration':
        pastos[key]['taus'] = taus
        pastos[key]['ecms'] = ecms
        pastos[key]['vds'] = vds
        pastos[key]['doubles'] = doubles
        pastos[key]['i2ts'] = i2ts
        if model == 'CPM':
            pastos[key]['betas'] = betas


if idea == 'acceleration':
    with open(f"analisis/{output_file}.json", "w") as f_out:
        json.dump({'pastos': pastos}, f_out, indent=4)
elif idea == 'deceleration':
    with open(f"analisis/{output_file}.json", "w") as f_out:
        json.dump({'deceleration_info': deceleration_info}, f_out, indent=4)
        

 
