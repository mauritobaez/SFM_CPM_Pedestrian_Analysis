

import json
import numpy as np
from scipy.optimize import curve_fit

from regression import double_linear_regression
FPS = 60
AMOUNT_ZEROES = 60
i2t_min_threshold = 0.5


def cpm_acceleration_with_beta(v_d, beta):
    #curr_r = prev_r + delta_r
    #curr_r = r_min + delta_r*(t/delta_t)
    #curr_r = r_min + ((r_max/tau) * delta_t) * (t/delta_t)
    #curr_r = r_min + (r_max/tau) * t
    #curr_r = r_min + ((r_max - r_min)/tau) * t
    def cpm_acc1(t, tau):
        return v_d * (t/tau)^beta if t < tau else v_d
    return cpm_acc1

def cpm_acceleration(v_d):
    def cpm_acc2(t, tau, beta):
        return v_d * (t/tau)^beta if t < tau else v_d
    return cpm_acc2

def cpm_deceleration(v_d):
    def cpm_decel(t, tau, beta):
        return v_d * (1 - (t/tau)^beta) if t < tau else 0
    return cpm_decel

def cpm_deceleration_with_beta(v_d, beta):
    def cpm_decel2(t, tau):
        return v_d * (1 - (t/tau)^beta) if t < tau else 0
    return cpm_decel2


def acceleration():
    def acc(t, tau, v_d):
        return v_d * (1 - np.exp(-t / tau))
    return acc

def acceleration_with_vd(v_d):
    def acc2(t, tau):
        return v_d * (1 - np.exp(-t / tau))
    return acc2

def acceleration_with_start_v(v_d, v_start):
    def acc3(t, tau):
        return v_start + (v_d - v_start) * (1 - np.exp(-t / tau))
    return acc3

def decelar(v_target, t1):
    def decel(t, tau):
        return v_target * np.exp((t1-t) / tau)
    return decel

def basic_decelaration(vM, tau, t):
    return vM * np.exp(-t / tau)

def decelar_vm_fix(vM):
    def decel_vm_fix(t, tau):
        return vM * np.exp(-t / tau)
    return decel_vm_fix

def decelar_both():
    def decel_both(t, tau, vM):
        return vM * np.exp(-t / tau)
    return decel_both

def get_middles():
    with open(f"analisis/middles.json", "r") as f:
        pastos_data = json.load(f)
        if 'pastos' in pastos_data:
            pastos = pastos_data['pastos']
        else:
            raise KeyError("Key 'pastos' not found in pastos.json")
    return pastos


def get_events(folder_name: str, key: str, basic: bool = False):
    events = []
    if basic:
        index_for_v = 4
    else:
        index_for_v = 3
    for event_number in range(1, 9):
        t = []
        x = []
        y = []
        v = []
        with open(f"archivosGerman/{folder_name}/ped_{key}_event_{event_number}.txt", "r") as values:
            lines = values.readlines()
        for i, line in enumerate(lines):
            line_values = line.split(sep='\t')
            multiply = 1.0
            if event_number in [3, 4, 5, 6]:
                multiply = -1.0
            t.append(float(line_values[0]))
            x.append(float(line_values[1]))
            y.append(float(line_values[2]))
            v.append(float(line_values[index_for_v])*multiply) # Velocity with nothing applied OJO
        events.append({'t': t, 'x': x, 'y': y, 'v': v})
        
    return events


def best_fit(t, v, model=acceleration, model_args=None):
    if model_args is None:
        model_args = []
    # Fit the exponential modeltion to the velocity data
    popt, pcov = curve_fit(model(*model_args), t, v, maxfev=10000)
    #tau_fit = popt[0]
    #v_fit = popt[1]
        
    # Calcular el Error Cuadrático Medio (ECM) entre los valores ajustados y los reales
    function = model(*model_args)
    errors = []
    for i, curr_t in enumerate(t):
        v_fit = function(curr_t, *popt)
        errors.append((v_fit - v[i]) ** 2)
        
    ecm = np.mean(errors)
    return popt, ecm
    
def double_acceleration(t, v, index_start, index_end, last_vd=None):
    best_index = -1
    best_error = float('inf')
    best_first_vd = None
    best_second_vd = None
    best_first_tau = None
    best_second_tau = None
    acc = acceleration()
    for i in range(index_start, index_end+1):
        if abs(i - index_start) < 2 or abs(index_end - i) < 2:
            continue
        popt_1, ecm_1 = best_fit(t[index_start: index_start+i+1], v[index_start: index_start+i+1], acceleration_with_vd, [v[index_start+i]])
        second_v = v[index_start+i: index_end+1]
        starting_v = acc(t[index_start+i], popt_1[0], v[index_start+i])
        if starting_v >= last_vd:
            continue
        popt_2, ecm_2 = best_fit(np.arange(len(second_v)) / 60, second_v, acceleration_with_start_v, [last_vd, starting_v])
        if ecm_1 + ecm_2 < best_error and popt_2[0] < 10:
            best_index = i
            best_first_vd = v[index_start+i]
            best_second_vd = last_vd
            best_first_tau = popt_1[0]
            best_second_tau = popt_2[0]
            best_error = ecm_1 + ecm_2
    
    return best_index, best_first_tau, best_second_tau, best_first_vd, best_second_vd, best_error



def deceleartion_following_distance(vel_start, positions, best_time):
    
    start_index = int(best_time*FPS)
    distance = abs(positions[start_index+AMOUNT_ZEROES] - positions[-AMOUNT_ZEROES-1]) 
    tau = distance / vel_start
    
    return {'tau': tau, 'distance': distance, 'velocity_at_best_time': vel_start}

def deceleration_cpm(v, curr_end, middle):
    v_data_full = v[AMOUNT_ZEROES : -AMOUNT_ZEROES]
    time = np.arange(len(v_data_full)) / FPS
    
    best_time, best_first_m, best_second_m, best_first_b, best_second_b = double_linear_regression(v_data_full, time, middle, curr_end)

    start_index = int(best_time * FPS)
    
    v_data = v_data_full[start_index:]
    t_data = np.arange(len(v_data)) / FPS
    
    popt, ecm = best_fit(t_data, v_data, model=cpm_deceleration_with_beta, model_args=[v_data[-1], 0.9])
    tau = popt[0]
    
    return {
        'best_time': best_time,
        'best_first_m': best_first_m,
        'best_second_m': best_second_m,
        'best_first_b': best_first_b,
        'best_second_b': best_second_b,
        'tau': tau,
        'velocity_at_best_time': v_data[0],
        'ecm': ecm,
    }
    

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

def cpm_parameters_for_acceleration(i, v, start, middles):
    curr_mid = middles[i]
    
    v_d = np.average(v[curr_mid-60:curr_mid + 1])
    v = v[start:curr_mid + 1]
    t = np.arange(len(v)) / FPS
    return t, v, cpm_acceleration_with_beta, [v_d, 0.9]