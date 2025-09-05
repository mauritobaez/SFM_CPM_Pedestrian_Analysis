import os

from data_lib import fft_filter, hampel_filter


FILES_TO_USE = [2, 4]  # Use all files from 01 to 14
keys= []
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)
    
folder_name = "with_sqrt"  # This is the folder with the sqrt values
folder_name_output = "trans_events_by_ped"  # Output folder for events

pastos = {} 
pastos['01'] = [0, [235, 362, 762, 946, 1330, 1531, 1892, 2097, 2517, 2681, 3022, 3095, 3429, 3469, 3805]]
pastos['02'] = [0, [374, 563, 958, 1142, 1568, 1703, 2142, 2286, 2659, 2669, 3037, 3059, 3425, 3464, 3908]]
pastos['03'] = [0, [313, 468, 807, 1044, 1392, 1647, 1975, 2092, 2388, 2440, 2726, 2834, 3136, 3268, 3632]]
pastos['04'] = [104, [483, 691, 1094, 1243, 1629, 1654, 2026, 2043, 2394, 2412, 2772, 2893, 3263, 3327, 3727]]
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
FPS = 60  # Frames per second
VX_INDEX = 3
VY_INDEX = 4

for key in keys:

    with open(f"./archivosGerman/datos/{folder_name}/tXYvXvY{key}.txt", "r") as values:
        lines = values.readlines()
            
    # Se puede usar pastos + [len(lines)]
    curr_pasto = pastos[key][1]
    start_idx = pastos[key][0]
    event_counter = 0
    for i in range(1, len(curr_pasto)+1, 2):
        end_idx = curr_pasto[i] if i != len(curr_pasto) else curr_pasto[-1]
        event_lines = lines[start_idx:end_idx+1]
        v = []
        for lin in event_lines:
            line_values = lin.split(sep='\t')
            v.append(float(line_values[VY_INDEX if event_counter == 2 or event_counter == 5 else VX_INDEX]))
        event_counter += 1
        
        v_filtered = hampel_filter(v, 19, 2)
        v_fft1 = fft_filter(v_filtered, fs=FPS, highcut=1.0)
        
        # Replace each line in event_lines with t, x, y, v (where v is the filtered value)
        new_event_lines = []
        for idx, lin in enumerate(event_lines):
            line_values = lin.strip().split('\t')
            t, x, y = line_values[0], line_values[1], line_values[2]
            v_val = v_fft1[idx]
            new_event_lines.append(f"{t}\t{x}\t{y}\t{v_val}\t{v[idx]}\n")
        event_lines = new_event_lines
        
        if not os.path.exists(folder_name_output):
            os.makedirs(folder_name_output) 
        
        with open(f"{folder_name_output}/ped_{key}_event_{i//2 + 1}.txt", "w") as out_file:
            out_file.writelines(event_lines)
        start_idx = curr_pasto[i-1]


