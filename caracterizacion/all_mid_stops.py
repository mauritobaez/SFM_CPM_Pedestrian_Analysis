from lib import add_horizontal_line, add_vertical_line, gaussian, get_all_values, get_between_indexes, get_stops_complete
import plotly.graph_objects as go
import os

FILES_TO_USE = [i for i in range(1, 15)]
folder_name = 'fft1p5'

keys= []
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)

figures = {}
all_stops = {}
times = {}

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
    times[key] = time
    velocities = []
    
    max_speed = 0.23 if key == '12' else 0.18 if key == '14' else 0.16
    stops = get_stops_complete(max_speed, time, vX, vY)

    velocities = get_all_values(time, vX, vY, stops)
    
    for i in range(0, len(stops), 2):
        if i + 2 >= len(stops):
            break
        fig = go.Figure()
        first = stops[i][0]
        last = stops[i+2][1]
        curr_vel = get_between_indexes(first, last, velocities)
        fig.add_trace(go.Scatter(
            x=time[first:last+1],
            y=curr_vel,
            mode='lines',
            line=dict(color='blue', width=2)
        ))
        fig.update_xaxes(showgrid=False, dtick=5) 
        fig.update_yaxes(showgrid=False)
        fig.update_layout(
            title=f"Velocidad {key} {i//2 + 1}",
            xaxis_title="Time (s)",
            yaxis_title="Speed (m/s)",
            template="plotly_white",
            showlegend=False,
        )

        name = "fft_tramos"
        if not os.path.exists(f"./{name}"):
            os.makedirs(f"./{name}")
        fig.write_image(
            f"./{name}/speeds_{key}_{i//2+1}.png",
            width=1920,
            height=1080,
            scale=4  # Higher scale for better resolution
        )
        #fig.show()
