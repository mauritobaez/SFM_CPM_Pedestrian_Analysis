import matplotlib.pyplot as plt
import numpy as np
import mplcursors

FILES_TO_USE = [5]# [i for i in range(1, 15)]
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
