
import numpy as np
from lib import get_all_events, get_stops_complete

FILES_TO_USE = [i for i in range(1,15)]  # Use all files from 01 to 14
folder_names = ['no_fft_with_30_zero']#['fft_with_30_zeros', 'no_fft_with_30_zeros']  # Change this to the folder you want to use

keys= []
figures = {}
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)

for key in keys:
    
    for folder_name in folder_names:
        
        time = []
        vX = []
        vY = []
        x = []
        y = []

        with open(f"./archivosGerman/{folder_name}/tXYvXvY{key}.txt", "r") as values:
            lines = values.readlines()
        for line in lines:
            line_values = line.split(sep='\t')
            time.append(float(line_values[0]))
            x.append(float(line_values[1]))
            y.append(float(line_values[2]))
            vX.append(float(line_values[3]))
            vY.append(float(line_values[4]))
        velocities = []
        
    
        max_speed = 0.38 if key == '12' or key == '14' else 0.2 if key == '04' else 0.181 if key == '13' else 0.163
        stops = get_stops_complete(max_speed, time, vX, vY)
        
        events = get_all_events(time, vX, vY, stops)
        
        for i, event in enumerate(events):
            t = np.arange(0,len(event))/60
            data = np.c_[t, x[stops[i][0]:stops[i][0]+len(event)], y[stops[i][0]:stops[i][0]+len(event)] , event]
            outFile = f'tXYV_{key}_{i+1:02d}.txt'
            np.savetxt(f'./no_fft_events_data/{outFile}', data, delimiter='\t',fmt='%.8e')