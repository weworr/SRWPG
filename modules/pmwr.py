# projectile motion without restiance
import matplotlib.pyplot as plt
import numpy as np
from modules.conversion import sin,cos

def maxHeight(A, B, C, x):
    return A * x ** 2 + B * x + C


def velocity(initialVelocity, alpha, gravity, time):
    if time == 0.0:
        return initialVelocity
    xVelocity = initialVelocity * np.cos(alpha)
    yVelocity = initialVelocity * np.sin(alpha) - gravity * time
    velocity = np.sqrt(xVelocity ** 2 + yVelocity ** 2)
    return velocity


def endTime(initialVelocity, initialHeight, alpha, gravity):
    A = -1 * gravity / 2
    B = initialVelocity * sin(alpha)
    C = initialHeight

    quadraticEquation = [A, B, C]
    roots = np.roots(quadraticEquation)
    return max(roots)


def cooridnates(initialVelocity, initialHeight, alpha, gravity, time):
    #alpha w radianach
    x = initialVelocity * cos(alpha) * time
    y = initialHeight * sin(alpha) * time - (gravity * time ** 2) / 2

    return {"x": x, "y": y}


def xToTime(x, initialVelocity, alpha):
    return x / (initialVelocity * cos(alpha))


def rangeCalculation(initialVelocity, initialHeight, alpha, gravity):
    A = -1 * gravity / (2 * initialVelocity ** 2 * np.cos(alpha) ** 2)
    B = np.tan(alpha)
    C = initialHeight

    quadraticEquation = [A, B, C]
    roots = np.roots(quadraticEquation)
    return max(roots)


def projectileMotionWithoutResistance(initialVelocity, initialHeight, alpha, gravity):
    # kąty muszą być w radianach
    if (alpha == np.pi / 2):
        height = initialHeight + (initialVelocity ** 2) / (2 * gravity)
        return {"x": 0, "y": height}
        
    elif (alpha == -1 * np.pi / 2):
        return {"x": 0, "y": initialHeight}
    
    else:
        range = rangeCalculation(initialVelocity, initialHeight, alpha, gravity)
        # height = maxHeight(A, B, C, (roots[0] + roots[1]) / 2)

        x = np.linspace(0, range, 1000)
        y = (initialHeight + np.tan(alpha) * x - gravity * x ** 2 / (2 * initialVelocity ** 2 * np.cos(alpha) ** 2))

        return {"x": x, "y": y}

