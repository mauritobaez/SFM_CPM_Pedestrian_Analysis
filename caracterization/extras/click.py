import matplotlib.pyplot as plt
import numpy as np
import mplcursors

from data_lib import fft_filter

key = "14"
    
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

ln, = ax.plot(time, vSqrt, color='#a3a7e4', linewidth=1)  # lines instead of dots
sc = ln  # For mplcursors compatibility

# mplcursors allows clicking on points
cursor = mplcursors.cursor(sc, hover=False)

pastos = []

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

# Group clicks into pairs
rounded_pastos = [int(round(p)) for p in pastos]
paired_pastos = [rounded_pastos[i:i+2] for i in range(0, len(rounded_pastos), 2)]
print(f"Paired indices: pastos['{key}'] = {paired_pastos}")
