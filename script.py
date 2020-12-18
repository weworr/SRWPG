from tkinter import *
import tkinter.font as tkFont
import tkinter.ttk as ttk
import numpy as np
from modules import pmwr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox as mbox
from modules import conversion as conv

XY = pmwr.projectileMotionWithoutResistance(2, np.pi / 4, 10, 2)  # Zwraca słownik X i Y
window = Tk()
window.title("Projectile motion")
window.config(bg="#FFFFFF")

rightFrame = Frame(window)
rightFrame.pack(side="right", expand="false", fill="both")

rightBottomFrame = Frame(rightFrame)
rightBottomFrame.pack(side="bottom")

rightTopFrame = Frame(rightFrame)
rightTopFrame.pack(side="top")

windowWidth = Frame(rightFrame, height=1, width=400)
windowWidth.pack()


fig = plt.Figure()  # deklaracja figury
# tworzenie podziału na wiersze i kolumny, w krotce wybór miejsca
graph = fig.add_subplot()
graph.set_title("Some title")
graph.plot(XY["x"], XY["y"])
canvas = FigureCanvasTkAgg(fig, master=window)  # ustawianie
canvas.draw()
canvas.get_tk_widget().pack(side="left", fill="both", expand="true")

fontStyleLabel = tkFont.Font(family="Lucida Grande", size=15)
fontStyleInteractive = tkFont.Font(family="Lucida Grande", size=12)

Label(rightTopFrame).grid(row=0)

# region Velocity
Label(rightTopFrame, text="Velocity: ", font=fontStyleLabel).grid(row=1, column=0)
userInputVelocity = Entry(rightTopFrame, width=18, font=fontStyleInteractive, justify="center")
userInputVelocity.grid(row=1, column=1, columnspan=2)

cbVelocityS_value = StringVar()
cbVelocityS = ttk.Combobox(rightTopFrame, textvariable=cbVelocityS_value, width=3, font=fontStyleInteractive, state="readonly", justify="center")
cbVelocityS["values"] = ("mm", "cm", "m", "km")
cbVelocityS.current(2)
cbVelocityS.grid(row=1, column=3)

Label(rightTopFrame, text="/", font=fontStyleLabel).grid(row=1, column=4)

cbVelocityT_value = StringVar()
cbVelocityT = ttk.Combobox(rightTopFrame, textvariable=cbVelocityT_value, width=3, font=fontStyleInteractive, state="readonly", justify="center")
cbVelocityT["values"] = ("ms", "s", "min", "h")
cbVelocityT.current(1)
cbVelocityT.grid(row=1, column=5)
# endregion Velocity

# region Height
Label(rightTopFrame, text="Height: ", font=fontStyleLabel).grid(row=2, column=0)
userInputHeight = Entry(rightTopFrame, width=18, font=fontStyleInteractive, justify="center")
userInputHeight.grid(row=2, column=1, columnspan=2)

cbHeight_value = StringVar()
cbHeight = ttk.Combobox(rightTopFrame, textvariable=cbHeight_value, width=3, font=fontStyleInteractive, state="readonly", justify="center")
cbHeight["values"] = ("mm", "cm", "m", "km")
cbHeight.current(2)
cbHeight.grid(row=2, column=3)
# endregion


# region Angle
Label(rightTopFrame, text="Angle: ", font=fontStyleLabel, justify="center").grid(row=3, column=0)
userInputAngle = Entry(rightTopFrame, width=18, font=fontStyleInteractive, justify="center")
userInputAngle.grid(row=3, column=1, columnspan=2)

cbAngle_value = StringVar()
cbAngle = ttk.Combobox(rightTopFrame, textvariable=cbAngle_value, width=5, font=fontStyleInteractive, state="readonly", justify="center")
cbAngle["values"] = ("°", "rad", "rad·π")
cbAngle.current(0)
cbAngle.grid(row=3, column=3, columnspan=2)
# endregion

# region Gravity
Label(rightTopFrame, text="Gravity: ", font=fontStyleLabel).grid(row=4, column=0)
userInputGravity = Entry(rightTopFrame, width=18, font=fontStyleInteractive, justify="center")
userInputGravity.insert(END, "9.80665")
userInputGravity.grid(row=4, column=1, columnspan=2)
Label(rightTopFrame, text="m/s", font=fontStyleLabel).grid(row=4, column=3)
# endregion


userInputVelocity.insert(END, "9.80665")
userInputHeight.insert(END, "9.80665")
userInputAngle.insert(END, "9.80665")


def GetListOfParameters():
    from numpy import pi

    try:
        whichValueError = " velocity "
        velocity = float(userInputVelocity.get())

        whichValueError = " height "
        height = float(userInputHeight.get())

        whichValueError = " angle "
        angle = eval(userInputAngle.get())

        whichValueError = " gravity "
        gravity = float(userInputGravity.get())

    except ValueError:
        mbox.showerror("Error", "Wrong" + whichValueError + "value")
        return False
    except SyntaxError:
        mbox.showerror("Error", "Wrong" + whichValueError + "value")
        return False

    velocitySUnit = cbVelocityS.get()
    velocityTUnit = cbVelocityT.get()
    heightUnit = cbHeight.get()
    angleUnit = cbAngle.get()

    velocity = conv.UnitConversionT(conv.UnitConversionS(velocity, velocitySUnit), velocityTUnit)
    height = conv.UnitConversionS(height, heightUnit)
    try:
        angle = conv.UnitConversionA(angle, angleUnit)
        if -pi / 2 > angle or angle > pi / 2:
            raise ValueError
    except ValueError:
        mbox.showerror("Error", "Wrong angle value, pick value from -90° to 90°")
        return False
    return {"velocity": velocity, "height": height, "angle": angle, "gravity": gravity}


ListOfParameters = {}


def ShowResultsInterface():
    ShowResultsInterface.slider = Scale(rightBottomFrame, from_=0.0, to=10.0, orient=HORIZONTAL, command=ShowValuesOfSlider, digits=4,
                   resolution=0.01)
    Label(rightBottomFrame, text="Velocity", font=fontStyleLabel).grid(row=1, column=0)
    ShowResultsInterface.slider.grid(row=0, column=1)
    return


def ShowValuesOfSlider(self):
    ListOfParameters = GetListOfParameters()
    Label(rightBottomFrame,
          text=pmwr.velocity(ListOfParameters["velocity"], ListOfParameters["angle"], ListOfParameters["gravity"], ShowResultsInterface.slider.get()),
          font=fontStyleInteractive).grid(row=1, column=1)



def SubmitButton():
    ListOfParameters = GetListOfParameters()
    if not ListOfParameters:
        return

    XY = pmwr.projectileMotionWithoutResistance(ListOfParameters["velocity"], ListOfParameters["height"], ListOfParameters["angle"], ListOfParameters["gravity"])
    graph.clear()
    graph.set_title("Some title")
    graph.plot(XY["x"], XY["y"])
    fig.canvas.draw_idle()
    ShowResultsInterface()


# region Buttons
Label(rightTopFrame, text="").grid(row=5, column=0)

save = Button(rightTopFrame, text="Save to File", width=15, font=fontStyleInteractive)
save.grid(row=6, column=0, columnspan=2, padx=15)

enter = Button(rightTopFrame, text="Submit", width=15, font=fontStyleInteractive, command=SubmitButton)
enter.grid(row=6, column=2, columnspan=5, padx=15)
# endregion


Label(rightTopFrame).grid()
horizontalLine = Frame(rightFrame, height=1, width=380, bg="black")
horizontalLine.pack()

window.mainloop()
