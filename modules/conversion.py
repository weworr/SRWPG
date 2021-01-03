import numpy as np


def unitConversionS(number, unit):
    if unit == "mm":
        return number*0.001
    elif unit =="cm":
        return number*0.01
    elif unit =="km":
        return number*1000
    else:
        return number


def unitConversionT(number, unit):
    if unit == "ms":
        return number*1000
    elif unit == "min":
        return number/60
    elif unit == "h":
        return number/360
    return number


def unitConversionA(number, unit):
    if unit == "°":
        number = number*np.pi/180
    elif unit == "rad·π":
        number = number*np.pi
    return number

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