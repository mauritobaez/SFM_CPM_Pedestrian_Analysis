

import json
import numpy as np
from scipy.optimize import curve_fit


# Quizás cambiar el 1.3
def acceleration(parameter):
    def acc(t, tau):
        return parameter * (1 - np.exp(-t / tau))
    return acc

def deceleration(parameter):
    def dece(t, tau):
        return parameter * np.exp(-t / tau)
    return dece


def get_pastos():
    with open(f"analisis/pastos.json", "r") as f:
        pastos_data = json.load(f)
        if 'pastos' in pastos_data:
            pastos = pastos_data['pastos']
        else:
            raise KeyError("Key 'pastos' not found in pastos.json")
    return pastos


def get_events(folder_name: str, key: str):
    events = []
    for event_number in range(1, 9):
        t = []
        x = []
        y = []
        v = []
        with open(f"archivosGerman/{folder_name}/ped_{key}_event_{event_number}.txt", "r") as values:
            lines = values.readlines()
        for line in lines:
            line_values = line.split(sep='\t')
            t.append(float(line_values[0]))
            x.append(float(line_values[1]))
            y.append(float(line_values[2]))
            v.append(abs(float(line_values[3])))    # Ojo que usamos el valor absoluto de la velocidad
        events.append({'t': t, 'x': x, 'y': y, 'v': v})
        
    return events


def best_fit(t, v, model=acceleration, model_args=None):
    if model_args is None:
        model_args = []
    # Fit the exponential modeltion to the velocity data
    popt, pcov = curve_fit(model(*model_args), t, v, maxfev=10000)
    tau_fit = popt[0]
        
    # Calcular el Error Cuadrático Medio (ECM) entre los valores ajustados y los reales
    v_fit = model(*model_args)(t, tau_fit)
    ecm = np.mean((v - v_fit) ** 2)
    return tau_fit, ecm
    
