# projectile motion with restiance
import matplotlib.pyplot as plt
import numpy as np
from modules.conversion import sin, cos
from modules.pmwr import endTimeCalculation

def velocity(initialVelocity, alpha, gravity, time, resistance):
    xVelocity = initialVelocity * np.exp(-1 * resistance * time) * cos(alpha)
    yVelocity = (initialVelocity * sin(alpha) + gravity / resistance) * np.exp(-1 * resistance * time) - gravity / resistance

    if time == 0.0:
        return {"xVelocity": xVelocity, "yVelocity": yVelocity, "velocity": initialVelocity}

    velocity = np.sqrt(xVelocity ** 2 + yVelocity ** 2)
    return {"xVelocity": xVelocity, "yVelocity": yVelocity, "velocity": velocity}


def xPoint(initialVelocity, alpha, time, resistance):
    return (initialVelocity * cos(alpha) / resistance) * (1 - np.exp(-1 * resistance * time))


def yPoint(v0y, initialHeight, alpha, gravity, time, resistance):
    return initialHeight + (v0y / resistance) + gravity / (resistance ** 2) - gravity * time / resistance - ((resistance * v0y + gravity) / (resistance ** 2)) * np.exp(-1 * resistance * time)


def vertex(initialVelocity, initialHeight, alpha, gravity, resistance):
    time = (np.log(resistance * initialVelocity * sin(alpha) / gravity) + 1) / resistance
    v0y = initialVelocity * sin(alpha)

    x = xPoint(initialVelocity, alpha, time, resistance)
    y = yPoint(v0y, initialHeight, alpha, gravity, time, resistance)
    
    return {"x": x, "y": y, "t": time}


def xToTime(x, initialVelocity, alpha, resistance):
    return - 1 * np.log(1 - resistance * x / (initialVelocity * cos(alpha))) / resistance        


def calculateFunctionGraph(initialVelocity, initialHeight, alpha, gravity, resistance):
    time = np.linspace(0, endTimeCalculation(initialVelocity, initialHeight, alpha, gravity), 100)
    if alpha == np.pi / 2:
        height = initialHeight + (initialVelocity ** 2) / (2 * gravity)
        return {"x": 0, "y": height}

    elif alpha == -1 * np.pi / 2:
        return {"x": 0, "y": initialHeight}
        
    x = (initialVelocity * cos(alpha) / resistance) * (1 - np.exp(-1 * resistance * time))
    v0y = initialVelocity * sin(alpha)
    y = initialHeight + (v0y / resistance) + gravity / (resistance ** 2) - gravity * time / resistance - ((resistance * v0y + gravity) / (resistance ** 2)) * np.exp(-1 * resistance * time)

    return {"x": x, "y": y}  
