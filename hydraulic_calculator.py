import math

def calculate(bore_in, rod_in, pressure_psi, flow_gpm):
    """
    Returns extend/retract force (lbf) and speed (in/min).
    flow_gpm: gallons per minute → convert to in³/min (1 gal = 231 in³)
    """
    bore_area  = math.pi * (bore_in / 2) ** 2        # in²
    rod_area   = math.pi * (rod_in  / 2) ** 2        # in²
    annulus    = bore_area - rod_area                  # in² (retract side)
    flow_in3   = flow_gpm * 231                        # in³/min

    extend_force  = pressure_psi * bore_area           # lbf
    retract_force = pressure_psi * annulus             # lbf
    extend_speed  = flow_in3 / bore_area               # in/min
    retract_speed = flow_in3 / annulus                 # in/min

    return extend_force, retract_force, extend_speed, retract_speed

import tkinter as tk
from tkinter import ttk

def run_gui():
    root = tk.Tk()
    root.title("Hydraulic Cylinder Calculator")
    root.resizable(False, False)

    # STYLES
    BG      = "#1e2130"
    CARD    = "#272b3d"
    ACCENT  = "#4fc3f7"
    TEXT    = "#e0e6f0"
    MUTED   = "#8a93b0"
    GREEN   = "#69f0ae"
    YELLOW  = "#ffd740"
    FONT    = ("Segoe UI", 10)
    BOLD    = ("Segoe UI", 10, "bold")
    HEAD    = ("Segoe UI", 13, "bold")