import matplotlib.pyplot as plt
import numpy as np
import mplcursors

from data_lib import fft_filter

FILES_TO_USE = [2]# [i for i in range(1, 15)]
keys= []
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)
    
folder_name = "with_sqrt"  # This is the folder with the sqrt values

time = []
vX = []
vY = []
vSqrt = []

with open(f"./archivosGerman/datos/{folder_name}/tXYvXvY{key}.txt", "r") as values:
            lines = values.readlines()

for line in lines:
    line_values = line.split(sep='\t')
    time.append(float(line_values[0]))
    vX.append(abs(float(line_values[3])))
    vY.append(abs(float(line_values[4])))
    vSqrt.append(float(line_values[5]))

# Initial scatter plot
fig, ax = plt.subplots()

vSqrt = vSqrt[555:961]
vX = vX[555:961]


time = np.arange(len(vX))/60

vx_filtered = fft_filter(vX, fs=60, highcut=1)

ln, = ax.plot(time, vX, color='#a3a7e4', linewidth=1)  # lines instead of dots
sc = ln  # For mplcursors compatibility

# mplcursors allows clicking on points
cursor = mplcursors.cursor(sc, hover=False)



# Plot vSqrt on the same graph
ln_sqrt, = ax.plot(time, vSqrt, color='#e4a3a7', linewidth=1, label='vSqrt')
ax.legend(['vX', 'vSqrt'])



ln_filtered, = ax.plot(time, vx_filtered, color='#7ae4a3', linewidth=1, label='vX Filtered')
ax.legend(['vX', 'vSqrt', 'vX Filtered'])



pastos = []

# Keep track of modified points to avoid repeating changes
modified_indices = set()
print(f'len(time): {len(time)}')
@cursor.connect("add")
def on_click(sel):
    ind = sel.index
    print("===========================")
    print(ind)
    print("===========================\n\n\n")
    pastos.append(ind)

plt.title("Click on points to highlight them")
plt.show()

print("--"*10)
print(f"Number of clicks: {len(pastos)}")
print(f"Clicked indices: {pastos}")

rounded_pastos = [int(round(p)) for p in pastos]
print(f"Rounded indices: pastos['{key}'] = {rounded_pastos}")
