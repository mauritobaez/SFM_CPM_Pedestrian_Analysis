
import math
import statistics
import plotly.graph_objects as go


FILES_TO_USE = [i for i in range(0, 14)]


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


###
index_when_stopped = {}
for key in keys:
    curr_index_when_stopped = []
    last_time = None

    value_max = 0.13 if key == "11" else 0.08 # ESTO ES UNA NEGRADA

    for i in range(len(time[key])):
        if (vX[key][i] < value_max and vX[key][i] > -value_max and vY[key][i] < value_max and vY[key][i] > -value_max) or i == 0:
            if last_time is None or time[key][i] - last_time > 1:
                curr_index_when_stopped.append(i)
            else:
                curr_index_when_stopped[-1] = i
            last_time = time[key][i]            
    index_when_stopped[key] = curr_index_when_stopped

##########################################################################################

MIN_TIME_AFTER_STOP = 2
MAX_TIME_AFTER_STOP = 3
FPS = 60
TICKS_MIN_TIME_AFTER_STOP = MIN_TIME_AFTER_STOP * FPS
TICKS_MAX_TIME_AFTER_STOP = MAX_TIME_AFTER_STOP * FPS
gaussian_distibution = {}

for key in keys:
    for i in range(len(index_when_stopped[key])):
        if i == 0:
            gaussian_distibution[key] = []
        curr_index = index_when_stopped[key][i]
        curr_rapidez = []

        direction_vel, direction_walk = (vY, y) if i == 2 or i == 5 else (vX, x)

        for j in range(int(curr_index + TICKS_MIN_TIME_AFTER_STOP), int(curr_index + TICKS_MAX_TIME_AFTER_STOP)):
            if j >= 0 and j < len(time[key]):
                curr_rapidez.append(abs(direction_vel[key][j]))
        if curr_rapidez:
            mean = statistics.mean(curr_rapidez)
            std_dev = statistics.stdev(curr_rapidez) if len(curr_rapidez) > 1 else 0
            gaussian_distibution[key].append((mean, std_dev))

velocities_after_stopped = {}
for key in keys:
    velocities_after_stopped[key] = []
    for index_number_stop, i in enumerate(index_when_stopped[key]):
        curr_vel_after_stopped = []
        if index_number_stop >= len(gaussian_distibution[key]):
            break

        direction_vel, direction_walk = (vY, y) if i == index_number_stop or i == index_number_stop else (vX, x)
        curr_mean, curr_std_dev = gaussian_distibution[key][index_number_stop]
        for j in range(i, int(i+TICKS_MIN_TIME_AFTER_STOP)):
            if j < len(time[key]):
                vel_importante = abs(direction_vel[key][j])
                curr_vel_after_stopped.append((vel_importante, time[key][j]))
                
                if curr_mean - curr_std_dev > vel_importante and curr_mean + curr_std_dev < vel_importante:
                    break
        velocities_after_stopped[key].append(curr_vel_after_stopped)



############################################################################################

speeds_meters = {}

for key in keys:
    speeds_meters[key] = []
    for i in range(len(index_when_stopped[key])):
        curr_index = index_when_stopped[key][i]
        curr_rapidez = []
        direction_vel, direction_walk = (vY, y) if i == 2 or i == 5 else (vX, x)
        curr_meter = direction_walk[key][curr_index]

        while curr_index < len(time[key]) and abs(curr_meter - direction_walk[key][curr_index]) < 4:
            curr_rapidez.append((abs(direction_vel[key][curr_index]), time[key][curr_index]))
            curr_index += 1

        speeds_meters[key].append(curr_rapidez)



velocities = {}
for key in keys:
    curr_dir = 0
    curr_velocities = []
    stops = index_when_stopped[key]
    direction_vel = vX
    for i in range(len(time[key])):
        if curr_dir < len(stops) and i == stops[curr_dir]:
            curr_dir +=1
            if curr_dir == 3 or curr_dir == 6: # Es como estar contando (empezando en 1) los puntos 
                direction_vel = vY
            else:
                direction_vel = vX
        curr_velocities.append(abs(direction_vel[key][i]))
    velocities[key] = curr_velocities

###

for key in keys:    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=time[key], y=velocities[key], mode='lines', line=dict(color='blue'), showlegend=False))
    fig.update_xaxes(showgrid=False, dtick=5) 
    fig.update_yaxes(showgrid=False)

    for index, stopped_velocities in enumerate(speeds_meters[key]):

        fig.add_shape(
            type="rect",
            x0=stopped_velocities[0][1],
            x1=stopped_velocities[-1][1],
            y0=min(velocities[key]) - 0.1,  # Extend a bit below the data
            y1=max(velocities[key]) + 0.3,  # Extend a bit above the data
            fillcolor="blue",
            opacity=0.4,
            layer="below",
            line_width=0,
        )


    for index, stopped_velocities in enumerate(velocities_after_stopped[key]):

        fig.add_shape(
            type="rect",
            x0=stopped_velocities[0][1],
            x1=stopped_velocities[-1][1],
            y0=min(velocities[key]) - 0.1,  # Extend a bit below the data
            y1=max(velocities[key]) + 0.3,  # Extend a bit above the data
            fillcolor="red",
            opacity=0.4,
            layer="below",
            line_width=0,
        )


    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color='blue', opacity=0.4),
        name='Zone: only 4 meters'
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color='red', opacity=0.4),
        name='Zone: 4 meters & gaussian'
    ))

    fig.update_layout(
        xaxis_title="Time (s)",
        yaxis_title="Speed (m/s)",
        template="plotly_white",
        showlegend=True,
    )

    fig.write_image(f"./imagenes2/{key}_gauss4metros_arranque.png", width=800, height=600)
    #fig.show()


