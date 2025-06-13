


def linear_regression(velocities, time, index_start, index_end, c):
    initial_velocity = velocities[index_start]
    initial_time = time[index_start]
    return sum([(velocities[i] - (c * (time[i]-initial_time) + initial_velocity)) ** 2 for i in range(index_start, index_end + 1)])

def linear_regression_best(velocities, time, index_start, index_end):
    min_error = float('inf')
    best_c = None
    for c in [i * 0.002 for i in range(-1100, 10)]:
        error = linear_regression(velocities, time, index_start, index_end, c)
        if error < min_error:
            min_error = error
            best_c = c
    
    return best_c, min_error

def double_linear_regression(complete_velocities, time, index_start, index_end):
    best_index = float('inf')
    best_error = float('inf')
    best_first_c = None
    best_second_c = None
    for i in range(index_start, index_end+1):
        first_c, first_error = linear_regression_best(complete_velocities, time, index_start, i)
        second_c, second_error = linear_regression_best(complete_velocities, time, i, index_end)
        if first_error + second_error < best_error:
            best_error = first_error + second_error
            best_index = i
            best_first_c = first_c
            best_second_c = second_c

    return best_index, best_first_c, best_second_c



