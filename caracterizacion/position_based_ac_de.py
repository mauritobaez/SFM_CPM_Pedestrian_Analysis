from lib import add_horizontal_line, add_vertical_line, get_stops_complete
import plotly.graph_objects as go


FILES_TO_USE = [i for i in range(1, 15)]
folder_name = 'NewPedestriansMovAvg_5PS_Ham'

keys= []
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)

figures = {}

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
    
    velocities = []
    
    max_speed = 0.21 if key == '12' else 0.16
    stops = get_stops_complete(max_speed, time, vX, vY)
    print(f"File {key} has {len(stops)} stops")

    #for i in range(len(time)):
    #    velocities.append(max(abs(vX[i]),abs(vY[i])))

    if key not in figures:
        figures[key] = go.Figure()   
    fig = figures[key]
    #fig.add_trace(go.Scatter(x=time, y=velocities, mode='lines', name="Hola", line=dict(color='red')))

    for stop in stops:
        add_vertical_line(fig, time[stop[0]])
        add_vertical_line(fig, time[stop[1]])
        add_horizontal_line(fig, time[stop[0]], time[stop[1]], -0.5)

    curr_index = 0
    stop_index = 0
    first_stop = stops[0][0]
    direction_vel, direction_walk = (vX, x)
    middles = []
    curr_rapidez = []
    reached_half = False
    curr_meter = x[0]
    while curr_index < len(time):
        curr_rapidez.append(abs(direction_vel[curr_index]))
        if not reached_half and 3.25 < abs(curr_meter - direction_walk[curr_index]):
            reached_half = True
            middles.append(time[curr_index])
            #print(f"Curr meter: {curr_meter}, direction_walk: {direction_walk[curr_index]}, time: {time[curr_index]}")
        if stop_index < len(stops)-1 and curr_index > stops[stop_index+1][0]:
            stop_index += 1
            direction_vel, direction_walk = (vY, y) if stop_index == 2 or stop_index == 5 else (vX, x)
            reached_half = False
            curr_meter = direction_walk[stops[stop_index][1]]
            #print(f"Curr meter: {curr_meter}, time: {time[curr_index]}")    
        curr_index += 1
        
    fig.add_trace(go.Scatter(x=time, y=curr_rapidez, mode='lines', name="Hola", line=dict(color='red')))
    for middle in middles:
        add_vertical_line(fig, middle, color='orange')
    
for key in keys:
    fig = figures[key]

    fig.update_xaxes(showgrid=False, dtick=5) 
    fig.update_yaxes(showgrid=False)
    fig.update_layout(
        title=f"Speed vs Time for {key}",
        xaxis_title="Time (s)",
        yaxis_title="Speed (m/s)",
        template="plotly_white",
        showlegend=True,
    )

    fig.show()