import os
import numpy as np
import csv


FILES_TO_USE = [i for i in range(1, 15)]  # Use all files from 01 to 14
EVENTS = [i for i in range(1,9)]  # Events to process
folder_name = 'only_events_60_v2'
output_folder = 'filtered_and_raw'  # Folder to save images

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

keys = []
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)

AMOUNT_ZEROES = 60
FPS = 60
for key in keys:
    index = 0
    for event_number in range(1, 9):
        v_filtered = []
        v_raw = []
        
        
        if event_number in [3, 4, 5, 6]:
            multiply = -1.0
        else:
            multiply = 1.0
        
        with open(f"archivosGerman/{folder_name}/ped_{key}_event_{event_number}.txt", "r") as values:
            lines = values.readlines()
        for line in lines:
            line_values = line.split(sep='\t')
            v_filtered.append(float(line_values[3]) * multiply)
            v_raw.append(float(line_values[4]) * multiply)
        
        v_filtered = v_filtered[AMOUNT_ZEROES: -AMOUNT_ZEROES]
        v_raw = v_raw[AMOUNT_ZEROES: -AMOUNT_ZEROES]
        t = np.arange(len(v_filtered)) / FPS
            
        filename = f"{output_folder}/Vel_Raw_and_Smooth_P{key}_E{event_number}.csv"
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['tiempo (s)', 'velocidad raw', 'velocidad fft filtrada'])
            for ti, v_r, v_f in zip(t, v_raw, v_filtered):
                writer.writerow([ti, v_r, v_f])
            
