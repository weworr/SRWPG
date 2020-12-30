from tkinter import *
import tkinter.font as tkFont
import tkinter.ttk as ttk
import numpy as np
from modules import pmwr
from modules import pm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox as mbox
from modules import conversion as conv

# List of parameters global
LOP = {}

######################################################
# ERROR HALO, jak sie t ustawi to slider i tak chodzi do max x
######################################################

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

    velocity = conv.unitConversionT(conv.unitConversionS(velocity, velocitySUnit), velocityTUnit)
    height = conv.unitConversionS(height, heightUnit)
    try:
        angle = conv.unitConversionA(angle, angleUnit)
        if -pi / 2 > angle or angle > pi / 2:
            raise ValueError
    except ValueError:
        mbox.showerror("Error", "Wrong angle value, pick value from -90° to 90°")
        return False
    return {"velocity": velocity, "height": height, "angle": angle, "gravity": gravity}


XY = pmwr.projectileMotionWithoutResistance(2, 10, np.pi / 4, 9.81)  # Zwraca słownik X i Y
pm.projectileMotionWithResistance(2, 10, np.pi / 4, 9.81)
window = Tk()
window.title("Projectile motion")
window.config(bg="#FFFFFF")

# region Frames
rightFrame = Frame(window)
rightFrame.pack(side="right", expand="false", fill="both")

rightBottomFrame = Frame(rightFrame)
rightBottomFrame.pack(side="bottom")

rightTopFrame = Frame(rightFrame)
rightTopFrame.pack(side="top")

windowWidth = Frame(rightFrame, height=1, width=400)
windowWidth.pack()
# endregion

# region Graph
fig = plt.Figure()  # deklaracja figury
# tworzenie podziału na wiersze i kolumny, w krotce wybór miejsca
graph = fig.add_subplot()
graph.set_title("Exemplary Graph")
graph.plot(XY["x"], XY["y"])
canvas = FigureCanvasTkAgg(fig, master=window)  # ustawianie
canvas.draw()
canvas.get_tk_widget().pack(side="left", fill="both", expand="true")
# endregion

fontStyleLabel = tkFont.Font(family="Lucida Grande", size=15)
fontStyleInteractive = tkFont.Font(family="Lucida Grande", size=12)
fontStyleInteractive2 = tkFont.Font(family="Lucida Grande", size=8)

# region Global Variables
cbPoint_value = StringVar()  # Musi być poza funkcją
zmienna = Label()  # global
zmienna2 = Label()
# endregion

Label(rightTopFrame).grid(row=0)  # Odstęp od góry okienka

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
userInputGravity.grid(row=4, column=1, columnspan=2)
Label(rightTopFrame, text="m/s", font=fontStyleLabel).grid(row=4, column=3)
# endregion

# region InitialValues
horizontalLine = Frame(rightFrame, height=1, width=380, bg="black")
horizontalLine.pack()

userInputVelocity.insert(END, "2")
userInputHeight.insert(END, "10")
userInputAngle.insert(END, "45")
userInputGravity.insert(END, "9.81")
#endregion

def ChangeSliderValue():
    ShowResultsInterface.slider.set(float(ShowResultsInterface.userInputPoint.get()))


def ShowResultsInterface():
    Label(rightBottomFrame, text="Pick point by:", font=fontStyleLabel).grid(row=0, column=0)

    cbPoint = ttk.Combobox(rightBottomFrame, textvariable=cbPoint_value, width=3, font=fontStyleInteractive,
                            state="readonly", justify="center")
    cbPoint["values"] = ("x", "t")
    cbPoint.current(0)
    cbPoint.grid(row=0, column=1)
    # region Slider
    ShowResultsInterface.userInputPoint = Entry(rightBottomFrame, width=8, font=fontStyleInteractive, justify="center")
    ShowResultsInterface.userInputPoint.insert(END,"0.0")
    ShowResultsInterface.userInputPoint.grid(row=2, column=0, sticky="E", padx=3)

    sliderValue = Button(rightBottomFrame, text="Submit", width=8, font=fontStyleInteractive2, command=ChangeSliderValue)
    sliderValue.grid(row=2, column=1, sticky="W")

    Label(rightBottomFrame, text="").grid(row=2, column=2)

    Label(rightBottomFrame, text="0", font=fontStyleInteractive).grid(row=2, column=3)
    ShowResultsInterface.slider = Scale(rightBottomFrame, from_=0.00,
                                        to=pmwr.rangeCalculation(LOP["velocity"], LOP["height"], LOP["angle"], LOP["gravity"]),
                                        orient=HORIZONTAL, command=ShowValuesOfSlider, digits=4, resolution=0.00000001)
    ShowResultsInterface.slider.grid(row=1, column=4, rowspan=2)

    global zmienna
    zmienna.destroy()
    zmienna = Label(rightBottomFrame, text="%.2f" % pmwr.rangeCalculation(LOP["velocity"], LOP["height"], LOP["angle"], LOP["gravity"]),
          font=fontStyleInteractive)
    zmienna.grid(row=2, column=5)

    global zmienna2
    zmienna2.destroy()
    zmienna2 = Label(rightBottomFrame, text=LOP["velocity"], font=fontStyleInteractive)
    zmienna2.grid(row=3, column=1, columnspan=4)
    

    # endregion

    # region show
    Label(rightBottomFrame, text="Velocity", font=fontStyleLabel).grid(row=3, column=0)


    # endregion


def ShowValuesOfSlider(self):
    ShowResultsInterface.userInputPoint.delete(0, END)
    ShowResultsInterface.userInputPoint.insert(END, ShowResultsInterface.slider.get())
    
    global zmienna2
    zmienna2.destroy()
    zmienna2 = Label(rightBottomFrame, text=pmwr.velocity(LOP["velocity"], LOP["angle"], LOP["gravity"], float(ShowResultsInterface.userInputPoint.get())), font=fontStyleInteractive)
    zmienna2.grid(row=3, column=1, columnspan=4)


def SubmitButton():
    global LOP
    LOP = GetListOfParameters()
    if not LOP:
        return

    XY = pmwr.projectileMotionWithoutResistance(LOP["velocity"], LOP["height"], LOP["angle"], LOP["gravity"])
    if (LOP["angle"] == np.pi / 2):
        graph.clear()
        graph.vlines(x=0, ymin=LOP["height"], ymax=XY["y"], colors="#3383BB")
        fig.canvas.draw_idle()

    elif (LOP["angle"] == -1 * np.pi / 2):
        graph.clear()
        graph.vlines(x=0, ymin=0, ymax=XY["y"], colors="#3383BB")
        fig.canvas.draw_idle()
    else:
        graph.clear()
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
window.mainloop()
