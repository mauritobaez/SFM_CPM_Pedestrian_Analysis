import statistics


def get_stops_complete(max_speed, time, vX, vY):
    curr_index_when_stopped = []
    last_time = None

    for i in range(len(time)):
        if abs(vX[i]) < max_speed and abs(vY[i]) < max_speed or i == 0:
            if last_time is None or time[i] - last_time > 1:
                curr_index_when_stopped.append((i, i))
            else:
                curr_index_when_stopped[-1] = (curr_index_when_stopped[-1][0], i)
            last_time = time[i]

    return curr_index_when_stopped

def get_between_indexes(first_index, last_index, v):
    velocities = []
    for i in range(first_index, last_index + 1):
        velocities.append(abs(v[i]))
    return velocities

def get_all_values(time, vX, vY, stops):
    stop_index = 0
    velocities = []
    direction_vel = vX
    for i in range(len(time)):
        if stop_index < len(stops)-1 and i > stops[stop_index+1][0]:
            stop_index += 1
            direction_vel = vY if stop_index == 2 or stop_index == 5 else vX
        velocities.append(abs(direction_vel[i]))
    return velocities

# Esto es para tener en cuenta los minimos siguientes a un stop, es innecesariamente ineficiente hacerlo con otra función
# Debería estar en get_stops_complete
def get_reduced_stops(stops, velocities):
    reduced_stops = []
    for i in range(len(stops)):
        beg_stop, end_stop = stops[i]
        reduced_stops.append(stops[i])
        # No me acuerdo bien por qué está esto
        #if beg_stop == 0:
        #    continue
        current_index = beg_stop
        min = velocities[beg_stop]
        index_min = beg_stop
        
        while current_index <= end_stop:
            curr_vel = velocities[current_index]
            if curr_vel < min:
                min = curr_vel
                index_min = current_index
            if curr_vel - min > 0.001 or curr_vel < 0.08:
                reduced_stops[i] = (index_min, end_stop)
                break
            current_index += 1

        current_index = end_stop
        min = velocities[end_stop]
        index_min = end_stop
        while current_index >= beg_stop:
            curr_vel = velocities[current_index]
            if curr_vel < min:
                min = curr_vel
                index_min = current_index
            if curr_vel - min > 0.001 or curr_vel < 0.08:
                reduced_stops[i] = (reduced_stops[i][0], index_min)
                break
            current_index -= 1
    return reduced_stops

def get_all_values_and_positions(time, vX, vY, x, y, stops):
    stop_index = 0
    velocities = []
    positions = []
    direction_vel = vX
    direction_walk = x
    for i in range(len(time)):
        if stop_index < len(stops)-1 and i > stops[stop_index+1][0]:
            stop_index += 1
            direction_vel = vY if stop_index == 2 or stop_index == 5 else vX
            direction_walk = y if stop_index == 2 or stop_index == 5 else x
        velocities.append(abs(direction_vel[i]))
        positions.append(direction_walk[i])
    return velocities, positions

# Esto te devuelve por evento desde el primer beginning del stop hasta el final del siguiente stop
def get_all_events(time, vX, vY, stops):
    stop_index = 0
    events = []
    current_event = []
    next_event = []
    direction_vel = vX
    start_next = False
    for i in range(len(time)):
        if stop_index < len(stops)-1 and i > stops[stop_index+1][0]:
            stop_index += 1
            alt_dir = vY if stop_index == 2 or stop_index == 5 else vX
            start_next = True
            next_event = []
            
        if start_next and stops[stop_index][1] == i:
            events.append(current_event)
            current_event = next_event
            direction_vel = alt_dir
            start_next = False
        
        if start_next:
            next_event.append(abs(alt_dir[i]))
        current_event.append(abs(direction_vel[i]))
        
    return events

def add_vertical_line(fig, x, color='blue', width=5, showlegend=False, legend="", dash="dash"):
    dash_style = dash if dash is not None else "solid"
    fig.add_shape(
        type="line",
        x0=x,
        x1=x,
        y0=-0.25,
        y1=2,
        line=dict(color=color, width=width, dash=dash_style),
        layer="below",
        showlegend=showlegend,
        name=legend
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

def get_middles(positions, stops):
    middles = []
    for _, end_stop in stops:
        curr_index = end_stop
        curr_meter = positions[end_stop]
        while curr_index < len(positions):
            if 3.25 < abs(curr_meter - positions[curr_index]):
                middles.append(curr_index)
                break
            curr_index += 1
    
    return middles

def get_middle(positions, prev_end_stop):
    curr_index = prev_end_stop
    curr_meter = positions[prev_end_stop]
    while curr_index < len(positions):
        if positions[curr_index] == 0:
            curr_index += 1
            continue
        if 3.25 < abs(curr_meter - positions[curr_index]):
            return curr_index - 1 if abs(abs(curr_meter - positions[curr_index - 1]) - 3.25) < abs(abs(curr_meter - positions[curr_index]) - 3.25) else curr_index
        curr_index += 1
    return None

def get_next_local_minimum(v, start_index):
    curr_index = start_index
    while curr_index < len(v) - 1:
        if v[curr_index] < v[curr_index + 1]:
            return curr_index
        curr_index += 1
    return len(v) - 1

def get_prev_local_minimum(v, start_index):
    curr_index = start_index
    while curr_index > 0:
        if v[curr_index] < v[curr_index - 1]:
            return curr_index
        curr_index -= 1
    return 0

def get_avg_speeds_around_positions(positions_index, positions, v, meters_around=0.5):
    avg_speeds = []
    for pos in positions_index:
        mid_pos = positions[pos]
        curr_forw_pos = mid_pos
        forw_ind = pos
        while abs(curr_forw_pos - mid_pos) < meters_around:
            forw_ind += 1
            curr_forw_pos = positions[forw_ind]
       
        curr_back_pos = mid_pos
        back_ind = pos
        while abs(curr_back_pos - mid_pos) < meters_around:
            back_ind -= 1
            curr_back_pos = positions[back_ind]
    
        avg_speed = statistics.mean(v[back_ind:forw_ind+1])
        avg_speeds.append(avg_speed)
    return avg_speeds
