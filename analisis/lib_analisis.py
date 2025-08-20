

import numpy as np


# Quizás cambiar el 1.3
def acceleration(parameter):
    def acc(t, tau):
        return parameter * (1 - np.exp(-t / tau))
    return acc

def deceleration(parameter):
    def dece(t, tau):
        return parameter * np.exp(-t / tau)
    return dece
