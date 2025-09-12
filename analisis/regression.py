import numpy as np



#def linear_regression(velocities, time, index_start, index_end, c, b):
#    initial_velocity = b
#    initial_time = time[index_start]
#    return sum([(velocities[i] - (c * (time[i]-initial_time) + initial_velocity)) ** 2 for i in range(index_start, index_end + 1)])

def linear_regression_best(velocities, time, index_start, index_end):
    # Zero-base the time array for the regression segment
    time_segment = np.array(time[index_start:index_end + 1])
    time_zeroed = time_segment - time_segment[0]
    velocities_segment = np.array(velocities[index_start:index_end + 1])
    # Fit a line: y = m*x + b
    best_m, best_b = np.polyfit(time_zeroed, velocities_segment, 1)
    # Compute predicted velocities
    predicted = best_m * time_zeroed + best_b
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
            # Calculate intersection point between the two lines: first_m*x + first_b = second_m*x + second_b
            if first_m != second_m:
                numerator = first_m * time[index_start] - second_m * time[i] + second_b - first_b   # Lo de time es para ajustarlo porque las líneas no empiezan en el mismo t
                denominator = first_m - second_m
                best_time = numerator / denominator
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



