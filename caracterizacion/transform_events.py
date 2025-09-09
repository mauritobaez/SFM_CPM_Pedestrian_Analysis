

import json
import os
import numpy as np
import plotly.graph_objects as go

from lib import add_vertical_line, get_middle

FILES_TO_USE = [i for i in range(1,15)]  # Use all files from 01 to 14
EVENTS = [i for i in range(1,9)]  # Events to process
folder_name = 'only_events'#['fft_with_30_zeros', 'no_fft_with_30_zeros']  # Change this to the folder you want to use
ACC = True
DEC = False
AMOUNT_ZEROES = 30
FPS = 60
keys= []

with open(f"analisis/nuevos_pastos.json", "r") as f:
    pastos_data = json.load(f)
    if 'pastos' in pastos_data:
        pastos = pastos_data['pastos']
    else:
        raise KeyError("Key 'pastos' not found in pastos.json")

for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)

with open(f"analisis/viejos/events_dec_info.json", "r") as f:
    dec_info = json.load(f)["deceleration_info"]

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

    #curr_pasto = pastos[key]['values']
    #prev_end_stop = 0   # No hace falta que sea el start porque ya viene cortado el evento por el divide_in_events.py
    taus = pastos[key]['taus']
    #initial_offset = pastos[key]['start']
    shift = AMOUNT_ZEROES / FPS
    ped_dec_info = dec_info[key]
    middles = []
    
    for i, event in enumerate(events):
        
        fig = go.Figure()
        x = event['x']
        y = event['y']
        v = event['v']
        v_with_nothing = event['v_with_nothing']
        t = np.arange(len(v)) / FPS
        
        t = np.array(t) - shift
        
        #fig.add_trace(go.Scatter(x=t, y=v_with_nothing, mode='lines', name='Raw Velocity', line=dict(color='red'), opacity=0.5))
        fig.add_trace(go.Scatter(x=t, y=v, mode='lines', name='FFT Filtered Velocity 1.0', line=dict(color='orange'), opacity=0.7))
        
        
        middle = get_middle(y if i == 2 or i == 5 else x, AMOUNT_ZEROES)
        add_vertical_line(fig, t[middle], color='blue', width=2, showlegend=False)
        
        if ACC:
            tau = taus[i]
            mid_vel = v[middle]
            ts = t[AMOUNT_ZEROES:middle+1]
            theoretical_v = mid_vel * (1 - np.exp(-ts / tau))
            fig.add_trace(go.Scatter(x=ts, y=theoretical_v, mode='lines', name='Theoretical Velocity', line=dict(color='green', dash='dash')))
        
        if DEC:
            event_dec_info = ped_dec_info[f'event_{i+1}']
            end_dec = t[-AMOUNT_ZEROES-1]
            dec_tau = event_dec_info['tau_dec']
            dec_start_vel = event_dec_info['v_d']
            dec_start_time = end_dec - event_dec_info['time_to_zero']
            theoretical_v_dec = dec_start_vel * np.exp(-(t - dec_start_time + shift) / dec_tau)
            theoretical_v_dec2 = theoretical_v_dec[int(dec_start_time*60): int(end_dec * 60)]
            t_dec = t[int(dec_start_time*60): int(end_dec * 60)]
            fig.add_trace(go.Scatter(x=t_dec, y=theoretical_v_dec2, mode='lines', name='Theoretical Deceleration Velocity', line=dict(color='purple', dash='dash')))
            add_vertical_line(fig, dec_start_time - shift, color='green', width=2, showlegend=True, legend='Start Deceleration') 
            
        add_vertical_line(fig, 0, color='black', width=2, showlegend=False)  # Start acceleration
        add_vertical_line(fig, t[-AMOUNT_ZEROES-1], color='black', width=2, showlegend=False) # End deceleration       
    
        if i+1 not in EVENTS:
            continue
        
        fig.update_xaxes(showgrid=False, dtick=5) 
        fig.update_yaxes(showgrid=False)
        fig.update_layout(
            title=f"Event {i+1} - Pedestrian {key}",
            xaxis_title="Time [s]",
            yaxis_title="Velocity [m/s]",
            legend=dict(title="Legend"),
            template="plotly_white",
            showlegend=True,
            font=dict(size=20),
            xaxis=dict(title_font=dict(size=24), tickfont=dict(size=18), range=[-1, 9]),
            yaxis=dict(title_font=dict(size=24), tickfont=dict(size=18), range=[-0.3, 2]),
        )

        #fig.show()

        name = "smooth_vs_acceleration"
        if not os.path.exists(f"./{name}"):
           os.makedirs(f"./{name}")
        fig.write_image(
           f"./{name}/speeds_{key}_{(i+1):02}.png",
           width=1920,
           height=1080,
           scale=2  # Higher scale for better resolution
        )
        
