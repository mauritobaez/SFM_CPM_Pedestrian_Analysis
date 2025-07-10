import plotly.graph_objects as go

# Sample data
x = [0, 1, 2, 3, 4, 5, 6]
y = [1, 3, 2, 4, 3, 5, 4]

fig = go.Figure()

# Add main line plot
fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode='lines+markers',
    name='Data'
))

# Define color-coded regions
highlight_regions = [
    {"x0": 0.5, "x1": 2.5, "color": "LightSkyBlue", "label": "Region A"},
    {"x0": 3, "x1": 4, "color": "LightSalmon", "label": "Region B"},
    {"x0": 4.5, "x1": 5.5, "color": "LightGreen", "label": "Region C"},
]

# Add each region as a shape
for region in highlight_regions:
    fig.add_shape(
        type="rect",
        x0=region["x0"],
        x1=region["x1"],
        y0=0,
        y1=max(y) + 1,  # Extend a bit above the data
        fillcolor=region["color"],
        opacity=0.4,
        layer="below",
        line_width=0,
    )

for region in highlight_regions:
    # Draw vertical lines at the region boundaries
    fig.add_shape(
        type="line",
        x0=region["x0"],
        x1=region["x0"],
        y0=min(y) - 1,
        y1=max(y) + 1,
        line=dict(color=region["color"], width=3, dash="dash"),
        layer="below"
    )
    fig.add_shape(
        type="line",
        x0=region["x1"],
        x1=region["x1"],
        y0=min(y) - 1,
        y1=max(y) + 1,
        line=dict(color=region["color"], width=3, dash="dash"),
        layer="below"
    )

# Optional: add annotations for each region
for region in highlight_regions:
    fig.add_annotation(
        x=(region["x0"] + region["x1"]) / 2,
        y=max(y) + 0.5,
        text=region["label"],
        showarrow=False,
        font=dict(size=12, color="black"),
        bgcolor=region["color"],
        opacity=0.7
    )

fig.update_layout(
    title="Plot with Multiple Highlighted Regions",
    xaxis_title="X Axis",
    yaxis_title="Y Axis"
)

fig.show()
