import json
import numpy as np

from regression import double_linear_regression
from lib_analisis import acceleration, acceleration_with_vd, basic_decelaration, best_fit, decelar, decelar_both, decelar_vm_fix, double_acceleration, get_events, get_middles


FILES_TO_USE = [i for i in range(1,15)]  # Use all files from 01 to 14
EVENTS = [i for i in range(1,9)]
folder_name = 'only_events_60_v2'
output_file = 'dec_60_both'  # 'pastos_with_taus'
idea = 'deceleration' # 'acceleration' or 'deceleration'
USE_WITHOUT_SMOOTH = False
FPS = 60
AMOUNT_ZEROES = 60
ECM_THRESHOLD = 0.024


def deceleartion_following_distance(vel_start, positions, best_time):
    
    start_index = int(best_time*FPS)
    distance = abs(positions[start_index+AMOUNT_ZEROES] - positions[-AMOUNT_ZEROES-1]) 
    tau = distance / vel_start
    
    return {'tau': tau, 'distance': distance, 'velocity_at_best_time': vel_start}

def deceleration(v, curr_end, middle, positions):
    # Ignore the padded zeros
    v_data_full = v[AMOUNT_ZEROES : -AMOUNT_ZEROES]
    time = np.arange(len(v_data_full)) / FPS   # reset time axis starting at 0
    
    # Run your double regression on the valid region
    best_time, best_first_m, best_second_m, best_first_b, best_second_b = double_linear_regression(v_data_full, time, middle, curr_end)

    start_index = int(best_time * FPS)

    # Final time and velocity (end of braking, before padding)
    #t_final = time[-1]
    v_target = v_data_full[-1] if v_data_full[-1] > 0 else 0.003

    # Slice out the deceleration interval
    v_data = v_data_full[start_index:]
    t_data = np.arange(len(v_data)) / FPS  # reset time axis starting at 0
    t_final = t_data[-1]

    # Fit exponential model (anchored at endpoint)
    popt, ecm = best_fit(t_data, v_data, model=decelar, model_args=[v_target, t_final])
    tau = popt[0]

    # Initial condition: velocity at start of braking (theoretical)
    t0 = t_data[0]
    vM = decelar(v_target, t_final)(t0, tau)

    # Otro método más pedorro
    dec_follow_distance = deceleartion_following_distance(v_data[0], positions, best_time)
    errors = []
    vel_fl_dist = dec_follow_distance['velocity_at_best_time']
    tau_fl_dist = dec_follow_distance['tau']
    for i, curr_t in enumerate(t_data):
        v_fit = basic_decelaration(vel_fl_dist, tau_fl_dist, curr_t)
        errors.append((v_fit - v_data[i]) ** 2)
        
    ecm_follow_distance = np.mean(errors)


    # Otro método ajustando ambos parámetros
    popt_vm_fix, ecm_vm_fix = best_fit(t_data, v_data, model=decelar_vm_fix, model_args=[v_data[0]])
    tau_vm_fix = popt_vm_fix[0]


    # Método Both
    popt_both, ecm_both = best_fit(t_data, v_data, model=decelar_both, model_args=[])
    tau_both = popt_both[0]
    vM_both = popt_both[1]

    return {
        'best_time': best_time,
        'best_first_m': best_first_m,
        'best_second_m': best_second_m,
        'best_first_b': best_first_b,
        'best_second_b': best_second_b,
        'tau': tau,
        'velocity_at_best_time': vM,
        'ecm': ecm,
        'tau_following_distance': dec_follow_distance['tau'],
        'distance_following_distance': dec_follow_distance['distance'],
        'velocity_at_best_time_following_distance': dec_follow_distance['velocity_at_best_time'],
        'ecm_following_distance': ecm_follow_distance,
        'tau_vm_fix': tau_vm_fix,
        'vm_vm_fix': v_data[0],
        'ecm_vm_fix': ecm_vm_fix,
        'tau_both': tau_both,
        'vm_both': vM_both,
        'ecm_both': ecm_both
    }
    
    
def parameters_for_acceleration(i, v, start, middles):
    curr_mid = middles[i]
    
    v_d = np.average(v[curr_mid-60:curr_mid + 1])
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
    doubles = {}
    middles = pastos[key]['middles']
    curr_deceleration_info = {}

    for i, event in enumerate(events):
        v = event['v']
        
        if idea == 'deceleration':
            if i+1 in EVENTS:
                positions = event['y'] if i == 2 or i == 5 else event['x']
                curr_deceleration_info[f'event_{i+1}'] = deceleration(v, len(v) - 2*AMOUNT_ZEROES - 1, middle=middles[i] - AMOUNT_ZEROES, positions=positions)

        elif idea == 'acceleration':
            t, v, func, func_args = parameters_for_acceleration(i, v, AMOUNT_ZEROES, middles)
            popt, ecm = best_fit(t, v, model=func, model_args=func_args)
            tau_fit = popt[0]
            #vd_fit = popt[1]
            # t y v ya fueron trimeados en parameters_for_acceleration
            if ecm > ECM_THRESHOLD:
                best_index, first_tau, second_tau, first_vd, second_vd, best_error = double_acceleration(t, v, 0, len(v)-1)
                doubles[f'event_{i+1}'] = {
                    'best_index': best_index,
                    'first_tau': first_tau,
                    'second_tau': second_tau,
                    'first_vd': first_vd,
                    'second_vd': second_vd,
                    'best_error': best_error
                }
                
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


if idea == 'acceleration':
    with open(f"analisis/{output_file}.json", "w") as f_out:
        json.dump({'pastos': pastos}, f_out, indent=4)
elif idea == 'deceleration':
    with open(f"analisis/{output_file}.json", "w") as f_out:
        json.dump({'deceleration_info': deceleration_info}, f_out, indent=4)   
 
