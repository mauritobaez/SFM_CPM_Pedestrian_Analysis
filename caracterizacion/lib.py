

def get_stops_complete(max_speed, time, vX, vY):
    curr_index_when_stopped = []
    last_time = None

    for i in range(len(time)):
        if (vX[i] < max_speed and vX[i] > -max_speed and vY[i] < max_speed and vY[i] > -max_speed) or i == 0:
            if last_time is None or time[i] - last_time > 1:
                curr_index_when_stopped.append((i, i))
            else:
                curr_index_when_stopped[-1] = (curr_index_when_stopped[-1][0], i)
            last_time = time[i]

    return curr_index_when_stopped


def add_vertical_line(fig, x, color='blue', width=1):
    fig.add_shape(
        type="line",
        x0=x,
        x1=x,
        y0=-0.5,
        y1=2,
        line=dict(color=color, width=width, dash="dash"),
        layer="below"
    )

def add_horizontal_line(fig, first_x, second_x, altura, color='blue', width=1):
    fig.add_shape(
        type="line",
        x0=first_x,
        x1=second_x,
        y0=altura,
        y1=altura,
        line=dict(color=color, width=width, dash="dash"),
        layer="below"
    )
    
