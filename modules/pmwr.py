# projectile motion without restiance
import numpy as np
from modules.conversion import sin, cos


def vertex(initialVelocity, initialHeight, alpha, gravity, r):
    if alpha == np.pi / 2:
        return {"y": initialVelocity **2 / 2*gravity, "x": 0, "t": initialVelocity / gravity}
    elif alpha <= 0:
        return {"y": initialHeight, "x": 0, "t": 0}
    A = -1 * gravity / (2 * initialVelocity ** 2 * cos(alpha) ** 2)
    B = np.tan(alpha)
    C = initialHeight
    quadraticEquation = [A, B, C]
    roots = np.roots(quadraticEquation)
    x = (roots[0] + roots[1])/2

    return {"y": A * x ** 2 + B * x + C, "x": x, "t": xToTime(x, initialVelocity, alpha)}


def velocity(initialVelocity, alpha, gravity, time, r):
    xVelocity = initialVelocity * cos(alpha)
    yVelocity = initialVelocity * sin(alpha) - gravity * time
    if time == 0.0:
        return {"velocity": initialVelocity, "xvelocity": xVelocity, "yvelocity": yVelocity}
    velocity = np.sqrt(xVelocity ** 2 + yVelocity ** 2)
    return {"velocity": velocity, "xvelocity": xVelocity, "yvelocity": yVelocity}


def endTimeCalculation(initialVelocity, initialHeight, alpha, gravity):
    A = -1 * gravity / 2
    B = initialVelocity * sin(alpha)
    C = initialHeight

    quadraticEquation = [A, B, C]
    roots = np.roots(quadraticEquation)
    return max(roots)


def xPoint(initialVelocity, alpha, time, r):
    #alpha w radianach
    return initialVelocity * cos(alpha) * time


def yPoint(initialVelocity, initialHeight, alpha, gravity, time, r):
    #alpha w radianach
    y = initialHeight + initialVelocity * sin(alpha) * time - (gravity * time ** 2) / 2
    if y < 0:
        return 0
    return y


def xToTime(x, initialVelocity, alpha, r=0):
    return x / (initialVelocity * cos(alpha))


def rangeCalculation(initialVelocity, initialHeight, alpha, gravity, r):
    if alpha == np.pi / 2 or alpha == -np.pi / 2:
        return 0
    A = -1 * gravity / (2 * initialVelocity ** 2 * cos(alpha) ** 2)
    B = np.tan(alpha)
    C = initialHeight

    quadraticEquation = [A, B, C]
    roots = np.roots(quadraticEquation)
    return max(roots)


def calculateFunctionGraph(initialVelocity, initialHeight, alpha, gravity, r):
    # kąty muszą być w radianach
    if alpha == np.pi / 2:
        height = initialHeight + (initialVelocity ** 2) / (2 * gravity)
        return {"x": 0, "y": height}
        
    elif alpha == -1 * np.pi / 2:
        return {"x": 0, "y": initialHeight}
    
    else:
        range = rangeCalculation(initialVelocity, initialHeight, alpha, gravity, 0)

    x = np.linspace(0, range, 1000)
    y = (initialHeight + np.tan(alpha) * x - gravity * x ** 2 / (2 * initialVelocity ** 2 * cos(alpha) ** 2))

    return {"x": x, "y": y}
