import statistics


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
        y0=-0.25,
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
    

MIN_TIME_AFTER_STOP = 2
MAX_TIME_AFTER_STOP = 3
FPS = 60
TICKS_MIN_TIME_AFTER_STOP = MIN_TIME_AFTER_STOP * FPS
TICKS_MAX_TIME_AFTER_STOP = MAX_TIME_AFTER_STOP * FPS
def gaussian(index_when_stopped, time, vX, vY):
    for i in range(len(index_when_stopped)):
        if i == 0:
            gaussian_distibution = []
        curr_index = index_when_stopped[i][1]
        curr_rapidez = []

        direction_vel = vY if i == 2 or i == 5 else vX

        for j in range(int(curr_index + TICKS_MIN_TIME_AFTER_STOP), int(curr_index + TICKS_MAX_TIME_AFTER_STOP)):
            if j >= 0 and j < len(time):
                curr_rapidez.append(abs(direction_vel[j]))
        if curr_rapidez:
            mean = statistics.mean(curr_rapidez)
            std_dev = statistics.stdev(curr_rapidez) if len(curr_rapidez) > 1 else 0
            gaussian_distibution.append((mean, std_dev))
            #print(f"Index {i}, mean: {mean}, std_dev: {std_dev}")
    
    moments_finish_acc = []
    for index_number_stop, index_stop in enumerate(index_when_stopped):
        if index_number_stop >= len(gaussian_distibution):
            break

        direction_vel = vY if index_number_stop == 2 or index_number_stop == 5 else vX
        curr_mean, curr_std_dev = gaussian_distibution[index_number_stop]
        
        for j in range(index_stop[1], int(index_stop[1] + (TICKS_MIN_TIME_AFTER_STOP+ TICKS_MAX_TIME_AFTER_STOP) / 2)):
            if j < len(time):
                vel_importante = abs(direction_vel[j])
                
                if curr_mean - curr_std_dev < vel_importante and curr_mean + curr_std_dev > vel_importante:
                    moments_finish_acc.append(time[j])
                    break
        #if j == index_stop[1] + TICKS_MIN_TIME_AFTER_STOP - 1:
        #    moments_finish_acc.append(time[j])
        #print(f"{index_stop[1]} j: {j}")
    return moments_finish_acc
