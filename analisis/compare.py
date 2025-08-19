import json
import numpy as np
from scipy.optimize import curve_fit
import plotly.graph_objects as go

from lib_analisis import acceleration


FILES_TO_USE = [1]  # Use all files from 01 to 14
folder_name = 'trans_events_by_ped'
FPS = 60

keys = []
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)

with open(f"analisis/pastos.json", "r") as f:
    pastos_data = json.load(f)
    if 'pastos' in pastos_data:
        pastos = pastos_data['pastos']
    else:
        raise KeyError("Key 'pastos' not found in pastos.json")

for key in keys:
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

    curr_pastos = pastos[key]['values']
    start = pastos[key]['start']
    curr_end = curr_pastos[0] - start

    for i, event in enumerate(events):
        fig = go.Figure()
        v = event['v']
        
        if i != 0:
            curr_end = curr_pastos[2*i] - curr_pastos[2*i - 2]
        
        v = v[start:curr_end+1]
        t = np.arange(len(v)) / FPS
        
        # Fit the exponential function to the velocity data
        popt, pcov = curve_fit(acceleration, t, v, maxfev=10000)

        tau_fit = popt

        print(f"Best fit parameters for event {i+1} of ped {key}: tau = {tau_fit}")
        
        if i != len(events) - 1:
            start = curr_pastos[2*i + 1] - curr_pastos[2*i]
    
        
    