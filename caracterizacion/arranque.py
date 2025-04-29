
import plotly.graph_objects as go


FILES_TO_USE = [5] # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]


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


times_when_stopped = {}
for key in keys:
    curr_time_when_stopped = []
    last_time = None

    for i in range(len(time[key])):
        if (vX[key][i] < 0.1 and vX[key][i] > -0.1 and vY[key][i] < 0.1 and vY[key][i] > -0.1) or i == 0:
            if last_time is None or time[key][i] - last_time > 0.5:
                curr_time_when_stopped.append(time[key][i])
            last_time = time[key][i]            
    times_when_stopped[key] = curr_time_when_stopped

print(times_when_stopped)
MAX_TIME_AFTER_STOP = 5
velocities_after_stopped = {}
for key in keys:
    velocities_after_stopped[key] = []
    index_stopped = 0
    curr_time_when_stopped = times_when_stopped[key]
    last_stopped = 0
    has_recently_stopped = False
    for i in range(len(time[key])):
        curr_time = time[key][i]
        if has_recently_stopped:
            curr_vel_after_stopped.append((vX[key][i], vY[key][i], curr_time))
            
            if last_stopped + MAX_TIME_AFTER_STOP < curr_time:
                velocities_after_stopped[key].append(curr_vel_after_stopped)
                has_recently_stopped = False
                curr_vel_after_stopped = []

        if (index_stopped < len(curr_time_when_stopped) and curr_time_when_stopped[index_stopped] < curr_time):
            curr_vel_after_stopped = []
            index_stopped += 1
            has_recently_stopped = True
            last_stopped = curr_time
            
    # Para el último tiempo cuando se detuvo si no llegó a MAX_TIME_AFTER_STOP segundos
    if has_recently_stopped:
        velocities_after_stopped[key].append(curr_vel_after_stopped)

#print(velocities_after_stopped)
#for key in keys:
#    print(len(velocities_after_stopped[key]))
fig = go.Figure()
for key in keys:
    for stopped_velocities in velocities_after_stopped[key]:
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



