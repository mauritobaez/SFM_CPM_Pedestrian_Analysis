
import plotly.graph_objects as go
import os

FILES_TO_USE = [2]# [i for i in range(1, 15)]

folders = [
    #"para_presentacion/diferenciasFinitas",
    #"diferenciasFinitasSmoothAndFilter",
    "para_presentacion/pedestrianTrajectoriesProcessed",
    #"pedestrianTrajectoriesProcessedSmoothAndFilter",
    #"stencilMovingAverage",
    #"stencilMovingAverageHampel",
    #"MovingAverageStencilHampel",
    #"newPedestriansMovAvg_5PS_Ham",
    #"fft1p5",
    #"fft1",
    #"fft0p5",
]

colors = [
    "red",
    #"blue",
    "green",
    #"orange",
    #"purple",
    #"green"
]

names = [
    #"finite differences",
    #"fd smooth and filter",
    "Velocity in X axis",
    #"5pt Savitzky-Golay + Hampel",
    #"5pt moving average",
    #"5pt moving average + Hampel",
    #"Moving Average over x and y + Hampel",
    #"Mov Avg + 5pt + Hampel",
    #"Mov Avg + 5pt + Hampel + FFT 1.5Hz",
    #"Mov Avg + 5pt + Hampel + FFT 1Hz",
    #"Mov Avg + 5pt + Hampel + FFT 0.5Hz",
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
        fig.add_trace(go.Scatter(x=time, y=vX, mode='lines', name=names[index], line=dict(color=colors[index]), opacity=1 if index == 0 else 0.8))
        fig.add_trace(go.Scatter(x=time, y=vY, mode='lines', name="Velocity in Y axis", line=dict(color="blue"), opacity=1 if index == 0 else 0.8))
        
        
for key in keys:
    fig = figures[key]

    fig.update_xaxes(showgrid=False, dtick=5) 
    fig.update_yaxes(showgrid=False)
    fig.update_layout(
        title={
            'text': f"Speed vs Time for {key}",
            'font': dict(size=28)
        },
        xaxis_title="Time (s)",
        yaxis_title="Speed (m/s)",
        template="plotly_white",
        showlegend=True,
        font=dict(size=20),
        xaxis=dict(title_font=dict(size=24), tickfont=dict(size=18)),
        yaxis=dict(title_font=dict(size=24), tickfont=dict(size=18)),
        )

    fig.show()
    #name = "multiple_fft_comparison"
    #if not os.path.exists(f"./{name}"):
    #    os.makedirs(f"./{name}")
    #fig.write_image(
    #    f"./{name}/speeds_{key}.png",
    #    width=1920,
    #    height=1080,
    #    scale=4  # Higher scale for better resolution
    #)


