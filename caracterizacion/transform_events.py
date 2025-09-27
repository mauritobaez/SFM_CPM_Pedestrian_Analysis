

import json
import os
import numpy as np
import plotly.graph_objects as go

from lib import add_vertical_line, get_middle

FILES_TO_USE = [i for i in range(1,15)]  # Use all files from 01 to 14
EVENTS = [i for i in range(1,9)]  # Events to process
folder_name = 'only_events_60_fix'#['fft_with_30_zeros', 'no_fft_with_30_zeros']  # Change this to the folder you want to use
file_with_acc_info = 'analisis/acc_60'  # File with acceleration info
DEC_NAME = 'analisis/dec_60'
WITH_NOTHING_TOO = True
ACC = False
DEC = False
DOUBLE_LINES = True
DEC_EXP = True
SHOW = False
SAVE = True
name = 'both_60_fix'  # Folder to save images
AMOUNT_ZEROES = 60
FPS = 60
keys= []

if ACC:
    with open(f"{file_with_acc_info}.json", "r") as f:
        pastos_data = json.load(f)
        if 'pastos' in pastos_data:
            pastos = pastos_data['pastos']
        else:
            raise KeyError("Key 'pastos' not found in pastos.json")

if DEC:
    with open(f"{DEC_NAME}.json", "r") as f:
        dec_info = json.load(f)["deceleration_info"]


for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)


for key in keys:
    events = []
    for event_number in range(1, 9):
        t = []
        x = []
        y = []
        v = []
        v_with_nothing = []
        
        if event_number in [3, 4, 5, 6]:
            multiply = -1.0
        else:
            multiply = 1.0
        
        with open(f"archivosGerman/{folder_name}/ped_{key}_event_{event_number}.txt", "r") as values:
            lines = values.readlines()
        for line in lines:
            line_values = line.split(sep='\t')
            t.append(float(line_values[0]))
            x.append(float(line_values[1]))
            y.append(float(line_values[2]))
            v.append(float(line_values[3]) * multiply)
            v_with_nothing.append(float(line_values[4]) * multiply)
            
        events.append({'t': t, 'x': x, 'y': y, 'v': v, 'v_with_nothing': v_with_nothing})

    if ACC:
        taus = pastos[key]['taus']
        vds = pastos[key]['vds']
    shift = AMOUNT_ZEROES / FPS
    if DEC:
        ped_dec_info = dec_info[key]
    
    for i, event in enumerate(events):
        
        if i+1 not in EVENTS:
            continue
        
        fig = go.Figure()
        x = event['x']
        y = event['y']
        v = event['v']
        v_with_nothing = event['v_with_nothing']
        t = np.arange(len(v)) / FPS
        
        t = np.array(t) - shift
        
        if WITH_NOTHING_TOO:
            fig.add_trace(go.Scatter(x=t, y=v_with_nothing, mode='lines', name='Raw Velocity', line=dict(color='red'), opacity=0.5))
        fig.add_trace(go.Scatter(x=t, y=v, mode='lines', name='FFT Filtered Velocity 1.0', line=dict(color='orange'), opacity=0.7))
        
        
        middle = get_middle(y if i == 2 or i == 5 else x, AMOUNT_ZEROES)
        add_vertical_line(fig, t[middle], color='blue', width=2, showlegend=False)
        
        if ACC:
            tau = taus[i]
            v_d = vds[i]
            ts = t[AMOUNT_ZEROES:middle+1]
            theoretical_v = v_d * (1 - np.exp(-ts / tau))
            fig.add_trace(go.Scatter(x=ts, y=theoretical_v, mode='lines', name='Theoretical Velocity', line=dict(color='green', dash='dash')))
        
        if DEC:
            event_dec_info = ped_dec_info[f'event_{i+1}']
            best_time = event_dec_info['best_time']
            best_first_m = event_dec_info['best_first_m']
            best_second_m = event_dec_info['best_second_m']
            best_first_b = event_dec_info['best_first_b']
            best_second_b = event_dec_info['best_second_b']
            add_vertical_line(fig, best_time, color='green', width=2, showlegend=True, legend='Start Deceleration')
            if DOUBLE_LINES:
                # Create time arrays for the lines
                first_time = np.array([t[middle], best_time])
                second_time = np.array([best_time, t[-AMOUNT_ZEROES-1]])
                
                # Add back the shift to the times before calculating y values
                first_line = best_first_m * (first_time) + best_first_b
                second_line = best_second_m * (second_time) + best_second_b
                
                fig.add_trace(go.Scatter(x=first_time, y=first_line, mode='lines', name='Best Fit 1', line=dict(color='purple', dash='dash')))
                fig.add_trace(go.Scatter(x=second_time, y=second_line, mode='lines', name='Best Fit 2', line=dict(color='purple', dash='dash')))
            
            if DEC_EXP:
                tau = event_dec_info['tau']
                v_M = event_dec_info['velocity_at_best_time']
                t_dec = t[int(best_time*60) + AMOUNT_ZEROES: -AMOUNT_ZEROES-1]
                theoretical_v_dec = v_M * np.exp(-(t_dec-best_time) / tau)    # Revisar esto
                fig.add_trace(go.Scatter(x=t_dec, y=theoretical_v_dec, mode='lines', name='Theoretical Deceleration Velocity', line=dict(color='red', dash='dash')))
            
            
        add_vertical_line(fig, 0, color='black', width=2, showlegend=False)  # Start acceleration
        add_vertical_line(fig, t[-AMOUNT_ZEROES-1], color='black', width=2, showlegend=False) # End deceleration       
    
        
        fig.update_xaxes(showgrid=False, dtick=5) 
        fig.update_yaxes(showgrid=False)
        fig.update_layout(
            title=f"Pedestrian {key} - Event {i+1}",
            xaxis_title="Time [s]",
            yaxis_title="Velocity [m/s]",
            legend=dict(title="Legend"),
            template="plotly_white",
            showlegend=True,
            font=dict(size=20),
            xaxis=dict(title_font=dict(size=24), tickfont=dict(size=18), range=[-2.5, 8.5]),
            yaxis=dict(title_font=dict(size=24), tickfont=dict(size=18), range=[-0.3, 2]),
        )

        if SHOW:
            fig.show()

        if SAVE:
            if not os.path.exists(f"./{name}"):
                os.makedirs(f"./{name}")
            fig.write_image(
            f"./{name}/speeds_{key}_{(i+1):02}.png",
            width=1920,
            height=1080,
            scale=2  # Higher scale for better resolution
            )
        
