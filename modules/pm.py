# projectile motion with restiance
import matplotlib.pyplot as plt
import numpy as np
from modules.conversion import sin, cos
from modules.pmwr import endTimeCalculation

def calculateFunctionGraph(initialVelocity, initialHeight, alpha, gravity, resistance):
    time = np.linspace(0, endTimeCalculation(initialVelocity, initialHeight, alpha, gravity), 100)
    x = (initialVelocity * cos(alpha) / resistance) * (1 - np.exp(-1 * resistance * time))

    vy = initialVelocity * sin(alpha)
    y = initialHeight + (vy / resistance) + gravity / (resistance ** 2) - gravity * time / resistance - ((resistance * vy + gravity) / (resistance ** 2)) * np.exp(-1 * resistance * time)
