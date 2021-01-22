from modules import pmwr as mode
from modules import conversion as conv

from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory, askopenfilename

from numpy import pi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import os


def ShowLabel(text, name, row, column, rowspan, columnspan, width=19):
    """
    :return: Grids label with given parameters, on given position.
    """
    try:
        window.nametowidget(name).destroy()
    except KeyError:
        pass
    Label(rightBottomFrame, font=fontStyleInteractiveMedium, text=text, name=name.split('.')[2], width=width). \
        grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky='w')


def GetListOfParameters():
    """
    Gets values from entries, checks if correct values were entered,
    and converts them if it is needed.
    Also generates dictionary from those values.

    :return: False - if user input isn't correct, True - otherwise.
    """

    try:
        whichValueError = " velocity "
        velocity = float(userInputVelocity.get())

        if velocity < 0:
            messagebox.showerror("Error", "Velocity can't be lower than 0")

        whichValueError = " height "
        height = float(userInputHeight.get())

        if height < 0:
            messagebox.showerror("Error", "Height can't be lower than 0")

        whichValueError = " angle "
        angle = eval(userInputAngle.get())

        whichValueError = " gravity "
        gravity = float(userInputGravity.get())

        if gravity <= 0:
            messagebox.showerror("Error", "Gravity can't be lower or equal to 0")
            return False

        whichValueError = " resistance "
        resistance = float(userInputResistance.get())

        if resistance < 0:
            messagebox.showerror("Error", "Resistance can't be lower than 0")
            return False

    except (ValueError, SyntaxError, NameError):
        messagebox.showerror("Error", "Wrong" + whichValueError + "value")
        return False

    global mode
    if resistance > 0:
        modules = __import__('modules.pm', globals(), locals())
        mode = modules.pm
    else:
        modules = __import__('modules.pmwr', globals(), locals())
        mode = modules.pmwr

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
        if angleUnit == '°':
            whichValueError = "-90° to 90°"
        elif angleUnit == 'rad':
            whichValueError = "-π/2 to π/2"
        else:
            whichValueError = "-1/2 to 1/2"
        messagebox.showerror("Error", "Wrong angle value, pick value from "+whichValueError)
        return False

    return {"velocity": velocity, "height": height, "angle": angle, "gravity": gravity, "resistance": resistance}


def ChangeSliderValue():
    """
    Changes slider position if entry was submitted
    """
    try:
        ComboboxEvent.slider.set(float(ResultsInterface.userInputPoint.get()))
    except ValueError:
        messagebox.showerror("Error", "Wrong input value")


def ComboboxEvent(self):
    """
    Generates slider of X or time.
    """
    if ResultsInterface.cbPoint.get() == 't':
        ComboboxEvent.sliderRange = mode.endTimeCalculation(LOP["velocity"], LOP["height"], LOP["angle"],
                                                            LOP["gravity"])
    else:
        ComboboxEvent.sliderRange = mode.rangeCalculation(LOP["velocity"], LOP["height"], LOP["angle"], LOP["gravity"],
                                                          LOP["resistance"])

    ComboboxEvent.slider = Scale(rightBottomFrame, from_=0.00, to=ComboboxEvent.sliderRange, orient=HORIZONTAL,
                                 width=13, length=150, command=ShowValuesOfSlider, digits=8, resolution=0.0000000000001)

    ComboboxEvent.slider.grid(row=6, column=1, rowspan=2, columnspan=2)
    ShowLabel("%.2f" % ComboboxEvent.sliderRange, "right.rightbottom.range", 7, 3, 1, 1, 3)


