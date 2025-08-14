import numpy as np
import plotly.graph_objects as go


FILES_TO_USE = [i for i in range(1,15)]  # Use all files from 01 to 14
folder_name = 'events_by_ped'#['fft_with_30_zeros', 'no_fft_with_30_zeros']  # Change this to the folder you want to use
FPS = 60

keys = []
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
        with open(f"{folder_name}/ped_{key}_event_{event_number}.txt", "r") as values:
            lines = values.readlines()
        for line in lines:
            line_values = line.split(sep='\t')
            t.append(float(line_values[0]))
            x.append(float(line_values[1]))
            y.append(float(line_values[2]))
            v.append(abs(float(line_values[3])))
        events.append({'t': t, 'x': x, 'y': y, 'v': v})

    for i, event in enumerate(events):
        fig = go.Figure()
        t = np.arange(len(v)) / FPS
        x = event['x']
        y = event['y']
        v = event['v']
        
    