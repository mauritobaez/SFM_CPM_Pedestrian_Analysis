

import json
import os
import numpy as np
import plotly.graph_objects as go

from lib import add_vertical_line, get_middle

FILES_TO_USE = [i for i in range(1,15)]  # Use all files from 01 to 14
EVENTS = [i for i in range(1,9)]  # Events to process
folder_name = 'trans_events_by_ped'#['fft_with_30_zeros', 'no_fft_with_30_zeros']  # Change this to the folder you want to use
ACC = False
DEC = True
FPS = 60
keys= []

with open(f"analisis/pastos_with_taus.json", "r") as f:
    pastos_data = json.load(f)
    if 'pastos' in pastos_data:
        pastos = pastos_data['pastos']
    else:
        raise KeyError("Key 'pastos' not found in pastos.json")

for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)

with open(f"analisis/events_dec_info.json", "r") as f:
    dec_info = json.load(f)["deceleration_info"]

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
            v.append(abs(float(line_values[3])))
            
        events.append({'t': t, 'x': x, 'y': y, 'v': v})

    curr_pasto = pastos[key]['values']
    prev_end_stop = 0   # No hace falta que sea el start porque ya viene cortado el evento por el divide_in_events.py
    taus = pastos[key]['taus']
    initial_offset = pastos[key]['start']
    shift = 0
    middles = []
    ped_dec_info = dec_info[key]    
    
    
    for i, event in enumerate(events):
        
        fig = go.Figure()
        x = event['x']
        y = event['y']
        v = event['v']
        #t = event['t']
        t = np.arange(len(v)) / FPS
        if i != 0:
            shift = t[prev_end_stop]
        t = np.array(t) - shift
        fig.add_trace(go.Scatter(x=t, y=v, mode='lines', name='FFT Filtered Velocity 1.0', line=dict(color='orange'), opacity=0.7))
        
        middle = get_middle(y if i == 2 or i == 5 else x, prev_end_stop)
        add_vertical_line(fig, t[middle], color='blue', width=2, showlegend=False)
        
        if ACC:
            tau = taus[i]
            mid_vel = v[middle]
            theoretical_v = mid_vel * (1 - np.exp(-t / tau))
            fig.add_trace(go.Scatter(x=t, y=theoretical_v, mode='lines', name='Theoretical Velocity', line=dict(color='green', dash='dash')))
        
        if DEC:
            event_dec_info = ped_dec_info[f'event_{i+1}']
            end_dec = (curr_pasto[2*i] - curr_pasto[2*i - 2])/60 if i != 0 else (curr_pasto[0] - initial_offset)/60
            dec_tau = event_dec_info['tau_dec']
            dec_start_vel = event_dec_info['v_d']
            dec_start_time = end_dec - event_dec_info['time_to_zero']
            theoretical_v_dec = dec_start_vel * np.exp(-(t - dec_start_time + shift) / dec_tau)
            theoretical_v_dec2 = theoretical_v_dec[int(dec_start_time*60): int(end_dec * 60)]
            t_dec = t[int(dec_start_time*60): int(end_dec * 60)]
            fig.add_trace(go.Scatter(x=t_dec, y=theoretical_v_dec2, mode='lines', name='Theoretical Deceleration Velocity', line=dict(color='purple', dash='dash')))
            add_vertical_line(fig, dec_start_time - shift, color='green', width=2, showlegend=True, legend='Start Deceleration') 
            
        if i != 0:
            add_vertical_line(fig, prev_end_stop/60 - shift, color='black', width=2, showlegend=False)  # Start acceleration
            add_vertical_line(fig, (curr_pasto[2*i] - curr_pasto[2*i - 2])/60 - shift, color='black', width=2, showlegend=False) # End deceleration
        else:
            add_vertical_line(fig, (curr_pasto[0] - initial_offset)/60, color='black', width=2, showlegend=False)    # End deceleration
        
        if i != len(events) - 1:
            prev_end_stop = curr_pasto[2*i + 1] - curr_pasto[2*i]
            
    
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
            xaxis=dict(title_font=dict(size=24), tickfont=dict(size=18), range=[-5, 12]),
            yaxis=dict(title_font=dict(size=24), tickfont=dict(size=18), range=[-0.3, 2]),
        )

        #middles.append(middle)
        #fig.show()

        name = "dec_events_fit"
        if not os.path.exists(f"./{name}"):
           os.makedirs(f"./{name}")
        fig.write_image(
           f"./{name}/speeds_{key}_{(i+1):02}.png",
           width=1920,
           height=1080,
           scale=2  # Higher scale for better resolution
        )
    #print(f"Processed pedestrian {key} with {len(events)} events. Middle indices: {middles}")
        
