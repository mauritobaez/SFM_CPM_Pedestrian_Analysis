

import json
import numpy as np
from scipy.optimize import curve_fit


# Quizás cambiar el 1.3
def acceleration(parameter):
    def acc(t, tau):
        return parameter * (1 - np.exp(-t / tau))
    return acc

def decelar(parameter):
    def decel(t, tau):
        return parameter * np.exp(-t / tau)
    return decel

def get_pastos():
    with open(f"analisis/nuevos_pastos.json", "r") as f:
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
    tau_fit = popt[0]
        
    # Calcular el Error Cuadrático Medio (ECM) entre los valores ajustados y los reales
    function = model(*model_args)
    errors = []
    for i, curr_t in enumerate(t):
        v_fit = function(curr_t, tau_fit)
        errors.append((v_fit - v[i]) ** 2)
        
    ecm = np.mean(errors)
    return tau_fit, ecm
    
