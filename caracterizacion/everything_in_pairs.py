
import plotly.graph_objects as go
from lib import add_vertical_line, get_all_values_and_positions, get_avg_speeds_around_positions, get_middles, get_reduced_stops, get_stops_complete
from regression import double_linear_regression
import os

FILES_TO_USE = [3]  
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
    
    max_speed = 0.38 if key == '12' or key == '14' else 0.193 if key == '04' else 0.18 if key == '13' else 0.16
    stops = get_stops_complete(max_speed, time, vX, vY)
    

    if key not in figures:
        figures[key] = go.Figure()   
    fig = figures[key]

    velocities, positions = get_all_values_and_positions(time, vX, vY, x, y, stops)
    fig.add_trace(go.Scatter(x=time, y=velocities, mode='markers', marker=dict(color='red', size=4), opacity=0.4, showlegend=False))  
    stops = get_reduced_stops(stops, velocities)
    all_stops[key] = stops

    middles = get_middles(positions, stops)
    #middles = []
    #middles.append(get_middles(positions, stops)[0])

        
    dea_begginings = []
    for i in range(min(len(stops)-1, len(middles))):
        mid = middles[i]
        beg_next_stop = stops[i+1][0]
        best_time, first_c, second_c, first_b, second_b = double_linear_regression(velocities, time, mid, beg_next_stop)
        dea_begginings.append((best_time, first_c, second_c, first_b, second_b))
        #print(f"message {i}")

    for curr_stop in stops:
        add_vertical_line(fig, time[curr_stop[0]], color='orange', width=5, showlegend=False, legend='Start of Stop')
        add_vertical_line(fig, time[curr_stop[1]], color='blue', width=5, showlegend=False)
    fig.add_trace(go.Scatter(x=[None], y=[None],mode='lines',line=dict(color='orange', dash='dash', width=3),name='Start of Stop',showlegend=True))
    fig.add_trace(go.Scatter(x=[None], y=[None],mode='lines',line=dict(color='blue', dash='dash', width=3),name='End of Stop',showlegend=True))
    

    for best_time, first_c, second_c, first_b, second_b in dea_begginings:
        #print(f"First c: {first_c}, Second c: {second_c}, Index: {best_time}, first b: {first_b}, second b: {second_b}")
        if first_c is None:
            continue
        add_vertical_line(fig, best_time, color='green', width=5, showlegend=False, legend='Deaceleration Start')

    fig.add_trace(go.Scatter(x=[None], y=[None],mode='lines',line=dict(color='green', dash='dash', width=3),name='Deaceleration Start',showlegend=True))
    fig.add_trace(go.Scatter(x=[None], y=[None],mode='lines',line=dict(color='black', dash='dash', width=3),name='Middle',showlegend=True))


    for i, mid in enumerate(middles):
        if i >= len(dea_begginings):
            break
        add_vertical_line(fig, time[mid], color='black', width=5)

    # Velocidad alrededor del middle
    avg_speeds = get_avg_speeds_around_positions(positions_index=middles, x=x, meters_around=0.5)
    for avg_spd, mid in zip(avg_speeds, middles):
        fig.add_annotation(x=mid,y=avg_spd+0.2,text=f"{avg_spd:.2f}",font=dict(size=18, color="purple"),ax=0,ay=-40,bgcolor="rgba(255,255,255,0.7)",bordercolor="purple")
    fig.add_trace(go.Scatter(x=[None], y=[None],mode='lines',line=dict(color='purple', dash='dash', width=3),name='Average speed (near middle)',showlegend=True))

    # Checking if start deaceleration is 70% or less below avg_speed
    for i, (best_time, _, _, _, _) in enumerate(dea_begginings):
        mid_avg_spd = avg_speeds[i]
        if velocities[int(best_time*60)] < mid_avg_spd * 0.7:
            fig.add_annotation(x=best_time,y=velocities[int(best_time*60)]+0.2,text=f"*",font=dict(size=24, color="yellow"),ax=0,ay=-40,bgcolor="rgba(255,255,255,0.7)",bordercolor="red")


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

    #fig.show()
    name = "all_criteria_together"
    if not os.path.exists(f"./{name}"):
        os.makedirs(f"./{name}")
    fig.write_image(
        f"./{name}/speeds_{key}.png",
        width=1920,
        height=1080,
        scale=4  # Higher scale for better resolution
    )
    print(f"Saved figure for {key}")

for key in keys:
    fig = figures[key]
    stops = all_stops[key]
    time = times[key]

    # Divide each fig into 4 figures, each from stops[i][0] to stops[i+2][1]
    for i in range(0, len(stops), 2):
        if i + 2 >= len(stops):
            break
        first = stops[i][0]
        last = stops[i+2][1]
        
        fig.update_layout(
            title=f"Speed vs Time for {key} (Stop {i} to {i+2})",
            xaxis_title="Time (s)",
            yaxis_title="Speed (m/s)",
            template="plotly_white",
            showlegend=True,
            font=dict(size=24),
            title_font=dict(size=28),
            xaxis=dict(title_font=dict(size=24), tickfont=dict(size=20)),
            yaxis=dict(title_font=dict(size=24), tickfont=dict(size=20)),
            legend=dict(font=dict(size=20))
        )
        fig.update_xaxes(range=[time[first], time[last]])
        #fig.show()
        name = "all_criteria_together"
        if not os.path.exists(f"./{name}"):
            os.makedirs(f"./{name}")
        fig.write_image(
            f"./{name}/speeds_{key}_{i}.png",
            width=1920,
            height=1080,
            scale=4  # Higher scale for better resolution
        )

