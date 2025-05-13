import os
import plotly.graph_objects as go

FILES_TO_USE = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
FPS = 60 # frames per second

keys= []
time = {}
vX = {}
vY = {}

for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)
    time[key] = []
    vX[key] = []
    vY[key] = []

for key in keys:
    with open(f"./datosCorregidos/tXYvXvY{key}.txt", "r") as values:
        lines = values.readlines()

    for line in lines:
        line_values = line.split(sep='\t')
        time[key].append(float(line_values[0]))
        vX[key].append(float(line_values[3]))
        vY[key].append(float(line_values[4]))


index_when_stopped = {}
for key in keys:
    curr_index_when_stopped = []
    last_time = None

    for i in range(len(time[key])):
        if (vX[key][i] < 0.1 and vX[key][i] > -0.1 and vY[key][i] < 0.1 and vY[key][i] > -0.1) or i == 0:
            if last_time is None or time[key][i] - last_time > 0.5:
                curr_index_when_stopped.append(i)
            last_time = time[key][i]            
    index_when_stopped[key] = curr_index_when_stopped


TIME_BEFORE_STOP = 3 # seconds
TICKS_BEFORE_STOP = TIME_BEFORE_STOP * FPS
velocities_before_stopped = {}
for key in keys:
    velocities_before_stopped[key] = []
    for i in index_when_stopped[key]:
        curr_data_before_stopped = []
        for j in range(i - TICKS_BEFORE_STOP, i+30):
            if j >= 0 and j < len(time[key]):
                curr_data_before_stopped.append((vX[key][j], vY[key][j], time[key][j]))
        if curr_data_before_stopped:
            velocities_before_stopped[key].append(curr_data_before_stopped)


for key in keys:
    all_fig = go.Figure()
    for index, stopped_velocities in enumerate(velocities_before_stopped[key]):
        fig = go.Figure()

        times = []
        velocities_x = []
        velocities_y = []
        for i, (vx, vy, t) in enumerate(stopped_velocities):
            times.append(t)
            velocities_x.append(vx)
            velocities_y.append(vy)
        
        fig.add_trace(go.Scatter(x=times, y=velocities_x, mode='lines', name=f'Horizontal Speed (m/s)', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=times, y=velocities_y, mode='lines', name=f'Vertical Speed (m/s)', line=dict(color='red')))
        all_fig.add_trace(go.Scatter(x=times, y=velocities_x, mode='lines', line=dict(color='blue')))
        all_fig.add_trace(go.Scatter(x=times, y=velocities_y, mode='lines', line=dict(color='red')))
        fig.update_xaxes(showgrid=False, dtick=5) 
        fig.update_yaxes(showgrid=False)
        fig.update_layout(
            xaxis_title="Time (s)",
            yaxis_title="Velocity (m/s)",
            template="plotly_white",
            showlegend=False,
        )

        os.makedirs(f"./caracterizacion/imagenes/{key}/frenados", exist_ok=True)

        # Save the figure
        fig.write_image(f"./caracterizacion/imagenes/{key}/frenados/frenado_{index}.png")

    for trace in all_fig['data']: 
        trace['showlegend'] = False

    all_fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', name='Horizontal Speed (m/s)', line=dict(color='blue')))
    all_fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', name='Vertical Speed (m/s)', line=dict(color='red')))

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

    all_fig.write_image(f"./caracterizacion/imagenes/{key}/frenados/frenado_mejores.png")