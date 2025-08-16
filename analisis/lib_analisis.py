

import numpy as np


# Quizás cambiar el 1.3
def acceleration(t, tau):
    return 1.3 * (1 - np.exp(-t / tau))

def deceleration(t, tau):
    return 1.3 * np.exp(-t / tau)