def ShowValuesOfSlider(self):
    """
    Shows point values of params: (V, Vx, Vy, H, t, X)
    Using slider real time value
    """
    ResultsInterface.userInputPoint.delete(0, END)
    ResultsInterface.userInputPoint.insert(END, ComboboxEvent.slider.get())
    if ResultsInterface.cbPoint.get() == 't':
        time = float(ResultsInterface.userInputPoint.get())
    else:
        time = mode.xToTime(float(ResultsInterface.userInputPoint.get()), LOP["velocity"], LOP["angle"],
                            LOP["resistance"])

    velocity = mode.velocity(LOP["velocity"], LOP["angle"], LOP["gravity"], time, LOP["resistance"])
    # Point Velocity
    ShowLabel(velocity["velocity"], "right.rightbottom.velocity", 9, 2, 1, 4)
    # Point X Velocity
    ShowLabel(velocity["xvelocity"], "right.rightbottom.xvelocity", 10, 2, 1, 4)
    # Point Y Velocity
    ShowLabel(velocity["yvelocity"], "right.rightbottom.yvelocity", 11, 2, 1, 4)
    # Point Height
    ShowLabel(mode.yPoint(LOP["velocity"], LOP["height"], LOP["angle"], LOP["gravity"], time, LOP["resistance"]),
              "right.rightbottom.height", 12, 2, 1, 4)
    # Point Time
    ShowLabel(time, 'right.rightbottom.time', 13, 2, 1, 4)
    # Point X
    ShowLabel(mode.xPoint(LOP["velocity"], LOP["angle"], time, LOP["resistance"]), "right.rightbottom.x", 14, 2, 1, 4)


def ResultsInterface():
    """
    Function showing combobox and constant labels
    """
    # region Results Interface Combobox
    Label(rightBottomFrame).grid(row=4)
    Label(rightBottomFrame, text="Pick point by:", font=fontStyleLabelMedium).grid(row=5, column=0, columnspan=2)

    ResultsInterface.cbPoint = ttk.Combobox(rightBottomFrame, textvariable=cbPoint_value, width=3,
                                            font=fontStyleInteractiveSmall,
                                            state="readonly", justify="center")
    ResultsInterface.cbPoint["values"] = ("x", "t")
    ResultsInterface.cbPoint.current(0)
    ResultsInterface.cbPoint.bind("<<ComboboxSelected>>", ComboboxEvent)
    ResultsInterface.cbPoint.grid(row=5, column=2, sticky='w')
    ComboboxEvent(ComboboxEvent)
    Label(rightBottomFrame, text="0", font=fontStyleInteractive).grid(row=7, column=0, sticky='e')
    # endregion

    restart = Button(rightBottomFrame, text="Restart", width=5, font=fontStyleInteractiveMedium, command=RestartButton)
    restart.grid(row=0, column=3, sticky='w')

    # region Results Interface Vertex
    ResultsInterface.vertex = mode.vertex(LOP["velocity"], LOP["height"], LOP["angle"], LOP["gravity"],
                                          LOP["resistance"])

    Label(rightBottomFrame, text="Vertex values:", font=fontStyleLabelMedium).grid(row=0, column=0, columnspan=2)
    # Vertex X
    Label(rightBottomFrame, text="X:", font=fontStyleLabelMedium).grid(row=1, column=0, columnspan=2)
    ShowLabel(ResultsInterface.vertex['x'], "right.rightbottom.vertexx", 1, 2, 1, 1)
    # Vertex Y
    Label(rightBottomFrame, text="Y:", font=fontStyleLabelMedium).grid(row=2, column=0, columnspan=2)
    ShowLabel(ResultsInterface.vertex['y'], "right.rightbottom.vertexy", 2, 2, 1, 2)
    # Vertex T
    Label(rightBottomFrame, text="Time :", font=fontStyleLabelMedium).grid(row=3, column=0, columnspan=2)
    ShowLabel(ResultsInterface.vertex['t'], "right.rightbottom.vertext", 3, 2, 1, 1)
    # endregion

    # region Interactive Results Interface
    ResultsInterface.userInputPoint = Entry(rightBottomFrame, width=15, font=fontStyleInteractive, justify="center")
    ResultsInterface.userInputPoint.insert(END, "0.0")
    ResultsInterface.userInputPoint.grid(row=8, column=1, columnspan=2)

    sliderValue = Button(rightBottomFrame, text="Submit", width=8, font=fontStyleInteractiveSmall,
                         command=ChangeSliderValue)
    sliderValue.grid(row=8, column=3, sticky='w')

    # region Initial Values
    # Initial Velocity
    Label(rightBottomFrame, text="Velocity:", font=fontStyleLabelMedium).grid(row=9, column=0, columnspan=2)
    ShowLabel(LOP["velocity"], "right.rightbottom.velocity", 9, 2, 1, 4)

    # Initial X Velocity
    Label(rightBottomFrame, text="Velocity X:", font=fontStyleLabelMedium).grid(row=10, column=0, columnspan=2)
    ShowLabel(LOP["velocity"] * conv.cos(LOP["angle"]), "right.rightbottom.xvelocity", 10, 2, 1, 4)

    # Initial Y Velocity
    Label(rightBottomFrame, text="Velocity Y:", font=fontStyleLabelMedium).grid(row=11, column=0, columnspan=2)
    ShowLabel(LOP["velocity"] * conv.sin(LOP["angle"]), "right.rightbottom.yvelocity", 11, 2, 1, 4)

    # Initial Height
    Label(rightBottomFrame, text="Height:", font=fontStyleLabelMedium).grid(row=12, column=0, columnspan=2)
    ShowLabel(LOP["height"], "right.rightbottom.height", 12, 2, 1, 4)

    # Initial Time
    Label(rightBottomFrame, text="Time:", font=fontStyleLabelMedium).grid(row=13, column=0, columnspan=2)
    ShowLabel("0.00", "right.rightbottom.time", 13, 2, 1, 4)

    # Initial X
    Label(rightBottomFrame, text="X:", font=fontStyleLabelMedium).grid(row=14, column=0, columnspan=2)
    ShowLabel("0.00", "right.rightbottom.x", 14, 2, 1, 4)
    # endregion
    # endregion


