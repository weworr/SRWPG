from numpy import pi


def UnitConversionS(number, unit):
    if unit == "mm":
        return number*0.001
    elif unit =="cm":
        return number*0.01
    elif unit =="km":
        return number*1000
    else:
        return number


def UnitConversionT(number, unit):
    if unit == "ms":
        return number*1000
    elif unit == "min":
        return number/60
    elif unit == "h":
        return number/360
    return number


def UnitConversionA(number, unit):
    if unit == "°":
        number = number*pi/180
    elif unit == "rad·π":
        number = number*pi
    return number
