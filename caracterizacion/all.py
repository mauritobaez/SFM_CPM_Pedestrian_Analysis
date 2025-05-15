
import plotly.graph_objects as go


FILES_TO_USE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]


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


velocities = {}
for key in keys:
    curr_vel = []
    curr_vx = vX[key]
    curr_vy = vY[key]
    for i in len(time[key]):
        curr_vel.append(max(abs(curr_vx[i]),abs(curr_vy[i])))
    velocities[key] = curr_vel

fig = go.Figure()
for key in keys:
    for vels in velocities[key]:
        fig.add_trace(go.Scatter(x=time[key], y=vels, mode='lines', name=f'v {key}', line=dict(color='blue')))
        fig.update_xaxes(showgrid=False, dtick=5) 
        fig.update_yaxes(showgrid=False)
        

fig.update_layout(
    xaxis_title="Time (s)",
    yaxis_title="Velocity (m/s)",
    template="plotly_white",
    showlegend=False,
)

fig.show()



