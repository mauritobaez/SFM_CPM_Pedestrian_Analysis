import json
import numpy as np
from scipy.optimize import curve_fit
import plotly.graph_objects as go

from lib_analisis import acceleration, deceleration


FILES_TO_USE = [i for i in range(1, 15)]  # Use all files from 01 to 14
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
    start = 0 # pastos[key]['start']
    curr_end = curr_pastos[0] - start
    taus = []
    ecms = []
    middles = pastos[key]['middles']

    for i, event in enumerate(events):
        fig = go.Figure()
        v = event['v']
        
        if i != 0:
            curr_end = curr_pastos[2*i] - curr_pastos[2*i - 2]
        
        curr_mid = middles[i]
        mid_vel = v[curr_mid]
        
        #print(f"Event {i+1} of ped {key} - Start: {start/60}, End: {curr_end/60}, Middle: {curr_mid/60}, Mid Velocity: {mid_vel}")
        
        v = v[start:curr_mid+1]
        #v = v[curr_mid: curr_end+1]
        t = np.arange(len(v)) / FPS
        
        # Fit the exponential function to the velocity data
        popt, pcov = curve_fit(acceleration(mid_vel), t, v, maxfev=10000)

        tau_fit = popt[0]
        
        # Calcular el Error Cuadrático Medio (ECM) entre los valores ajustados y los reales
        v_fit = acceleration(mid_vel)(t, tau_fit)
        ecm = np.mean((v - v_fit) ** 2)
        #print(f"ECM for event {i+1} of ped {key}: {ecm}")
        ecms.append(ecm)

        #print(f"Best fit parameters for event {i+1} of ped {key}: tau = {tau_fit}")
        taus.append(tau_fit)
        
        if i != len(events) - 1:
            start = curr_pastos[2*i + 1] - curr_pastos[2*i]
    
    pastos[key]['taus'] = taus
    #print(f"Ped {key} \"taus\": {[float(tau) for tau in taus]}")
    pastos[key]['ecms'] = ecms
    

#    pastos[key].pop('start', None)
#    pastos[key].pop('values', None)
#    pastos[key].pop('middles', None)
#    
#with open("analisis/taus.json", "w") as f_out:
#    json.dump({'pedestrians': pastos}, f_out, indent=4)

with open("analisis/pastos_with_taus.json", "w") as f_out:
    json.dump({'pastos': pastos}, f_out, indent=4)
    