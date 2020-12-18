# projectile motion without restiance
import matplotlib.pyplot as plt
import numpy as np

def cos(x):
    if x % (np.pi / 2) == 0:
        return 0
    
    else:
        return np.cos(x)

def sin(x):
    if (x == 0):
        return 0
    
    else:
        return np.sin(x)

def maxHeight(A, B, C, x):
    return A * x ** 2 + B * x + C


def acceleration(gravity):
    xAcceleration = 0
    yAcceleration = -1 * gravity
    acceleration = gravity
    
    return acceleration


def velocity(initialVelocity, alpha, gravity, time):
    xVelocity = initialVelocity * np.cos(alpha)
    yVelocity = initialVelocity * np.sin(alpha) - gravity * time
    velocity = np.sqrt(xVelocity ** 2 + yVelocity ** 2)
    
    return velocity

def cooridnates(initialVelocity, initialHeight, alpha, gravity, time):
    #alpha w radianach
    x = initialVelocity * cos(alpha) * time
    y = initialHeight * sin(alpha) * time - (gravity * time ** 2) / 2

    return {"x": x, "y": y}


def projectileMotionWithoutResistance(initialVelocity, initialHeight, alpha, gravity):
    # kąty muszą być w radianach
    if (alpha == np.pi / 2):    #plt.stem(x,y)
        height = initialHeight + (initialVelocity ** 2) / (2 * gravity)
        return {"x": 0, "y": height}
        
    elif (alpha == -1 * np.pi / 2): #plt.stem(x,y)
        height = initialHeight
        return {"x": 0, "y": initialHeight}
    
    else:
        A = -1 * gravity / (2 * initialVelocity ** 2 * np.cos(alpha) ** 2)
        B = np.tan(alpha)
        C = initialHeight

        quadraticEquation = [A, B, C]
        roots = np.roots(quadraticEquation)
        range = max(roots)
        height = maxHeight(A, B, C, (roots[0] + roots[1]) / 2)

        x = np.linspace(0, range, 1000)
        y = (initialHeight + np.tan(alpha) * x - gravity * x ** 2 / (2 * initialVelocity ** 2 * np.cos(alpha) ** 2))

 # `  plt.plot(x, y)
 #    plt.xlim(0, range + 0.1 * range)
 #    plt.show()

        return {"x": x, "y": y}

