

import numpy as np
import plotly.graph_objects as go

from data_lib import fft_filter, hampel_filter, moving_average_smoothing

FILES_TO_USE = [4]  # Use all files from 01 to 14
folder_name = 'events_by_ped'#['fft_with_30_zeros', 'no_fft_with_30_zeros']  # Change this to the folder you want to use
FPS = 60
keys= []


for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)

for key in keys:
    events = []
    for event_number in range(1, 9):
        t = []
        x = []
        y = []
        vX = []
        vY = []
        with open(f"events_by_ped/ped_{key}_event_{event_number}.txt", "r") as values:
            lines = values.readlines()
        for line in lines:
            line_values = line.split(sep='\t')
            t.append(float(line_values[0]))
            x.append(float(line_values[1]))
            y.append(float(line_values[2]))
            vX.append(abs(float(line_values[3])))
            vY.append(abs(float(line_values[4])))
        events.append({'t': t, 'x': x, 'y': y, 'vX': vX, 'vY': vY})

    

    for i, event in enumerate(events):
        #if i+1 != 7:
        #    continue
        fig = go.Figure()
        x = event['x']
        y = event['y']
        v = event['vY'] if i == 2 or i == 5 else event['vX']
        t = event['t']
        
        v_filtered = hampel_filter(v, 19, 2)
        
        v_fft = fft_filter(v_filtered, fs=FPS, highcut=0.5)
        v_fft1 = fft_filter(v, fs=FPS, highcut=1.0)
        #v_mov_avg = moving_average_smoothing(v_filtered, window_size=5)
        
        fig.add_trace(go.Scatter(x=t, y=v_filtered, mode='markers', name='Velocity', marker=dict(color='red'), opacity=1))
        fig.add_trace(go.Scatter(x=t, y=v_fft, mode='lines', name='FFT Filtered Velocity 0.5', line=dict(color='blue'), opacity=0.7))
        #fig.add_trace(go.Scatter(x=t, y=v_mov_avg, mode='lines', name='Moving Average Smoothed Velocity', line=dict(color='green'), opacity=0.7))
        fig.add_trace(go.Scatter(x=t, y=v_fft1, mode='lines', name='FFT Filtered Velocity 1.0', line=dict(color='orange'), opacity=0.7))
        
    
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
            xaxis=dict(title_font=dict(size=24), tickfont=dict(size=18)),
            yaxis=dict(title_font=dict(size=24), tickfont=dict(size=18)),
        )

        fig.show()
