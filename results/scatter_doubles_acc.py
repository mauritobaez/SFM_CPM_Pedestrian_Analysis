import json
import plotly.graph_objects as go

file_name = 'acc_60_I2T'

# Read the JSON file
with open(f'./analisis/{file_name}.json', 'r') as f:
    data = json.load(f)

# Create lists to store the data for each pedestrian
traces = []

# Create a color list for different pedestrians
colors = [
    '#2ca02c', '#d62728'
]

# Process data for each pedestrian
for i, (ped_id, ped_data) in enumerate(data['pastos'].items()):
    x_values = ped_data['taus']
    y_values = ped_data['ecms']
    
    # Create a scatter trace for each pedestrian
    trace = go.Scatter(
        x=x_values,
        y=y_values,
        mode='markers',
        name=f'Pedestrian {ped_id}',
        marker=dict(
            size=10,
            color=colors[1],
            symbol='circle'
        )
    )
    traces.append(trace)
    
    doubles = [double['best_error'] for double in ped_data.get('doubles', []).values()]
    trace = go.Scatter(
        x=x_values,
        y=y_values,
        mode='markers',
        name=f'Pedestrian {ped_id}',
        marker=dict(
            size=10,
            color=colors[0],
            symbol='square'
        )
    )
    traces.append(trace)
    

# Create the figure
fig = go.Figure(data=traces)

# Update layout
fig.update_layout(
    title=f'ecm vs tau by Pedestrian',
    xaxis_title=f'tau (s)',
    yaxis_title=f'ecm',
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
#fig.update_xaxes(type="log")
fig.update_yaxes(type="log")
# Save the plot as HTML
fig.write_html(f"results/{file_name}_double_ecms_change.html")

# Show the plot (optional if you're running this in a notebook or interactive environment)
#fig.show()