from lib import add_horizontal_line, add_vertical_line, gaussian, get_stops_complete
import plotly.graph_objects as go


FILES_TO_USE = [i for i in range(1, 15)]
folder_name = 'NewPedestriansMovAvg_5PS_Ham'

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
    
    max_speed = 0.21 if key == '12' else 0.16
    stops = get_stops_complete(max_speed, time, vX, vY)
    #print(f"File {key} has {len(stops)} stops")

    #for i in range(len(time)):
    #    velocities.append(max(abs(vX[i]),abs(vY[i])))

    if key not in figures:
        figures[key] = go.Figure()   
    fig = figures[key]
    #fig.add_trace(go.Scatter(x=time, y=velocities, mode='lines', name="Hola", line=dict(color='red')))

    for stop in stops:
        add_vertical_line(fig, time[stop[0]])
        add_vertical_line(fig, time[stop[1]])
        add_horizontal_line(fig, time[stop[0]], time[stop[1]], -0.25, width=3)


    # TODO: Pasar esto a lib.py
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
        
    fig.add_trace(go.Scatter(x=time, y=curr_rapidez, mode='lines', line=dict(color='red'), showlegend=False))

    for middle in middles:
        add_vertical_line(fig, middle, color='orange')

    # Ahora el gaussiano
    end_of_gaussian = gaussian(stops, time, vX, vY)
    #print(end_of_gaussian)
    for index, end in enumerate(end_of_gaussian):
        add_vertical_line(fig, time[stops[index][1]], color='green')
        add_vertical_line(fig, end, color='green')
        add_horizontal_line(fig, time[stops[index][1]], end, 2, color='green', width=3)

    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='green', dash='dash'),
        name='Gaussian Acceleration'
    ))
    
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='blue', dash='dash'),
        name='Stop period'
    ))

    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='orange', dash='dash'),
        name='Separation Acc and Dec'
    ))

    all_stops[key] = stops
    
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
        font=dict(size=24),  # Increase font size
        title_font=dict(size=28),  # Increase title font size
        xaxis=dict(title_font=dict(size=24), tickfont=dict(size=20)),
        yaxis=dict(title_font=dict(size=24), tickfont=dict(size=20)),
        legend=dict(font=dict(size=20))
    )
    #fig.update_xaxes(range=[times[key][all_stops[key][1][0]], times[key][all_stops[key][4][1]]])

    #fig.show()
    fig.write_image(
        f"./all_images/acceleration_criteria/speeds_{key}.png",
        width=1920,
        height=1080,
        scale=4  # Higher scale for better resolution
    )