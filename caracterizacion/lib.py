

def get_stops_complete(max_speed, time, vX, vY):
    curr_index_when_stopped = []
    last_time = None

    for i in range(len(time)):
        if (vX[i] < max_speed and vX[i] > -max_speed and vY[i] < max_speed and vY[i] > -max_speed):
            if last_time is None or time[i] - last_time > 1:
                curr_index_when_stopped.append(i)
            last_time = time[i]

    return curr_index_when_stopped



