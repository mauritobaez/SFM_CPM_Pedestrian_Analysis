

import json
import numpy as np
import plotly.graph_objects as go

# Load the data from acc_60.json
name = 'analisis/acc_60_04'
with open(f'{name}.json', 'r') as f:
    data = json.load(f)

# Extract all ECM values
ecm_values = []
ecm_values_for_avg = []
ecm_double_values = []
for ped_id, ped_data in data['pastos'].items():
    ecm_values.extend(ped_data['ecms'])
    for i in range(len(ped_data['ecms'])):
        if 'event_' + str(i+1) not in ped_data.get('doubles', {}):
            ecm_values_for_avg.append(ped_data['ecms'][i])
    for double_item in ped_data.get('doubles', {}).values():
        ecm_double_values.append(double_item['best_error'])

# Create histogram
fig = go.Figure()

fig.add_trace(go.Histogram(
    x=ecm_values,
    name='ECM Distribution',
    opacity=0.55,
    nbinsx=100,  # You can adjust the number of bins
    marker_color='blue',
    marker_line_color='black',
    marker_line_width=1
))


fig.add_trace(go.Histogram(
    x=ecm_double_values,
    name='ECM Distribution (Double)',
    opacity=0.55,
    nbinsx=30,  # You can adjust the number of bins
    marker_color='red',
    marker_line_color='black',
    marker_line_width=1
))

fig.update_layout(barmode='overlay')


# Vertical line at ECM = 0.018
fig.add_vline(x=0.004, line_width=2, line_dash="dash", line_color="black",
              annotation_text="ECM THRESHOLD = 0.004", annotation_position="top right",
                annotation_font_size=16, annotation_font_color="black")

# Calculate averages
avg_ecm = np.mean(ecm_values)
avg_ecm_double = np.mean(ecm_double_values) if ecm_double_values else None

# Add annotation for avg_ecm
fig.add_annotation(
    x=avg_ecm,
    y=0,
    text=f"Avg ECM: {avg_ecm:.4f}",
    showarrow=True,
    arrowhead=2,
    ax=40,
    ay=-40,
    font=dict(color="blue", size=16),
    bgcolor="white",
    bordercolor="blue"
)

# Add annotation for avg_ecm_double if available
if avg_ecm_double is not None:
    fig.add_annotation(
        x=avg_ecm_double,
        y=0,
        text=f"Avg ECM (Double): {avg_ecm_double:.4f}",
        showarrow=True,
        arrowhead=2,
        ax=40,
        ay=-80,
        font=dict(color="red", size=16),
        bgcolor="white",
        bordercolor="red"
    )
    
fig.add_annotation(
        x=np.mean(ecm_values_for_avg),
        y=0,
        text=f"Avg ECM (No doubles): {np.mean(ecm_values_for_avg):.4f}",
        showarrow=True,
        arrowhead=2,
        ax=40,
        ay=-120,
        font=dict(color="orange", size=16),
        bgcolor="white",
        bordercolor="orange"
    )

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

# Calculate CCPDF (Complementary Cumulative Probability Distribution Function)
ecm_sorted = np.sort(ecm_values)
ccpdf = 1.0 - np.arange(1, len(ecm_sorted) + 1) / len(ecm_sorted)

# Add CCPDF trace (log-log scale)
#fig.add_trace(go.Scatter(
#    x=ecm_sorted,
#    y=ccpdf,
#    mode='lines',
#    name='CCPDF (log-log)',
#    line=dict(color='green', width=3, dash='dash'),
#))

# Set log-log scale for CCPDF
#fig.update_xaxes(type="log")
#fig.update_yaxes(type="log")

# Show the plot
#fig.show()

fig.write_image(
            f"./{name}_histo.png",
            width=1920,
            height=1080,
            scale=2  # Higher scale for better resolution
            )
