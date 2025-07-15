import numpy as np


def fft_filter(signal, fs, highcut):
    """
    signal: array 1D de la señal a filtrar
    fs: frecuencia de muestreo
    lowcut: frecuencia mínima del filtro
    highcut: frecuencia máxima del filtro
    """
    fft_vals = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1/fs)
    
    # Crear un filtro pasabanda
    band = (np.abs(freqs) > highcut)
    filtered_fft = fft_vals.copy()
    filtered_fft[band] = 0
    
    # Inversa FFT para obtener la señal filtrada
    filtered_signal = np.fft.ifft(filtered_fft).real
    
    return filtered_signal

def hampel_filter(v, window_size=7, n_sigmas=3):
    """
    v: array 1D de velocidades (o posiciones)
    window_size: longitud de la ventana (debe ser impar)
    n_sigmas: número de desviaciones estándar para considerar outlier
    """
    L = len(v)
    k = (window_size - 1) // 2
    filtered = v.copy()
    
    for i in range(L):
        # límites de ventana
        lo = max(i - k, 0)
        hi = min(i + k + 1, L)
        window = v[lo:hi]
        
        med = np.median(window)
        sigma = 1.4826 * np.median(np.abs(window - med))  # estimador robusto
        if np.abs(v[i] - med) > n_sigmas * sigma:
            filtered[i] = med  # reemplaza outlier por mediana local
    return filtered

def moving_average_smoothing(v, window_size=5):
    """
    v: array 1D de velocidades (o posiciones)
    window_size: longitud de la ventana (debe ser impar)
    """
    if window_size % 2 == 0:
        raise ValueError("window_size debe ser impar")
    
    half_window = window_size // 2
    smoothed = np.zeros_like(v)
    
    for i in range(len(v)):
        lo = max(i - half_window, 0)
        hi = min(i + half_window + 1, len(v))
        smoothed[i] = np.mean(v[lo:hi])
    
    return smoothed

def finite_difference_left(x, y, dt):
    """
    Calcula las velocidades usando diferencia finita por izquierda
    
    x: array 1D de posiciones en el eje x
    y: array 1D de posiciones en el eje y
    dt: intervalo de tiempo entre mediciones
    """
    vx = np.zeros(len(x))
    vy = np.zeros(len(y))
    
    for i in range(1, len(x)):
        vx[i] = (x[i] - x[i-1]) / dt
        vy[i] = (y[i] - y[i-1]) / dt
    
    # Manejo de los extremos
    vx[0] = (x[1] - x[0]) / dt
    vy[0] = (y[1] - y[0]) / dt
    
    return vx, vy

def finite_difference_centered(x, y, dt):
    """
    Calcula las velocidades usando diferencia finita por izquierda
    
    x: array 1D de posiciones en el eje x
    y: array 1D de posiciones en el eje y
    dt: intervalo de tiempo entre mediciones
    """
    vx = np.zeros(len(x))
    vy = np.zeros(len(y))
    
    for i in range(1, len(x)-1):
        vx[i] = (x[i+1] - x[i-1]) / (2*dt)
        vy[i] = (y[i+1] - y[i-1]) / (2*dt)
    
    # Manejo de los extremos
    vx[0] = (x[1] - x[0]) / dt
    vy[0] = (y[1] - y[0]) / dt
    vx[-1] = (x[-1] - x[-2]) / dt
    vy[-1] = (y[-1] - y[-2]) / dt
    
    return vx, vy


def five_point_stencil(x,dt):
    vx = np.zeros(len(x))
    #vy = np.zeros(len(y))
    
    for i in range(len(x)-4):
        vx[i+2] = (x[i]/12-2/3*x[i+1]+2/3*x[i+3]-x[i+4]/12)/dt
        #vy[i+2] = (y[i]/12-2/3*y[i+1]+2/3*y[i+3]-y[i+4]/12)/dt
        
    vx[0] = (x[1]-x[0])/dt
    #vy[0] = (y[1]-y[0])/dt
    vx[1] = (x[2]-x[0])/dt/2
    #vy[1] = (y[2]-y[0])/dt/2
    vx[-1] = (x[-1]-x[-2])/dt
    #vy[-1] = (y[-1]-y[-2])/dt
    vx[-2] = (x[-1]-x[-3])/dt/2
    #vy[-2] = (y[-1]-y[-3])/dt/2

    return vx


def divide_in_events(x, y):
    complete_events = []
    event_indexes = []
    index = 0
    print(f"Min x: {min(x):.4f}, Max x: {max(x):.4f}, difference = {max(x) - min(x):.4f}. Min y: {min(y):.4f}, Max y: {max(y):.4f}, difference = {max(y) - min(y):.4f}")
    target_x = (max(x) - min(x))/2
    target_y = (max(y) - min(y))/2
    for i in range(8):
        direction = y if i == 2 or i == 5 else x
        other_direction = x if i == 2 or i == 5 else y
        target_to_use = target_y if i == 2 or i == 5 else target_x
        initial_index = index
        initial_position = direction[index]
        other_direction_initial = other_direction[index]
        current_pos = initial_position
        while(abs(current_pos - initial_position) < target_to_use and index < len(direction) and abs(other_direction[index] - other_direction_initial) < 0.3):
            current_pos = direction[index]
            index += 1
        target = initial_position + target_to_use
        end_of_event_index = index if abs(current_pos - target) < abs(direction[index-1] - target) else index - 1
        complete_events.append(direction[initial_index:end_of_event_index+1])
        event_indexes.append((initial_index, end_of_event_index))
    return complete_events, event_indexes


def append_values_at_position(array, n, position, value=0):
    """
    Append n values at the specified position in the array.
    """
    if position < 0 or position > len(array):
        raise ValueError("Position out of bounds")
    
    return np.insert(array, position, [value]*n)
