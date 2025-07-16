import matplotlib.pyplot as plt


FILES_TO_USE = [6]# [i for i in range(1, 15)]
keys= []
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)
    
folder_name = "with_sqrt"  # This is the folder with the sqrt values

time = []
vX = []
vY = []
vSqrt = []

with open(f"./archivosGerman/{folder_name}/tXYvXvY{key}.txt", "r") as values:
            lines = values.readlines()
            

pastos = [483, 691, 1094, 1243, 1629, 1654, 2026, 2043, 2394, 2412, 2865, 2893, 3263, 3327, 3727]


# Se puede usar pastos + [len(lines)]
start_idx = 0
for i in range(1, len(pastos)+1, 2):
    end_idx = pastos[i] if i != len(pastos) else pastos[-1]
    event_lines = lines[start_idx:end_idx+1]
    with open(f"events_by_ped/ped_04_event_{i//2 + 1}.txt", "w") as out_file:
        out_file.writelines(event_lines)
    start_idx = pastos[i-1]


