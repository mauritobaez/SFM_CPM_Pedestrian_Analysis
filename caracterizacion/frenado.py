import plotly.graph_objects as go

FILES_TO_USE = [5] # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
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
    for i in curr_index_when_stopped:
        curr_data_before_stopped = []
        for j in range(i - TICKS_BEFORE_STOP, i+1):
            if j >= 0:
                curr_data_before_stopped.append((vX[key][j], vY[key][j], time[key][j]))
        velocities_before_stopped[key].append(curr_data_before_stopped)
            

fig = go.Figure()
for key in keys:
    for stopped_velocities in velocities_before_stopped[key]:
        times = []
        velocities_x = []
        velocities_y = []
        for i, (vx, vy, t) in enumerate(stopped_velocities):
            times.append(t)
            velocities_x.append(vx)
            velocities_y.append(vy)
        
        fig.add_trace(go.Scatter(x=times, y=velocities_x, mode='lines', name=f'vX {key}', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=times, y=velocities_y, mode='lines', name=f'vY {key}', line=dict(color='red')))
        fig.update_xaxes(showgrid=False, dtick=5) 
        fig.update_yaxes(showgrid=False)
        

fig.update_layout(
    xaxis_title="Time (s)",
    yaxis_title="Velocity (m/s)",
    template="plotly_white",
    showlegend=False,
)

fig.show()
