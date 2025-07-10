
import plotly.graph_objects as go
from lib import add_vertical_line, get_all_events, get_all_values_and_positions, get_avg_speeds_around_positions, get_middles, get_reduced_stops, get_stops_complete
from regression import double_linear_regression
import os

FILES_TO_USE = [4]  # Use all files from 01 to 14
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
    
    max_speed = 0.38 if key == '12' or key == '14' else 0.2 if key == '04' else 0.18 if key == '13' else 0.16
    stops = get_stops_complete(max_speed, time, vX, vY)
    
    events = get_all_events(time, vX, vY, stops)

    for i, event in enumerate(events):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time, y=event, mode='markers', marker=dict(color='red', size=4), opacity=0.8, showlegend=False))
        
        fig.update_xaxes(showgrid=False, dtick=5) 
        fig.update_yaxes(showgrid=False)
        fig.update_layout(
            title=f"Speed vs Time for {key}: Event {i+1}",
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
        name = "by_events"
        if not os.path.exists(f"./{name}"):
            os.makedirs(f"./{name}")
        fig.write_image(
            f"./{name}/speeds_{key}_{(i+1):02}.png",
            width=1920,
            height=1080,
            scale=4  # Higher scale for better resolution
        )


