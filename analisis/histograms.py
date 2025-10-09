

import json
import numpy as np
import plotly.graph_objects as go

# Load the data from acc_60.json
with open('analisis/acc_60.json', 'r') as f:
    data = json.load(f)

# Extract all ECM values
ecm_values = []
for ped_id, ped_data in data['pastos'].items():
    ecm_values.extend(ped_data['ecms'])

# Create histogram
fig = go.Figure()

fig.add_trace(go.Histogram(
    x=ecm_values,
    name='ECM Distribution',
    opacity=0.75,
    nbinsx=50,  # You can adjust the number of bins
    marker_color='blue'
))

# Vertical line at ECM = 0.018
fig.add_vline(x=0.018, line_width=3, line_dash="dash", line_color="red",
              annotation_text="ECM = 0.018", annotation_position="top right",
                annotation_font_size=16, annotation_font_color="red")

# Update layout
fig.update_layout(
    title="Distribution of ECM Values",
    xaxis_title="ECM Value",
    yaxis_title="Frequency",
    template="plotly_white",
    showlegend=True,
    font=dict(size=20),
    xaxis=dict(title_font=dict(size=24), tickfont=dict(size=18)),
    yaxis=dict(title_font=dict(size=24), tickfont=dict(size=18)),
)



# Show the plot
fig.show()
