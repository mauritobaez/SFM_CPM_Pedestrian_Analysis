import json
import plotly.graph_objects as go
import numpy as np

# Read the JSON file
with open('./analisis/acc_60_I2T.json', 'r') as f:
    data = json.load(f)

# Create lists to store the data for each pedestrian
traces = []

# Create a color list for different pedestrians
colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896'
]

# Process data for each pedestrian
for i, (ped_id, ped_data) in enumerate(data['pastos'].items()):
    taus = ped_data['taus']
    vds = ped_data['vds']
    
    # Create a scatter trace for each pedestrian
    trace = go.Scatter(
        x=taus,
        y=vds,
        mode='markers',
        name=f'Pedestrian {ped_id}',
        marker=dict(
            size=10,
            color=colors[i % len(colors)],
            symbol='circle'
        )
    )
    traces.append(trace)

# Create the figure
fig = go.Figure(data=traces)

# Update layout
fig.update_layout(
    title='Desired Velocity vs Tau by Pedestrian',
    xaxis_title='τ (s)',
    yaxis_title='Desired Velocity (m/s)',
    font=dict(size=14),
    showlegend=True,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99
    ),
    plot_bgcolor='white'
)

# Update axes
fig.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='LightGray',
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor='LightGray'
)

fig.update_yaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='LightGray',
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor='LightGray'
)

# Save the plot as HTML
fig.write_html("scatter_vm_vs_tau.html")

# Show the plot (optional if you're running this in a notebook or interactive environment)
#fig.show()