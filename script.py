from tkinter import *
import numpy as np
from modules import pmwr
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# pmwr.projectileMotionWithoutResistance(2, np.pi / 4, 10, 5)

window = Tk()
window.title("Projectile motion")

label = Label(
    window,
    text="XDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
)
label.pack()
# window.geometry("1920x1080") rozmiar okna
window.mainloop()