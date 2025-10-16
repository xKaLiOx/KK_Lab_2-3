import matplotlib.pyplot as plt
import KK_Lab2_GLOBALS as globals
import numpy as np
import tkinter as Tk

from KK_Lab2_FUNCTIONS import GUI_Exit

A = [1,2,4,4,56,6,7,7,5,54,42,24]
print(A)

fig = plt.figure()
ax = fig.add_subplot(111)
ploter = ax.scatter([1],[1])
ploter.set_data(np.arange(len(A)),A)
plt.ion()
print(A[-40:])
