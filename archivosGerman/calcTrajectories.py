
"""
Created on Thu Nov 30 14:53:18 2023

@author: german
"""

import numpy as np
import glob
from scipy.signal import savgol_filter

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


def five_point_stencil(x,y,dt):
    vx = np.zeros(len(x))
    vy = np.zeros(len(y))
    
    for i in range(len(x)-4):
        vx[i+2] = (x[i]/12-2/3*x[i+1]+2/3*x[i+3]-x[i+4]/12)/dt
        vy[i+2] = (y[i]/12-2/3*y[i+1]+2/3*y[i+3]-y[i+4]/12)/dt
        if vx[i+2] > 5:
            print('vx',i+2,vx[i+2])
            print(f'Values = {x[i]},{x[i+1]},{x[i+2]},{x[i+3]},{x[i+4]}')
    
    vx[0] = (x[1]-x[0])/dt
    vy[0] = (y[1]-y[0])/dt
    vx[1] = (x[2]-x[0])/dt/2
    vy[1] = (y[2]-y[0])/dt/2
    vx[-1] = (x[-1]-x[-2])/dt
    vy[-1] = (y[-1]-y[-2])/dt
    vx[-2] = (x[-1]-x[-3])/dt/2
    vy[-2] = (y[-1]-y[-3])/dt/2

    return vx,vy

inputFolder = './archivosGerman/pedestrianTrajectories/'
outputFolder = './archivosGerman/MovingAverageStencilHampel/'
import os
os.makedirs(outputFolder, exist_ok=True)

DIST_AB = 30 # metros
FPS = 60 # cuadros por segundo

HEIGHT = 30 # metros, altura drone
alturas = np.array([1.69,1.6,1.69,1.69,1.71,1.75,1.80,1.80,1.81,1.82,1.82,1.83,1.83,1.82])

# PUNTOS DE REFERENCIA FIJOS DE LA CANCHA
puntoA = np.loadtxt(inputFolder+'puntoA.txt')
puntoB = np.loadtxt(inputFolder+'puntoB.txt')

# POSICIONES DE LOS PEATONES
inputFile = glob.glob(inputFolder+'ped*.txt')
inputFile.sort()
# Print names of input files

for i in range(len(inputFile)):
    ped = np.loadtxt(inputFile[i])
    print(inputFile[i])
    xA = puntoA[int(ped[0,0]):int(ped[-1,0])+1,2]
    yA = puntoA[int(ped[0,0]):int(ped[-1,0])+1,3]
    xB = puntoB[int(ped[0,0]):int(ped[-1,0])+1,2]
    yB = puntoB[int(ped[0,0]):int(ped[-1,0])+1,3]
    r = np.sqrt((xB-xA)**2+(yB-yA)**2)

    # CORRIJO LA POSICIONES SEGUN LA PROYECCION (QUIERO LA POSICION DE LA CABEZA SOBRE EL PLANO DEL SUELO)

    x = ped[:,2]*(1-alturas[i]/HEIGHT)-xA
    y = ped[:,3]*(1-alturas[i]/HEIGHT)-yA

    # ROTO EL SISTEMA DE REFERENCIA

    X = ((xB-xA)*x+(yB-yA)*y)/r/r*DIST_AB
    Y = (-(yB-yA)*x+(xB-xA)*y)/r/r*DIST_AB

    # SMOOTHING DE LAS POSICIONES
    #X = savgol_filter(X, window_length=7, polyorder=3) # Hasta ahora: 7 y 3
    #Y = savgol_filter(Y, window_length=7, polyorder=3)
    X_smooth = moving_average_smoothing(X, window_size=5)
    Y_smooth = moving_average_smoothing(Y, window_size=5)

    # CALCULO LAS VELOCIDADES USANDO DIFERENCIAS FINITAS DE LAS POSICIONES EN DISTINTOS TIEMPOS

    VX,VY = five_point_stencil(X_smooth,Y_smooth,1/FPS)
    t = np.arange(0,len(ped))/FPS

    VX_clean = hampel_filter(VX, 19, 2)
    VY_clean = hampel_filter(VY, 19, 2)
    # GUARDO LOS DATOS

    #data = np.c_[t,X,Y,VX,VY]
    data = np.c_[t,X,Y,VX_clean,VY_clean]   # Para evitar el smoothing cambiar esto a VX y VY
    outFile = 'tXYvXvY' + str(i).zfill(2) + '.txt'
    np.savetxt(outputFolder+outFile, data, delimiter='\t',fmt='%.8e')
  
