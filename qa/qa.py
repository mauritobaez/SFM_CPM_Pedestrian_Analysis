import matplotlib.pyplot as plt
import math

keys= []
time = {}
x = {}
y = {}
vX = {}
vY = {}

for i in range(0, 14):
    key = f"{i:02}"
    keys.append(key)
    time[key] = []
    x[key] = []
    y[key] = []
    vX[key] = []
    vY[key] = []

for key in keys:
    with open(f"../../datosCorregidos/tXYvXvY{key}.txt", "r") as values:
        lines = values.readlines()

    for line in lines:
        line_values = line.split(sep='\t')
        time[key].append(float(line_values[0]))
        x[key].append(float(line_values[1]))
        y[key].append(float(line_values[2]))
        vX[key].append(float(line_values[3]))
        vY[key].append(float(line_values[4]))

key = "03"

#for key in time.keys():
#    closest_x_to_zero = min(vX[key], key=lambda x: abs(x))
#    closest_y_to_zero = min(vY[key], key=lambda y: abs(y))
#    print(f"Valor más cercano a 0 en x: {closest_x_to_zero}")
#    print(f"Valor más cercano a 0 en y: {closest_y_to_zero}")
#    min_x = min(vX[key])
#    max_x = max(vX[key])
#    min_y = min(vY[key])
#    max_y = max(vY[key])
#    print(f"Minimo vX: {min_x}")
#    print(f"Maximo vX: {max_x}")
#    print(f"Minimo vY: {min_y}")
#    print(f"Maximo vY: {max_y}")

for key in time.keys():

    x_when_stopped = []
    y_when_stopped = []
    prev_x = None
    prev_y = None

    for i in range(len(time[key])):
        if (vX[key][i] < 0.1 and vX[key][i] > -0.1 and vY[key][i] < 0.1 and vY[key][i] > -0.1) or i == 0:
            if prev_x is None or abs(prev_x - x[key][i]) > 0.1 or prev_y is None or abs(prev_y - y[key][i]) > 0.1:
                x_when_stopped.append(x[key][i])
                y_when_stopped.append(y[key][i])
            prev_x = x[key][i]
            prev_y = y[key][i]

    print(f"Key: {key}")
    print(x_when_stopped)
    print(y_when_stopped)
    for i in range(len(x_when_stopped)-1):
        print(f"Distance between {i} and {i+1}: {math.sqrt((x_when_stopped[i] - x_when_stopped[i+1])**2 + (y_when_stopped[i] - y_when_stopped[i+1])**2)}")

    for i in range(0, len(x_when_stopped)-1, 3):
        if i+2 < len(x_when_stopped):
            print(f"Distance between {i} and {i+2}: {math.sqrt((x_when_stopped[i] - x_when_stopped[i+2])**2 + (y_when_stopped[i] - y_when_stopped[i+2])**2)}")
    
    print(f"Distance between {0} and {6}: {math.sqrt((x_when_stopped[0] - x_when_stopped[6])**2 + (y_when_stopped[0] - y_when_stopped[6])**2)}")
    print(f"Distance between {1} and {7}: {math.sqrt((x_when_stopped[1] - x_when_stopped[7])**2 + (y_when_stopped[1] - y_when_stopped[7])**2)}")
    if len(x_when_stopped) > 8:
        print(f"Distance between {2} and {8}: {math.sqrt((x_when_stopped[2] - x_when_stopped[8])**2 + (y_when_stopped[2] - y_when_stopped[8])**2)}")

#
#
#x1 = {}
#x2 = {}
#x3 = {}
#for key_min_max in time.keys():
#    x1[key_min_max] = []
#    x2[key_min_max] = []
#    x3[key_min_max] = []
#    for i in range(len(time[key_min_max])):
#        if time[key_min_max][i] < 20:
#            x1[key_min_max].append(x[key_min_max][i])
#        elif time[key_min_max][i] < 40:
#            x2[key_min_max].append(x[key_min_max][i])
#        else:
#            x3[key_min_max].append(x[key_min_max][i])
#    
#    print(f"{key_min_max}:")
#    print(f"Tiempo 0-20: Max={max(x1[key_min_max])} Min={min(x1[key_min_max])}")
#    print(f"Tiempo 20-40: Max={max(x2[key_min_max])} Min={min(x2[key_min_max])}")
#    print(f"Tiempo 40-60: Max={max(x3[key_min_max])} Min={min(x3[key_min_max])}")

# Graficar los datos
# Plot min and max values for each time range
#plt.figure(figsize=(10, 6))
#plt.title("Min and Max Values for Each Time Range")
#plt.xlabel("Time Range")
#for key_min_max in keys:  
#    # Plot for time range 0-20
#    plt.axhline(y=max(x1[key_min_max]), color='blue', linestyle='--', label=f"Max 0-20 ({max(x1[key_min_max]):.2f})")
#    plt.axhline(y=min(x1[key_min_max]), color='cyan', linestyle='--', label=f"Min 0-20 ({min(x1[key_min_max]):.2f})")
#    
#    # Plot for time range 20-40
#    plt.axhline(y=max(x2[key_min_max]), color='green', linestyle='--', label=f"Max 20-40 ({max(x2[key_min_max]):.2f})")
#    plt.axhline(y=min(x2[key_min_max]), color='lime', linestyle='--', label=f"Min 20-40 ({min(x2[key_min_max]):.2f})")
#    
#    # Plot for time range 40-60
#    plt.axhline(y=max(x3[key_min_max]), color='red', linestyle='--', label=f"Max 40-60 ({max(x3[key_min_max]):.2f})")
#    plt.axhline(y=min(x3[key_min_max]), color='orange', linestyle='--', label=f"Min 40-60 ({min(x3[key_min_max]):.2f})")
#    
#plt.ylabel("X Values")
#plt.xticks([1, 2, 3], ["0-20", "20-40", "40-60"])
#plt.grid()
#plt.show()

#plt.plot(time[key], x[key], label="x")
#plt.plot(time[key], y[key], label="y")
#plt.plot(time[key], vX[key], label="vX")
#plt.plot(time[key], vY[key], label="vY")
#plt.legend()
#plt.grid()
#plt.title("Datos de la simulación")
#plt.show()

