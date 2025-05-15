
import plotly.graph_objects as go
import os

FILES_TO_USE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
FPS = 60

keys= []
time = {}
vX = {}
vY = {}
x = {}
y = {}

for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)
    time[key] = []
    vX[key] = []
    vY[key] = []
    x[key] = []
    y[key] = []

for key in keys:
    with open(f"./datosCorregidos/tXYvXvY{key}.txt", "r") as values:
        lines = values.readlines()

    for line in lines:
        line_values = line.split(sep='\t')
        time[key].append(float(line_values[0]))
        x[key].append(float(line_values[1]))
        y[key].append(float(line_values[2]))
        vX[key].append(float(line_values[3]))
        vY[key].append(float(line_values[4]))


index_when_stopped = {}
for key in keys:
    curr_index_when_stopped = []
    last_time = None

    for i in range(len(time[key])):
        if (vX[key][i] < 0.08 and vX[key][i] > -0.08 and vY[key][i] < 0.08 and vY[key][i] > -0.08) or i == 0:
            if last_time is None or time[key][i] - last_time > 0.5:
                curr_index_when_stopped.append(i)
            else:
                curr_index_when_stopped[-1] = i
            last_time = time[key][i]            
    index_when_stopped[key] = curr_index_when_stopped



speed = {}

for key in keys:
    for i in range(len(index_when_stopped[key])):
        curr_index = index_when_stopped[key][i]
        curr_rapidez = []
        direction_vel, direction_walk = vY, y if i == 2 or i == 5 else vX, x
        curr_meter = direction_walk[key][curr_index]

        while curr_index < len(time[key]) and abs(curr_meter - direction_walk[key][curr_index]) < 4:
            curr_rapidez.append(abs(direction_vel[key][curr_index]))
            curr_index += 1

        speed[key] = curr_rapidez

               
for key in keys:
    all_fig = go.Figure()
    for index, stopped_velocities in enumerate(speed[key]):
        fig = go.Figure()

        times = []
        velocities = []
        
        for i, (v, t) in enumerate(stopped_velocities):
            times.append(t)
            velocities.append(v)
        
        fig.add_trace(go.Scatter(x=times, y=velocities, mode='lines', name=f'Speed (m/s)', line=dict(color='blue')))
        all_fig.add_trace(go.Scatter(x=times, y=velocities, mode='lines', line=dict(color='blue')))
        fig.update_xaxes(showgrid=False, dtick=5) 
        fig.update_yaxes(showgrid=False)
        fig.update_layout(
            xaxis_title="Time (s)",
            yaxis_title="Velocity (m/s)",
            template="plotly_white",
            showlegend=False,
        )

        os.makedirs(f"./caracterizacion/imagenes/{key}/arranques", exist_ok=True)

        # Save the figure
        fig.write_image(f"./caracterizacion/imagenes/{key}/arranques/arranque_gaussiano_{index}.png")

    for trace in all_fig['data']: 
        trace['showlegend'] = False

    all_fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', name='Speed (m/s)', line=dict(color='blue')))

    all_fig.update_layout(
        xaxis_title="Time (s)",
        yaxis_title="Velocity (m/s)",
        template="plotly_white",
        showlegend=True,
        legend=dict(
            itemsizing='constant',
            title="Legend",
            font=dict(size=9),
        )
    )

    all_fig.write_image(f"./caracterizacion/imagenes/{key}/arranques/arranque_gaussiano_mejores.png")



