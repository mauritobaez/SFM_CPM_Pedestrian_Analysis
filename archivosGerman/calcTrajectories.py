
"""
Created on Thu Nov 30 14:53:18 2023

@author: german
"""

import numpy as np
import glob

from data_lib import divide_in_events, fft_filter, five_point_stencil, hampel_filter, moving_average_smoothing


inputFolder = './archivosGerman/pedestrianTrajectories/'
outputFolder = './archivosGerman/by_events/'
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
    (events, all_events_indexes) = divide_in_events(X_smooth, Y_smooth)
    for j, event in enumerate(events):
        event_indexes = all_events_indexes[j]
        
        V = five_point_stencil(event,1/FPS)
        t = np.arange(0,len(V))/FPS

        V_clean = hampel_filter(V, 19, 2)
        #VX_clean = hampel_filter(VX, 19, 2)
        #VY_clean = hampel_filter(VY, 19, 2)
        
        V_fft = fft_filter(V_clean, fs=FPS, highcut=0.5)
        #vx_fft = fft_filter(VX_clean, fs=FPS, highcut=0.5)
        #vy_fft = fft_filter(VY_clean, fs=FPS, highcut=0.5)

        data = np.c_[t,X_smooth[event_indexes[0]:event_indexes[1]+1],Y_smooth[event_indexes[0]:event_indexes[1]+1],V_fft]   # Para evitar el smoothing cambiar esto a VX y VY
        outFile = f'tXYV_ped{i+1:02d}_event{j+1:02d}.txt'

        np.savetxt(outputFolder+outFile, data, delimiter='\t',fmt='%.8e')
    
