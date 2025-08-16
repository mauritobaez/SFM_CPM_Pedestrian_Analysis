

import os
import numpy as np
import plotly.graph_objects as go

from lib import add_vertical_line, get_middle

FILES_TO_USE = [i for i in range(1,15)]  # Use all files from 01 to 14
folder_name = 'trans_events_by_ped'#['fft_with_30_zeros', 'no_fft_with_30_zeros']  # Change this to the folder you want to use
FPS = 60
keys= []

pastos = {} 
pastos['01'] = [0, [235, 362, 762, 946, 1330, 1531, 1892, 2097, 2517, 2681, 3022, 3095, 3429, 3469, 3805]]
pastos['02'] = [0, [374, 563, 958, 1142, 1538, 1703, 2142, 2286, 2659, 2669, 3037, 3059, 3425, 3464, 3908]]
pastos['03'] = [0, [313, 468, 807, 1044, 1392, 1647, 1975, 2092, 2388, 2440, 2726, 2834, 3136, 3268, 3632]]
pastos['04'] = [104, [483, 691, 1094, 1243, 1629, 1654, 2026, 2043, 2394, 2412, 2865, 2893, 3263, 3327, 3727]]
pastos['05'] = [0, [355, 553, 856, 937, 1273, 1316, 1648, 1734, 2050, 2161, 2468, 2595, 2908, 3045, 3342]]
pastos['06'] = [82, [428, 468, 815, 852, 1148, 1250, 1567, 1671, 2015, 2124, 2446, 2573, 2890, 2937, 3292]]
pastos['07'] = [0, [324, 387, 705, 799, 1114, 1244, 1574, 1683, 2022, 2122, 2455, 2474, 2833, 2872, 3221]]
pastos['08'] = [49, [406, 472, 792, 874, 1233, 1324, 1689, 1795, 2137, 2204, 2545, 2592, 2924, 3025, 3368]]
pastos['09'] = [0, [313, 486, 787, 902, 1223, 1301, 1646, 1695, 2021, 2141, 2441, 2578, 2901, 2994, 3317]]
pastos['10'] = [57, [417, 511, 892, 969, 1325, 1357, 1701, 1764, 2110, 2194, 2508, 2632, 2950, 3062, 3389]]
pastos['11'] = [0, [350, 458, 788, 828, 1189, 1278, 1589, 1726, 2066, 2141, 2502, 2562, 2909, 2979, 3304]]
pastos['12'] = [17, [344, 356, 658, 757, 1110, 1190, 1521, 1602, 1946, 2018, 2335, 2435, 2739, 2821, 3145]]
pastos['13'] = [0, [379, 413, 754, 792, 1166, 1235, 1605, 1615, 1970, 2011, 2381, 2426, 2762, 2802, 3163]]
pastos['14'] = [0, [374, 481, 825, 891, 1254, 1346, 1651, 1677, 1990, 2033, 2395, 2461, 2780, 2838, 3142]]

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
        
        with open(f"archivosGerman/{folder_name}/ped_{key}_event_{event_number}.txt", "r") as values:
            lines = values.readlines()
        for line in lines:
            line_values = line.split(sep='\t')
            t.append(float(line_values[0]))
            x.append(float(line_values[1]))
            y.append(float(line_values[2]))
            v.append(abs(float(line_values[3])))
            
        events.append({'t': t, 'x': x, 'y': y, 'v': v})

    curr_pasto = pastos[key][1]
    prev_end_stop = 0   # No hace falta que sea el start porque ya viene cortado el evento por el divide_in_events.py
    initial_offset = pastos[key][0]
    middles = []
    for i, event in enumerate(events):
        fig = go.Figure()
        x = event['x']
        y = event['y']
        v = event['v']
        #t = event['t']
        t = np.arange(len(v)) / FPS
        
        
        fig.add_trace(go.Scatter(x=t, y=v, mode='lines', name='FFT Filtered Velocity 1.0', line=dict(color='orange'), opacity=0.7))
        
        middle = get_middle(y if i == 2 or i == 5 else x, prev_end_stop)
        add_vertical_line(fig, t[middle], color='blue', width=2, showlegend=False)
        
        if i != 0:
            add_vertical_line(fig, prev_end_stop/60, color='black', width=2, showlegend=False)  # Start acceleration
            add_vertical_line(fig, (curr_pasto[2*i] - curr_pasto[2*i - 2])/60, color='black', width=2, showlegend=False) # End deceleration
        else:
            add_vertical_line(fig, (curr_pasto[0] - initial_offset)/60, color='black', width=2, showlegend=False)    # End deceleration
        
        if i != len(events) - 1:
            prev_end_stop = curr_pasto[2*i + 1] - curr_pasto[2*i]
    
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

        middles.append(middle)
        #fig.show()

        #name = "indep_events_3"
        #if not os.path.exists(f"./{name}"):
        #   os.makedirs(f"./{name}")
        #fig.write_image(
        #   f"./{name}/speeds_{key}_{(i+1):02}.png",
        #   width=1920,
        #   height=1080,
        #   scale=2  # Higher scale for better resolution
        #)
    print(f"Processed pedestrian {key} with {len(events)} events. Middle indices: {middles}")
        
