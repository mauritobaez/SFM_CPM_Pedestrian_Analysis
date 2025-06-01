from lib import get_stops_complete


FILES_TO_USE = [i for i in range(1, 15)]
folder_name = 'NewPedestriansMovAvg_5PS_Ham'

keys= []
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)


for key in keys:
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
    
    stops = get_stops_complete(0.1, time, vX, vY)
    print(f"File {key} has {len(stops)} stops")
