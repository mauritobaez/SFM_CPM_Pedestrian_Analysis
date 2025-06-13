
import plotly.graph_objects as go
from lib import add_vertical_line, get_all_values_and_positions, get_middles, get_stops_complete
from regression import double_linear_regression
import os

FILES_TO_USE = [14]
folder_name = 'fft0p5'

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
    
    max_speed = 0.21 if key == '12' else 0.193 if key == '4' else 0.16
    stops = get_stops_complete(max_speed, time, vX, vY)
    
    #stops = []
    #stops.append(get_stops_complete(max_speed, time, vX, vY)[0])
    
    #print(f"File {key} has {len(stops)} stops")

    #for i in range(len(time)):
    #    velocities.append(max(abs(vX[i]),abs(vY[i])))

    if key not in figures:
        figures[key] = go.Figure()   
    fig = figures[key]

    velocities, positions = get_all_values_and_positions(time, vX, vY, x, y, stops)
    fig.add_trace(go.Scatter(x=time, y=velocities, mode='lines', line=dict(color='red'), opacity=0.4, showlegend=False))
    
    middles = get_middles(positions, stops)
    #middles = []
    #middles.append(get_middles(positions, stops)[0])
    
    dea_begginings = []
    for i in range(min(len(stops)-1, len(middles))):
        mid = middles[i]
        beg_next_stop = stops[i+1][0]
        add_vertical_line(fig, time[beg_next_stop], color='orange', width=2, showlegend=False, legend='Start of Stop')
        best_index, first_c, second_c = double_linear_regression(velocities, time, mid, beg_next_stop)
        dea_begginings.append((best_index, first_c, second_c))
        print(f"message {i}")
    fig.add_trace(go.Scatter(x=[None], y=[None],mode='lines',line=dict(color='orange', dash='dash', width=3),name='Start of Stop',showlegend=True))


    for index, first_c, second_c in dea_begginings:
        print(f"First c: {first_c}, Second c: {second_c}, Index: {index}")
        if first_c is None:
            continue
        add_vertical_line(fig, time[index], color='green', width=2, showlegend=False, legend='Deaceleration Start')
    fig.add_trace(go.Scatter(x=[None], y=[None],mode='lines',line=dict(color='green', dash='dash', width=3),name='Deaceleration Start',showlegend=True))

        
    for i, mid in enumerate(middles):
        if i >= len(dea_begginings):
            break
        best_i, first_c, _ = dea_begginings[i]
        add_vertical_line(fig, time[mid], color='blue', width=2)
        start_time = time[mid]
        start_velocity = velocities[mid]
        trace_times = time[mid:min(mid+120, best_i)]
        trace_velocities = [start_velocity + first_c * (t - start_time) for t in trace_times]
        fig.add_trace(go.Scatter(x=trace_times, y=trace_velocities, mode='lines', line=dict(color='purple', dash='dash', width=3), showlegend=False))
    fig.add_trace(go.Scatter(x=[None], y=[None],mode='lines',line=dict(color='blue', dash='dash', width=3),name='Middle',showlegend=True))


    for index, _, second_c in dea_begginings:
        start_time = time[index]
        start_velocity = velocities[index]
        trace_times = time[index:index+60]
        trace_velocities = [start_velocity + second_c * (t - start_time) for t in trace_times]
        fig.add_trace(go.Scatter(x=trace_times, y=trace_velocities, mode='lines', line=dict(color='purple', dash='dash', width=3), showlegend=False))
    
    # For the legend!
    fig.add_trace(go.Scatter(x=[None], y=[None],mode='lines',line=dict(color='purple', dash='dash', width=3),name='Regression Lines',showlegend=True))

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
    name = "deaceleration_criteria"
    if not os.path.exists(f"./{name}"):
        os.makedirs(f"./{name}")
    fig.write_image(
        f"./{name}/speeds_{key}.png",
        width=1920,
        height=1080,
        scale=4  # Higher scale for better resolution
    )
    print(f"Saved figure for {key}")