def SubmitButton():
    """
    Submit button on click function
    """
    global LOP
    LOP = GetListOfParameters()
    if not LOP:
        return

    saveOrLoad = Button(rightTopFrame, text="Save to File", width=15, font=fontStyleInteractive, command=SaveButton)
    saveOrLoad.grid(row=6, column=0, columnspan=2, padx=15)

    XY = mode.calculateFunctionGraph(LOP["velocity"], LOP["height"], LOP["angle"], LOP["gravity"], LOP["resistance"])
    if (LOP["angle"] == pi / 2):
        graph.clear()
        graph.vlines(x=0, ymin=0, ymax=XY["y"], colors="#3383BB")
        fig.canvas.draw_idle()

    elif (LOP["angle"] == -1 * pi / 2):
        graph.clear()
        graph.vlines(x=0, ymin=0, ymax=XY["y"], colors="#3383BB")
        fig.canvas.draw_idle()

    else:
        graph.clear()
        graph.plot(XY["x"], XY["y"])
        fig.canvas.draw_idle()

    ResultsInterface()


def LoadButton():
    """
    Load button on click function,
    loads params from a file.
    """
    path = askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=[("Text files", "*.txt")])

    try:
        with open(path, "r") as file:
            for lineNum in range(0, 5):
                values = file.readline().split(" ")
                values[-1] = values[-1].split("\n")[0]

                LOE[lineNum].delete(0, END)
                LOE[lineNum].insert(0, values[1])

                if lineNum == 0:
                    cbVelocityS.current(cbVelocityS["values"].index(values[2]))
                    cbVelocityT.current(cbVelocityT["values"].index(values[3]))
                elif lineNum == 1:
                    cbHeight.current(cbHeight["values"].index(values[2]))
                elif lineNum == 2:
                    cbAngle.current(cbAngle["values"].index(values[2]))
    except FileNotFoundError:
        return
    SubmitButton()


