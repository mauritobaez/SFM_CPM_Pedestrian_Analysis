
import plotly.graph_objects as go
import os

FILES_TO_USE = [8]# [i for i in range(1, 15)]

folders = [
    #"para_presentacion/diferenciasFinitas",
    #"only_5ps"
    #"diferenciasFinitasSmoothAndFilter",
    #"para_presentacion/pedestrianTrajectoriesProcessedSmoothAndFilter", # ESTE ES SAVGOL
    #"para_presentacion/pedestrianTrajectoriesProcessedSmoothAndFilter",
    #"stencilMovingAverage",
    #"para_presentacion/stencilMovingAverageHampel",
    #"MovingAverageStencilHampel",
    #"newPedestriansMovAvg_5PS_Ham",
    "fft1p5",
    "fft1",
    "fft0p5",
    #"with_sqrt",
    #"only_5ps",
    #"only_hampel",
]

colors = [
    "red",
    "blue",
    #"green",
    "orange",
    #"purple",
    #"green"
]

names = [
    #"finite differences",
    #"5PS",
    #"5PS + Hampel",
    #"fd smooth and filter",
    #"Velocity in X axis",
    #"5pt Savitzky-Golay + Hampel",
    #"5pt moving average",
    #"5pt moving average + Hampel",
    #"Moving Average over x and y + Hampel",
    #"Mov Avg + 5pt + Hampel",
    "FFT 1.5Hz",
    "FFT 1Hz",
    "FFT 0.5Hz",
    #"5PS",
    #"5PS + Hampel",
]

figures = {}

keys= []
for i in FILES_TO_USE:
    key = f"{i:02}"
    keys.append(key)

i = 0
# Por cada carpeta
for index, folder_name in enumerate(folders):
    # Por cada archivo
    for key in keys:
        time = []
        vX = []
        vY = []
        vSqrt = []

        #if i == 0:
        with open(f"./archivosGerman/datos/{folder_name}/tXYvXvY{key}.txt", "r") as values:
            lines = values.readlines()
        #else:
        #    with open(f"./archivosGerman/datos/{folder_name}/tXYvXvY{FILES_TO_USE[0]+1:02}.txt", "r") as values:
        #        lines = values.readlines()
        i += 1

        for line in lines:
            line_values = line.split(sep='\t')
            time.append(float(line_values[0]))
            vX.append(abs(float(line_values[3])))
            vY.append(abs(float(line_values[4])))
            #vSqrt.append(float(line_values[5]))
            

        velocities = []

        for i in range(len(time)):
            velocities.append(max(abs(vX[i]),abs(vY[i])))

        if key not in figures:
            figures[key] = go.Figure()   
        fig = figures[key]
        fig.add_trace(go.Scatter(x=time, y=velocities, mode='lines', name=names[index], line=dict(color=colors[index], width=3), opacity=0.7 if index == 0 else 0.8))
        #fig.add_trace(go.Scatter(x=time, y=vSqrt, mode='lines', name="Rapidez", line=dict(color="blue"), opacity=0.5))
        #fig.add_trace(go.Scatter(x=time, y=vY, mode='lines', name="Velocity in Y axis", line=dict(color="blue"), opacity=1 if index == 0 else 0.8))
        
        #fig.add_trace(go.Scatter(x=time, y=vSqrt, mode='lines', name="Rapidez", line=dict(color="red", width=4), opacity=1))
        #fig.add_trace(go.Scatter(x=time, y=vX, mode='lines', name="Velocity in the X axis", line=dict(color='red')))
        #fig.add_trace(go.Scatter(x=time, y=vY, mode='lines', name="Velocity in the Y axis", line=dict(color="blue")))
        
        
        
for key in keys:
    fig = figures[key]

    fig.update_xaxes(showgrid=False, dtick=5) 
    fig.update_yaxes(showgrid=False)
    fig.update_layout(
        title={
            'text': f"Speed vs Time for {key}",
            'font': dict(size=38)
        },
        xaxis_title="Time (s)",
        yaxis_title="Speed (m/s)",
        template="plotly_white",
        showlegend=True,
        font=dict(size=32),
        xaxis=dict(title_font=dict(size=32), tickfont=dict(size=26)),
        yaxis=dict(title_font=dict(size=32), tickfont=dict(size=26)),
        )

    #fig.show()
    #name = "Sqrt_Velocities_max"
    #if not os.path.exists(f"./{name}"):
    #    os.makedirs(f"./{name}")
    fig.write_image(
        f"./speeds_{key}.png",
        width=1920,
        height=1080,
        scale=4  # Higher scale for better resolution
    )


