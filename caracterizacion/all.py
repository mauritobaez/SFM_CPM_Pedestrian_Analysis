
import plotly.graph_objects as go


FILES_TO_USE = [i for i in range(0, 14)]

folders = [
    #"diferenciasFinitas",
    #"diferenciasFinitasSmoothAndFilter",
    #"pedestrianTrajectoriesProcessed",
    #"pedestrianTrajectoriesProcessedSmoothAndFilter",
    #"stencilMovingAverage",
    "stencilMovingAverageHampel",
    "MovingAverageStencilHampel"
]

colors = [
    #"red",
    "blue",
    #"green",
    #"orange",
    #"purple",
    "green"
]

names = [
    #"finite difference",
    #"fd smooth and filter",
    #"5 point stencil",
    #"5pt Savitzky-Golay + Hampel",
    #"5pt moving average",
    "5pt moving average + Hampel",
    "Moving Average over x and y + Hampel"
]

figures = {}

keys= []
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)

# Por cada carpeta
for index, folder_name in enumerate(folders):
    # Por cada archivo
    for key in keys:
        time = []
        vX = []
        vY = []

        with open(f"./archivosGerman/{folder_name}/tXYvXvY{key}.txt", "r") as values:
            lines = values.readlines()

        for line in lines:
            line_values = line.split(sep='\t')
            time.append(float(line_values[0]))
            vX.append(float(line_values[3]))
            vY.append(float(line_values[4]))

        velocities = []

        for i in range(len(time)):
            velocities.append(max(abs(vX[i]),abs(vY[i])))

        if key not in figures:
            figures[key] = go.Figure()   
        fig = figures[key]
        fig.add_trace(go.Scatter(x=time, y=velocities, mode='lines', name=names[index], line=dict(color=colors[index]), opacity=1 if index == 0 else 0.5))
        
        
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
    #fig.write_image(
    #    f"./smoothing_compared/speed_comparison_{key}.png",
    #    width=1920,
    #    height=1080,
    #    scale=4  # Higher scale for better resolution
    #)


