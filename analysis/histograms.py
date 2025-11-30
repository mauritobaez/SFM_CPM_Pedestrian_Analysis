

import json
import numpy as np
import plotly.graph_objects as go

# Load the data from acc_60.json
name = 'analisis/acc_sfm_histo'
with open(f'{name}.json', 'r') as f:
    data = json.load(f)

# Extract all ECM values
ecm_values = []
ecm_values_for_avg = []
ecm_double_values = []
i2t = []
for ped_id, ped_data in data['pastos'].items():
    # ecms = ped_data.get('ecms', [])
    # doubles = ped_data.get('doubles', {})
    # for event_id in range(1,9) if ped_id not in ['01', '09'] else range(1,8):
    #     ecm1 = ecms[event_id-1]
    #     ecm2 = doubles[f'event_{event_id if ped_id != '01' and ped_id != '09' else event_id+1}']['best_error']
    #     i2t_value = (ecm1 - ecm2) / ecm1
    #     i2t.append(i2t_value)

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
   name='MSE Distribution',
   opacity=0.55,
   nbinsx=100,  # You can adjust the number of bins
   marker_color='blue',
   marker_line_color='black',
   marker_line_width=1
))

# fig.add_trace(go.Histogram(
#     x=i2t,
#     name='i2t Distribution',
#     opacity=0.85,
#     nbinsx=10,  # You can adjust the number of bins
#     marker_color='blue',
#     marker_line_color='black',
#     marker_line_width=3
# ))


fig.add_trace(go.Histogram(
   x=ecm_double_values,
   name='MSE Distribution (Double)',
   opacity=0.55,
   nbinsx=30,  # You can adjust the number of bins
   marker_color='red',
   marker_line_color='black',
   marker_line_width=1
))

fig.update_layout(barmode='overlay')


#Vertical line at ECM = 0.018
fig.add_vline(x=0.004, line_width=2, line_dash="dash", line_color="red",
              annotation_text="MSE THRESHOLD = 0.004", annotation_position="top right",
                annotation_font_size=24, annotation_font_color="red")

# # Count points lower and higher than 0.5
# count_lower = sum(val < 0.5 for val in i2t)
# count_higher = sum(val > 0.5 for val in i2t)

# fig.add_annotation(
#     x=0.4,
#     y=max(fig.data[0].y) * 0.95 if hasattr(fig.data[0], 'y') and fig.data[0].y is not None else 20,
#     text=f"< 0.5: {count_lower}",
#     showarrow=False,
#     font=dict(color="black", size=24),
#     bgcolor="white",
#     bordercolor="black",
#     xanchor="right"
# )

# fig.add_annotation(
#     x=0.6,
#     y=max(fig.data[0].y) * 0.95 if hasattr(fig.data[0], 'y') and fig.data[0].y is not None else 20,
#     text=f"> 0.5: {count_higher}",
#     showarrow=False,
#     font=dict(color="black", size=24),
#     bgcolor="white",
#     bordercolor="black",
#     xanchor="left"
# )

# Calculate averages
avg_ecm = np.mean(ecm_values)
avg_ecm_double = np.mean(ecm_double_values) if ecm_double_values else None

# Add annotation for avg_ecm
fig.add_annotation(
   x=avg_ecm,
   y=0,
   text=f"Avg MSE: {avg_ecm:.4f}",
   showarrow=True,
   arrowhead=2,
   ax=340,
   ay=-340,
   font=dict(color="blue", size=24),
   bgcolor="white",
   bordercolor="blue"
)

# Add annotation for avg_ecm_double if available
if avg_ecm_double is not None:
   fig.add_annotation(
       x=avg_ecm_double,
       y=0,
       text=f"Avg MSE (Double): {avg_ecm_double:.4f}",
       showarrow=True,
       arrowhead=2,
       ax=240,
       ay=-380,
       font=dict(color="red", size=24),
       bgcolor="white",
       bordercolor="red"
   )
    
fig.add_annotation(
       x=np.mean(ecm_values_for_avg),
       y=0,
       text=f"Avg MSE (No doubles): {np.mean(ecm_values_for_avg):.4f}",
       showarrow=True,
       arrowhead=2,
       ax=290,
       ay=-420,
       font=dict(color="orange", size=24),
       bgcolor="white",
       bordercolor="orange"
   )

# Update layout
fig.update_layout(
    title="Distribution of MSE Values",
    xaxis_title="MSE Value",
    yaxis_title="Frequency",
    template="plotly_white",
    showlegend=True,
    font=dict(size=30),
    xaxis=dict(title_font=dict(size=24), tickfont=dict(size=18)),
    yaxis=dict(title_font=dict(size=24), tickfont=dict(size=18)),
)

# Calculate CCPDF (Complementary Cumulative Probability Distribution Function)
#ecm_sorted = np.sort(ecm_values)
#ccpdf = 1.0 - np.arange(1, len(ecm_sorted) + 1) / len(ecm_sorted)

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
            scale=5  # Higher scale for better resolution
            )
