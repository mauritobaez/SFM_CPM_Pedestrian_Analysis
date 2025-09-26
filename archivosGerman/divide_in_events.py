import os
import numpy as np

from data_lib import fft_filter, hampel_filter


FILES_TO_USE = [i for i in range(1,15)]  # Use all files from 01 to 14
keys= []
for i in FILES_TO_USE:
    key = f"{i:02}"    
    keys.append(key)
    
folder_name = "with_sqrt"  # This is the folder with the sqrt values
folder_name_output = "only_events_60"  # Output folder for events

pastos = {} 
pastos['01'] = [[1, 235], [362, 762], [946, 1337], [1532, 1905], [2096, 2521], [2674, 3031], [3095, 3429], [3463, 3820]]
pastos['02'] = [[2, 373], [564, 960], [1142, 1562], [1694, 2159], [2285, 2659], [2669, 3043], [3045, 3433], [3453, 3908]]
pastos['03'] = [[1, 313], [464, 806], [1024, 1392], [1625, 2001], [2063, 2388], [2434, 2729], [2814, 3136], [3259, 3632]]
pastos['04'] = [[104, 483], [692, 1038], [1243, 1626], [1654, 2019], [2044, 2393], [2419, 2766], [2894, 3221], [3314, 3674]]
pastos['05'] = [[6, 362], [553, 856], [937, 1282], [1306, 1652], [1722, 2050], [2139, 2477], [2568, 2908], [3046, 3342]]
pastos['06'] = [[82, 427], [469, 818], [850, 1148], [1246, 1567], [1666, 2012], [2122, 2445], [2574, 2897], [2933, 3283]]
pastos['07'] = [[1, 331], [387, 704], [787, 1113], [1245, 1587], [1673, 2021], [2120, 2453], [2474, 2833], [2870, 3221]]
pastos['08'] = [[33, 406], [463, 798], [861, 1233], [1324, 1696], [1792, 2136], [2204, 2499], [2593, 2934], [3014, 3368]]
pastos['09'] = [[0, 295], [476, 793], [885, 1222], [1294, 1659], [1692, 2006], [2123, 2450], [2541, 2919], [2993, 3320]]
pastos['10'] = [[58, 425], [498, 892], [963, 1324], [1354, 1709], [1757, 2116], [2190, 2507], [2632, 2953], [3043, 3401]]
pastos['11'] = [[4, 379], [458, 788], [828, 1158], [1268, 1586], [1710, 2065], [2129, 2499], [2558, 2915], [2958, 3293]]
pastos['12'] = [[14, 343], [351, 658], [751, 1113], [1181, 1558], [1577, 1951], [2015, 2336], [2431, 2741], [2812, 3180]]
pastos['13'] = [[3, 381], [412, 753], [792, 1166], [1207, 1604], [1614, 1975], [2008, 2379], [2408, 2765], [2799, 3162]]
pastos['14'] = [[2, 374], [473, 824], [870, 1254], [1346, 1651], [1675, 1989], [2023, 2395], [2446, 2779], [2837, 3142]]
FPS = 60  # Frames per second
VX_INDEX = 3
VY_INDEX = 4
AMOUNT_ZEROES = 60  # Amount of zeroes to add at the beginning and end of each event

for key in keys:

    with open(f"./archivosGerman/datos/{folder_name}/tXYvXvY{key}.txt", "r") as values:
        lines = values.readlines()
            
    event_counter = 0
    for inicio_fin in pastos[key]:
        event_lines = lines[inicio_fin[0]:inicio_fin[1]+1]
        v = []
        v_index = VY_INDEX if event_counter == 2 or event_counter == 5 else VX_INDEX
        for lin in event_lines:
            line_values = lin.split(sep='\t')
            v.append(float(line_values[v_index]))
        event_counter += 1
                
        v_filtered_original = hampel_filter(v, 19, 2)
        
        first_value = np.inf
        last_value = np.inf
        beg_queue = 0.0
        end_queue = 0.0
        delta = 0.0005 if event_counter in [3,4,5,6] else -0.0005
        while abs(last_value) > 0.01 and abs(first_value) > 0.01:
            v_filtered = [beg_queue] * AMOUNT_ZEROES + v_filtered_original + [end_queue] * AMOUNT_ZEROES
            v_fft1 = fft_filter(v_filtered, fs=FPS, highcut=1.0)            
            first_value = v_fft1[AMOUNT_ZEROES]
            last_value = v_fft1[-AMOUNT_ZEROES-1]
            if abs(last_value) > 0.01:
                end_queue += delta
            if abs(first_value) > 0.01:
                beg_queue +=delta
            
            
        # Replace each line in event_lines with t, x, y, v (where v is the filtered value)
        new_event_lines = []
        
        for i in range(AMOUNT_ZEROES):
            new_event_lines.append(f"0.0\t0.0\t0.0\t{v_fft1[i]}\t0.0\n")
        
        for idx, lin in enumerate(event_lines):
            line_values = lin.strip().split('\t')
            t, x, y = line_values[0], line_values[1], line_values[2]
            new_event_lines.append(f"{t}\t{x}\t{y}\t{v_fft1[idx+AMOUNT_ZEROES]}\t{v_filtered[idx+AMOUNT_ZEROES]}\n")
        
        for i in range(AMOUNT_ZEROES):
            new_event_lines.append(f"0\t0\t0\t{v_fft1[-AMOUNT_ZEROES+i]}\t0.0\n")
        
        event_lines = new_event_lines
        
        if not os.path.exists(folder_name_output):
            os.makedirs(folder_name_output) 
        
        with open(f"{folder_name_output}/ped_{key}_event_{event_counter}.txt", "w") as out_file:
            out_file.writelines(event_lines)

