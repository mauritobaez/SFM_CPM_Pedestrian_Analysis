
import plotly.graph_objects as go


FILES_TO_USE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


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
            last_time = time[key][i]            
    index_when_stopped[key] = curr_index_when_stopped



velocities_before_stopped = {}
for key in keys:
    velocities_before_stopped[key] = []
    for i in range(len(index_when_stopped[key])):
        if i == 0:
            continue
        curr_index = index_when_stopped[key][i]

        direction_vel, direction_walk = (vY, y) if i == 3 or i == 6 else (vX, x)
        curr_meter = direction_walk[key][curr_index]

        curr_data_before_stopped = []
        while curr_index > 0 and abs(curr_meter - direction_walk[key][curr_index]) < 4:
            curr_data_before_stopped.append((abs(direction_vel[key][curr_index]), time[key][curr_index]))
            curr_index -= 1
        if curr_data_before_stopped:
            velocities_before_stopped[key].append(curr_data_before_stopped)


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

    fig.add_trace(go.Scatter(x=time[key], y=velocities[key], mode='lines', name=f'v {key}', line=dict(color='blue')))
    fig.update_xaxes(showgrid=False, dtick=5) 
    fig.update_yaxes(showgrid=False)

    for index, stopped_velocities in enumerate(velocities_before_stopped[key]):

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
        #fig.add_shape(
        #    type="line",
        #    x0=stopped_velocities[0][1],
        #    x1=stopped_velocities[0][1],
        #    y0=min(velocities[key]),
        #    y1=max(velocities[key])+0.2,
        #    line=dict(color="red", width=3, dash="dash"),
        #    layer="below"
        #)
        #fig.add_shape(
        #    type="line",
        #    x0=stopped_velocities[-1][1],
        #    x1=stopped_velocities[-1][1],
        #    y0=min(velocities[key]),
        #    y1=max(velocities[key])+0.2,
        #    line=dict(color="red", width=3, dash="dash"),
        #    layer="below"
        #)
        

    fig.update_layout(
        xaxis_title="Time (s)",
        yaxis_title="Speed (m/s)",
        template="plotly_white",
        showlegend=False,
    )

    fig.write_image(f"./imagenes2/{key}_all_4metros_frenado.png", width=800, height=600)
    #fig.show()



