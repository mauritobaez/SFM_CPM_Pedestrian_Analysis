
import plotly.graph_objects as go
import math
import statistics

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
index_when_stopped = {}
for key in keys:
    curr_time_when_stopped = []
    curr_index_when_stopped = []
    last_time = None

    for i in range(len(time[key])):
        if (vX[key][i] < 0.1 and vX[key][i] > -0.1 and vY[key][i] < 0.1 and vY[key][i] > -0.1) or i == 0:
            if last_time is None or time[key][i] - last_time > 0.5:
                curr_time_when_stopped.append(time[key][i])
                curr_index_when_stopped.append(i)
            last_time = time[key][i]            
    times_when_stopped[key] = curr_time_when_stopped
    index_when_stopped[key] = curr_index_when_stopped

print(times_when_stopped)
MIN_TIME_AFTER_STOP = 2.5
MAX_TIME_AFTER_STOP = 4.5
FPS = 60
TICKS_MIN_TIME_AFTER_STOP = MIN_TIME_AFTER_STOP * FPS
TICKS_MAX_TIME_AFTER_STOP = MAX_TIME_AFTER_STOP * FPS
gaussian_distibution = {}

for key in keys:
    for i in range(len(times_when_stopped[key])):
        if i == 0:
            gaussian_distibution[key] = []
        curr_time = times_when_stopped[key][i]
        curr_index = index_when_stopped[key][i]
        curr_rapidez = []
        for j in range(curr_index + TICKS_MIN_TIME_AFTER_STOP, curr_index + TICKS_MAX_TIME_AFTER_STOP):
            if j >= 0 and j < len(time[key]):
                curr_rapidez.append(math.sqrt(vX[key][j]**2, vY[key][j]**2))
        if curr_rapidez:
            mean = statistics.mean(curr_rapidez)
            std_dev = statistics.stdev(curr_rapidez) if len(curr_rapidez) > 1 else 0
            gaussian_distibution[key].append((mean, std_dev))

velocities_after_stopped = {}
for key in keys:
    velocities_after_stopped[key] = []
    for i in index_when_stopped:
        curr_vel_after_stopped = []
        curr_mean, curr_std_dev = gaussian_distibution[key][i]
        for j in range(i, i+TICKS_MIN_TIME_AFTER_STOP):
            if j < len(time[key]):
                curr_vel_after_stopped.append((vX[key][j], vY[key][j], time[key][j]))
                curr_rapidez = math.sqrt(vX[key][j]**2 + vY[key][j]**2)
                if curr_mean - curr_std_dev > curr_rapidez and curr_mean + curr_std_dev < curr_rapidez:
                    exit
        velocities_after_stopped[key].append(curr_vel_after_stopped)
               

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



