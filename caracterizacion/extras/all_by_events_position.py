import plotly.graph_objects as go


FILES_TO_USE = [3]
EVENTS_TO_USE = [i for i in range(1, 9)]
folder_name = 'by_events'

ped_keys = []
for i in FILES_TO_USE:
    key = f"{i:02}"
    ped_keys.append(key)

events_keys = []
for i in EVENTS_TO_USE:
    key = f"{i:02}"
    events_keys.append(key)


figures = {}
all_stops = {}
times = {}

for key in ped_keys:
    for event_key in events_keys:
        time = []
        v = []
        x = []
        y = []

        with open(f"./archivosGerman/{folder_name}/tXYV_ped{key}_event{event_key}.txt", "r") as values:
            lines = values.readlines()
        for line in lines:
            line_values = line.split(sep='\t')
            time.append(float(line_values[0]))
            x.append(float(line_values[1]))
            y.append(float(line_values[2]))
            v.append(float(line_values[3]))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time, y=v, mode='markers', marker=dict(color='red', size=4), opacity=0.4))
        
        fig.update_layout(title=f"Velocidades del peatón {key} en el evento {event_key}",
                          xaxis_title="Tiempo (s)",
                          yaxis_title="Velocidad (m/s)",
                          width=800,
                          height=600)
        fig.show()
    