def SaveButton():
    """
    Save button on click function,
    saves user inputs to a file and graph image.
    """
    savedir = askdirectory(initialdir=os.getcwd(), title='Select folder to save results')
    try:
        os.mkdir(savedir + "/PMS")
    except FileExistsError:
        pass

    from glob import glob
    i = 1
    fileName = "GraphData"
    while 1:
        try:
            glob(savedir + "/PMS" + "/" + fileName + ".txt")[0]
        except IndexError:
            file = open(savedir + "/PMS" + "/" + fileName + ".txt", "w")
            fig.savefig(savedir + "/PMS/" + fileName + ".png", dpi=72)
            file.write("Velocity: " + userInputVelocity.get() + " " + cbVelocityS.get() + " " + cbVelocityT.get() +
                       "\nHeight: " + userInputHeight.get() + " " + cbHeight.get() +
                       "\nAngle: " + userInputAngle.get() + " " + cbAngle.get() +
                       "\nGravity: " + userInputGravity.get() +
                       "\nResistance: " + userInputResistance.get() +
                       "\n\nVertex: " +
                       "\nx = " + str(ResultsInterface.vertex['x']) +
                       "\ny = " + str(ResultsInterface.vertex['y']) +
                       "\ntime = " + str(ResultsInterface.vertex['t']))
            break
        fileName = fileName.split('(')[0] + "(" + str(i) + ")"
        i += 1


def RestartButton():
    """
    Restart button on click function,
    Restarts program.
    """
    import sys
    python = sys.executable
    os.execl(python, python, *sys.argv)


# region Window & Frames
window = Tk()
window.title("Projectile motion")
window.config(bg="#FFFFFF")

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
XY = mode.calculateFunctionGraph(2, 10, pi / 4, 9.81, 0)
fig = plt.Figure()
graph = fig.add_subplot()
graph.set_title("Exemplary Graph")
graph.plot(XY["x"], XY["y"])
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side="left", fill="both", expand="true")
# endregion

# region Global Variables
LOP = {}  # Fullname: List of parameters, global dictionary
cbPoint_value = StringVar()  # Must be outside of function
LOE = []  # list of entries (needed to loadfromfile)
# endregion

# region Font Styles
fontStyleLabel = tkFont.Font(family="Lucida Grande", size=12, weight='bold')
fontStyleLabelMedium = tkFont.Font(family="Lucida Grande", size=11, weight='bold')

fontStyleInteractive = tkFont.Font(family="Lucida Grande", size=10)
fontStyleInteractiveMedium = tkFont.Font(family="Lucida Grande", size=10)
fontStyleInteractiveSmall = tkFont.Font(family="Lucida Grande", size=8)
# endregion

Label(rightTopFrame).grid(row=0)

# region Interface
# region Velocity
Label(rightTopFrame, text="Velocity: ", font=fontStyleLabel).grid(row=1, column=0)
userInputVelocity = Entry(rightTopFrame, width=18, font=fontStyleInteractive, justify="center")
userInputVelocity.grid(row=1, column=1, columnspan=2)
LOE.append(userInputVelocity)

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
LOE.append(userInputHeight)

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
LOE.append(userInputAngle)

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
LOE.append(userInputGravity)

Label(rightTopFrame, text="m/s", font=fontStyleLabel).grid(row=4, column=3)
# endregion

# region Resistance
Label(rightTopFrame, text="Resistance: ", font=fontStyleLabel).grid(row=5, column=0)
userInputResistance = Entry(rightTopFrame, width=18, font=fontStyleInteractive, justify="center")
userInputResistance.grid(row=5, column=1, columnspan=2)
LOE.append(userInputResistance)
# endregion
# endregion

# region InitialValues
userInputVelocity.insert(END, "2")
userInputHeight.insert(END, "10")
userInputAngle.insert(END, "45")
userInputGravity.insert(END, "9.81")
userInputResistance.insert(END, "0")
#endregion

# region Buttons
saveOrLoad = Button(rightTopFrame, text="Load from File", width=15, font=fontStyleInteractive, command=LoadButton)
saveOrLoad.grid(row=6, column=0, columnspan=2, padx=15)

enter = Button(rightTopFrame, text="Submit", width=15, font=fontStyleInteractive, command=SubmitButton)
enter.grid(row=6, column=2, columnspan=5, padx=15)
# endregion

# Results Interface

horizontalLine = Frame(rightFrame, height=1, width=380, bg="black")
horizontalLine.pack()

Label(rightTopFrame).grid()
window.mainloop()
