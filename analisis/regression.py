import numpy as np



#def linear_regression(velocities, time, index_start, index_end, c, b):
#    initial_velocity = b
#    initial_time = time[index_start]
#    return sum([(velocities[i] - (c * (time[i]-initial_time) + initial_velocity)) ** 2 for i in range(index_start, index_end + 1)])

def linear_regression_best(velocities, time, index_start, index_end):
    time_segment = np.array(time[index_start:index_end + 1])
    velocities_segment = np.array(velocities[index_start:index_end + 1])
    # Fit a line using original time values: y = mx + b
    best_m, best_b = np.polyfit(time_segment, velocities_segment, 1)
    # Compute predicted velocities
    predicted = best_m * time_segment + best_b
    # Compute least squares error (cost)
    error = np.sum((velocities_segment - predicted) ** 2)
    return best_m, best_b, error

def double_linear_regression(complete_velocities, time, index_start, index_end):
    best_time = -1
    best_error = float('inf')
    best_first_m = None
    best_second_m = None
    best_i = -1
    for i in range(index_start, index_end+1):
        if abs(i - index_start) < 2 or abs(index_end - i) < 2:
            continue
        first_m, first_b, first_error = linear_regression_best(complete_velocities, time, index_start, i)
        second_m, second_b, second_error = linear_regression_best(complete_velocities, time, i, index_end)
        if first_error + second_error < best_error:
            best_error = first_error + second_error
            # Calculate intersection point between the two lines
            # First line: y = first_m * t + first_b
            # Second line: y = second_m * t + second_b
            if first_m != second_m:
                # At intersection: first_m * t + first_b = second_m * t + second_b
                # (first_m - second_m) * t = second_b - first_b
                best_time = (second_b - first_b) / (first_m - second_m)
            else:
                print(f"Warning: Lines are parallel at indices {index_start} and {index_end}, using index {i} as fallback.")
                best_time = i  # fallback if lines are parallel
            best_first_m = first_m
            best_second_m = second_m
            best_first_b = first_b
            best_second_b = second_b
            best_i = i
    
    #print(f"Best i: {best_i}, best i / 60: {best_i/60}, Best time: {best_time}")
    return best_time, best_first_m, best_second_m, best_first_b, best_second_b



