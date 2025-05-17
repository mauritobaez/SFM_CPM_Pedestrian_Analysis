
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


velocities = {}
for key in keys:
    curr_vel = []
    curr_vx = vX[key]
    curr_vy = vY[key]
    for i in range(len(time[key])):
        curr_vel.append(max(abs(curr_vx[i]),abs(curr_vy[i])))
    velocities[key] = curr_vel


for key in keys:    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=time[key], y=velocities[key], mode='lines', name=f'v {key}', line=dict(color='blue')))
    fig.update_xaxes(showgrid=False, dtick=5) 
    fig.update_yaxes(showgrid=False)
        

    fig.update_layout(
        title=f"Velocity vs Time for {key}",
        xaxis_title="Time (s)",
        yaxis_title="Velocity (m/s)",
        template="plotly_white",
        showlegend=False,
    )

    fig.show()



