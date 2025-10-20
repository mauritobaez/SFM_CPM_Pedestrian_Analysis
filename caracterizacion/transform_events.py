

import json
import os
import numpy as np
import plotly.graph_objects as go

from lib import add_vertical_line, get_middle

FILES_TO_USE = [i for i in range(1, 15)]  # Use all files from 01 to 14
EVENTS = [i for i in range(1,9)]  # Events to process
folder_name = 'only_events_60_v2'#['fft_with_30_zeros', 'no_fft_with_30_zeros']  # Change this to the folder you want to use
file_with_acc_info = 'analisis/acc_CPM_beta'  # File with acceleration info
DEC_NAME = 'analisis/dec_60'
WITH_NOTHING_TOO = False
ACC = True
DEC = False
MODEL = 'CPM'  # 'SFM' or 'CPM'
DOUBLE_LINES = False
DEC_EXP = True
SHOW = False
SAVE = True
name = 'only_events_CPM_v4_acc'  # Folder to save images
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
        doubles = pastos[key].get('doubles', {})
    shift = AMOUNT_ZEROES / FPS
    if DEC:
        ped_dec_info = dec_info[key]
    
    for i, event in enumerate(events):
        if ACC and i+1 == 1 and (key == '01' or key == '09'):
            continue  # Skip pedestrian 01 event 1 due to data issues
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
        fig.add_trace(go.Scatter(x=t, y=v, mode='lines', name='FFT Filtered Velocity 1.0', line=dict(color='orange'), opacity=0.7, line_width=3))
        
        
        middle = get_middle(y if i == 2 or i == 5 else x, AMOUNT_ZEROES)
        add_vertical_line(fig, t[middle], color='blue', width=2, showlegend=False)
        
        if ACC:
            tau = taus[i if not (key == '01' or key == '09') else i-1]
            v_d = vds[i if not (key == '01' or key == '09') else i-1]
            ts = t[AMOUNT_ZEROES:middle+1]
            theoretical_v = v_d * (1 - np.exp(-ts / tau)) if MODEL == 'SFM' else np.where(ts < tau, v_d * (ts / tau) ** 0.9, v_d)
            fig.add_trace(go.Scatter(x=ts, y=theoretical_v, mode='lines', name='Theoretical Velocity', line=dict(color='green', dash='dash')))
            if f'event_{i+1}' in doubles:
                double_info = doubles[f'event_{i+1}']
                best_index = double_info['best_index']
                first_tau = double_info['first_tau']
                second_tau = double_info['second_tau']
                first_vd = double_info['first_vd']
                second_vd = double_info['second_vd']
                
                t_first = t[AMOUNT_ZEROES: AMOUNT_ZEROES + best_index +1]
                t_second = t[AMOUNT_ZEROES + best_index: middle +1]
                
                theoretical_v_first = first_vd * (1 - np.exp(-t_first / first_tau))
                start_v_second = theoretical_v_first[-1]
                theoretical_v_second = start_v_second + (second_vd - start_v_second) * (1 - np.exp(-(t_second - t_second[0]) / second_tau))
                
                fig.add_trace(go.Scatter(x=t_first, y=theoretical_v_first, mode='lines', name='Theoretical Velocity 1', line=dict(color='purple', dash='dash')))
                fig.add_trace(go.Scatter(x=t_second, y=theoretical_v_second, mode='lines', name='Theoretical Velocity 2', line=dict(color='brown', dash='dash')))
        
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
                t_dec = t[int(best_time*60) + AMOUNT_ZEROES: -AMOUNT_ZEROES]
                theoretical_v_dec = v_M * np.exp(-(t_dec-best_time) / tau) if MODEL == 'SFM' else np.where(t_dec - best_time < tau, v_M * (1 - (t_dec - best_time) / tau)** 0.9, 0)
                fig.add_trace(go.Scatter(x=t_dec, y=theoretical_v_dec, mode='lines', name='Theoretical Deceleration', line=dict(color='red', dash='dash')))
            
                tau_follow = event_dec_info['tau_following_distance']
                velocity_at_best_time_follow = event_dec_info['velocity_at_best_time_following_distance']
                theoretical_v_dec_follow = velocity_at_best_time_follow * np.exp(-(t_dec-best_time) / tau_follow)
                fig.add_trace(go.Scatter(x=t_dec, y=theoretical_v_dec_follow, mode='lines', name='Theoretical Deceleration (Distance)', line=dict(color='brown', dash='dot')))
            
                tau_vm_fix = event_dec_info['tau_vm_fix']
                vm_vm_fix = event_dec_info['vm_vm_fix']
                theoretical_v_dec_vm_fix = vm_vm_fix * np.exp(-(t_dec-best_time) / tau_vm_fix)
                fig.add_trace(go.Scatter(x=t_dec, y=theoretical_v_dec_vm_fix, mode='lines', name='Theoretical Deceleration (Vm set)', line=dict(color='black', dash='dashdot')))
                
                tau_both = event_dec_info['tau_both']
                vm_both = event_dec_info['vm_both']
                theoretical_v_dec_both = vm_both * np.exp(-(t_dec-best_time) / tau_both)
                fig.add_trace(go.Scatter(x=t_dec, y=theoretical_v_dec_both, mode='lines', name='Theoretical Deceleration (Both)', line=dict(color='grey', dash='longdash')))
                
                
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
            xaxis=dict(title_font=dict(size=24), tickfont=dict(size=18), range=[0 if not DEC else t[middle], t[-AMOUNT_ZEROES-1]]),
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
        
