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

        whichValueError = " resistance "
        resistance = float(userInputResistance.get())

    except ValueError:
        mbox.showerror("Error", "Wrong" + whichValueError + "value")
        return False

    except SyntaxError:
        mbox.showerror("Error", "Wrong" + whichValueError + "value")
        return False

    if gravity <= 0:
        mbox.showerror("Error", "Gravity can't be lower or equal to 0")
        return False

    if resistance < 0:
        mbox.showerror("Error", "Resistance can't be lower than 0")
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
rightFrame = Frame(window, name="right")
rightFrame.pack(side="right", expand="false", fill="both")

rightBottomFrame = Frame(rightFrame, name="rightbottom")
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

# region Global Variables
LOP = {}  # List of parameters global
cbPoint_value = StringVar()  # Musi być poza funkcją
# endregion

# region Font Styles
fontStyleLabel = tkFont.Font(family="Lucida Grande", size=15)
fontStyleInteractive = tkFont.Font(family="Lucida Grande", size=12)
fontStyleInteractive2 = tkFont.Font(family="Lucida Grande", size=8)
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

# region Resistance
Label(rightTopFrame, text="Resistance: ", font=fontStyleLabel).grid(row=5, column=0)
userInputResistance = Entry(rightTopFrame, width=18, font=fontStyleInteractive, justify="center")
userInputResistance.grid(row=5, column=1, columnspan=2)
# endregion

# region InitialValues
userInputVelocity.insert(END, "2")
userInputHeight.insert(END, "10")
userInputAngle.insert(END, "45")
userInputGravity.insert(END, "9.81")
userInputResistance.insert(END, "0")
#endregion

horizontalLine = Frame(rightFrame, height=1, width=380, bg="black")
horizontalLine.pack()

def ChangeSliderValue():
    ComboboxEvent.slider.set(float(ShowResultsInterface.userInputPoint.get()))


def ShowLabelWithValues(text, row, column, rowspan, columnspan, name):
    try:
        window.nametowidget(name).destroy()
    except KeyError:
        pass
    Label(rightBottomFrame, font=fontStyleInteractive, text=text, name=name.split('.')[2]).\
        grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)


def ComboboxEvent(self):
    if StartUpResultsInterface.cbPoint.get() == 't':
        ComboboxEvent.sliderRange = pmwr.endTime(LOP["velocity"], LOP["height"], LOP["angle"], LOP["gravity"])
    else:
        ComboboxEvent.sliderRange = pmwr.rangeCalculation(LOP["velocity"], LOP["height"], LOP["angle"], LOP["gravity"])
    ComboboxEvent.slider = Scale(rightBottomFrame, from_=0.00, to=ComboboxEvent.sliderRange, orient=HORIZONTAL,
                                        command=ShowValuesOfSlider, digits=4, resolution=0.00000001)

<<<<<<< HEAD
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
    
=======
    ComboboxEvent.slider.grid(row=1, column=1, rowspan=2)

    ShowLabelWithValues("%.2f" % ComboboxEvent.sliderRange,
                        2, 2, 1, 1, "right.rightbottom.range")

>>>>>>> 0daa3ce13cacb5db63e36f962b1325e323877b25

def ShowResultsInterface():
    Label(rightBottomFrame, text="0", font=fontStyleInteractive).grid(row=2, column=0)

    ShowResultsInterface.userInputPoint = Entry(rightBottomFrame, width=8, font=fontStyleInteractive, justify="center")
    ShowResultsInterface.userInputPoint.insert(END, "0.0")
    ShowResultsInterface.userInputPoint.grid(row=2, column=4, sticky="E", padx=3)

    sliderValue = Button(rightBottomFrame, text="Submit", width=8, font=fontStyleInteractive2,
                         command=ChangeSliderValue)
    sliderValue.grid(row=2, column=5)

    Label(rightBottomFrame, text="Velocity:", font=fontStyleLabel).grid(row=3, column=0)
    ShowLabelWithValues(LOP["velocity"], 3, 1, 1, 4, "right.rightbottom.velocity")


def ShowValuesOfSlider(self):
    ShowResultsInterface.userInputPoint.delete(0, END)
    ShowResultsInterface.userInputPoint.insert(END, ComboboxEvent.slider.get())
    if StartUpResultsInterface.cbPoint.get() == 't':
        time = float(ShowResultsInterface.userInputPoint.get())
    else:
        time = pmwr.xToTime(float(ShowResultsInterface.userInputPoint.get()), LOP["velocity"], LOP["angle"])

    ShowLabelWithValues(pmwr.velocity(LOP["velocity"], LOP["angle"], LOP["gravity"], time), 3, 1, 1, 4, "right.rightbottom.velocity")


def StartUpResultsInterface():

    Label(rightBottomFrame, text="Pick point by:", font=fontStyleLabel).grid(row=0, column=0)

    StartUpResultsInterface.cbPoint = ttk.Combobox(rightBottomFrame, textvariable=cbPoint_value, width=3, font=fontStyleInteractive,
                           state="readonly", justify="center")
    StartUpResultsInterface.cbPoint["values"] = ("x", "t")
    StartUpResultsInterface.cbPoint.current(0)
    StartUpResultsInterface.cbPoint.bind("<<ComboboxSelected>>", ComboboxEvent)
    StartUpResultsInterface.cbPoint.grid(row=0, column=1)
    ComboboxEvent(ComboboxEvent)
    ShowResultsInterface()


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

    StartUpResultsInterface()


# region Buttons
save = Button(rightTopFrame, text="Save to File", width=15, font=fontStyleInteractive)
save.grid(row=6, column=0, columnspan=2, padx=15)

enter = Button(rightTopFrame, text="Submit", width=15, font=fontStyleInteractive, command=SubmitButton)
enter.grid(row=6, column=2, columnspan=5, padx=15)
# endregion

Label(rightTopFrame).grid()
window.mainloop()
