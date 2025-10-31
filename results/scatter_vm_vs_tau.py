import json
import plotly.graph_objects as go
import numpy as np

file_name = 'acc_60_I2T'

# Read the JSON file
with open(f'./analisis/{file_name}.json', 'r') as f:
    data = json.load(f)

x_axis = 'taus'
y_axis = 'ecms'

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
    x_values = ped_data[x_axis]
    y_values = ped_data[y_axis]
    doubles = ped_data.get('doubles', [])
    
    for double in doubles:
        double[-1] 
    
    # Create a scatter trace for each pedestrian
    trace = go.Scatter(
        x=x_values,
        y=y_values,
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
    title=f'{y_axis} vs {x_axis} by Pedestrian',
    xaxis_title=f'{x_axis} (s)',
    yaxis_title=f'{y_axis} (m/s)',
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
fig.write_html(f"results/{file_name}_{x_axis}_{y_axis}.html")

# Show the plot (optional if you're running this in a notebook or interactive environment)
#fig.show()