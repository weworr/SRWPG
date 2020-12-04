from tkinter import *
import tkinter.font as tkFont
import tkinter.ttk as ttk
import numpy as np
from modules import pmwr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

XY = pmwr.projectileMotionWithoutResistance(2, np.pi / 4, 10, 100)  # Podaje słownik X i Y

window = Tk()
window.title("Projectile motion")
window.config(bg="#FFFFFF")

# leftFrame = Frame(window)
# leftFrame.grid(row=0, column=0)
rightFrame = Frame(window)
rightFrame.pack(side="right", expand="true", fill="both")

fig = plt.Figure()  # deklaracja figury
graph = (
    fig.add_subplot()
)  # tworzenie podziału na wiersze i kolumny, w krotce wybór miejsca
graph.set_title("Some title")
graph.plot(XY["x"], XY["y"])
canvas = FigureCanvasTkAgg(fig, master=window)  # ustawianie
canvas.draw()

canvas.get_tk_widget().pack(side="left", fill="both", expand="true")

fontStyleLabel = tkFont.Font(family="Lucida Grande", size=15)
fontStyleInteractive = tkFont.Font(family="Lucida Grande", size=12)

# region Velocity
Label(rightFrame, text="Velocity: ", font=fontStyleLabel).grid(row=0, column=0)
userInputVelocity = Entry(rightFrame, width=18, font=fontStyleInteractive)
userInputVelocity.grid(row=0, column=1, columnspan=2)

cbVelocityS_value = StringVar()
cbVelocityS = ttk.Combobox(rightFrame, textvariable=cbVelocityS_value, width=3, font=fontStyleInteractive, state="readonly")
cbVelocityS['values'] = ("mm", "cm", "m", "km")
cbVelocityS.current(2)
cbVelocityS.grid(row=0, column=3)

Label(rightFrame, text="/", font=fontStyleLabel).grid(row=0, column=4)

cbVelocityT_value = StringVar()
cbVelocityT = ttk.Combobox(rightFrame, textvariable=cbVelocityT_value, width=3, font=fontStyleInteractive, state="readonly")
cbVelocityT['values'] = ("ms", "s", "min", "h")
cbVelocityT.current(1)
cbVelocityT.grid(row=0, column=5)
# endregion Velocity

# region Height
Label(rightFrame, text="Height: ", font=fontStyleLabel).grid(row=1, column=0)
userInputHeight = Entry(rightFrame, width=18, font=fontStyleInteractive)
userInputHeight.grid(row=1, column=1, columnspan=2)

cbHeight_value = StringVar()
cbHeight = ttk.Combobox(
    rightFrame,
    textvariable=cbHeight_value,
    width=3,
    font=fontStyleInteractive,
    state="readonly",
)
cbHeight["values"] = ("mm", "cm", "m", "km")
cbHeight.current(2)
cbHeight.grid(row=1, column=3)
# endregion

# region Angle
Label(rightFrame, text="Angle: ", font=fontStyleLabel).grid(row=2, column=0)
userInputAngle = Entry(rightFrame, width=18, font=fontStyleInteractive)
userInputAngle.grid(row=2, column=1, columnspan=2)

cbAngle_value = StringVar()
cbAngle = ttk.Combobox(rightFrame, textvariable=cbAngle_value, width=3, font=fontStyleInteractive, state="readonly")
cbAngle['values'] = ("°", "rad")
cbAngle.current(0)
cbAngle.grid(row=2, column=3)
# endregion

# region Gravity
Label(rightFrame, text="Gravity: ", font=fontStyleLabel).grid(row=3, column=0)
userInputAngle = Entry(rightFrame, width=18, font=fontStyleInteractive)
userInputAngle.grid(row=3, column=1, columnspan=2)
Label(rightFrame, text="m/s", font=fontStyleLabel).grid(row=3, column=3)
# endregion

# region Buttons
Label(rightFrame, text="").grid(row=4, column=0)

save = Button(rightFrame, text="Save to File", width=15, font=fontStyleInteractive)
save.grid(row=5, column=0, columnspan=2, padx=15)

enter = Button(rightFrame, text="Enter", width=15, font=fontStyleInteractive)
enter.grid(row=5, column=2, columnspan=5, padx=15)
# endregion


# window.geometry("1920x1080") rozmiar okna
window.mainloop()