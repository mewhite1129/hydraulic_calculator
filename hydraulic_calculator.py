import math
from tkinter import font
from turtle import fill

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

    root.configure(bg=BG)

    def label(parent, text, **kw):
        return tk.Label(
            parent, 
            text=text, 
            bg=kw.pop("bg", CARD), 
            fg=kw.pop("fg", TEXT), 
            font=kw.pop("font", FONT), 
            **kw
            )
    
    def entry(parent):
        e = tk.Entry(
            parent, 
            bg="#323757", 
            fg=TEXT, 
            font=FONT, 
            insertbackground=ACCENT,
            relief="flat",
            width=14,
            highlightthickness=1,
            highlightcolor=ACCENT,
            highlightbackground=MUTED
            )
        
        return e

# TITLE BAR
title_bar = tk.Frame(root, bg=ACCENT, pady=8)
title_bar.pack(fill="x")
tk.Label(
    title_bar, 
    text="Hydraulic Cylinder Calculator",
    bg=ACCENT,
    fg="#0d1117",
    font=("SEGOE UI", 13, "bold")
).pack()

# INPUT CARD
card = tk.Frame(root, bg=CARD, padx=24, pady=20)
card.pack(padx=16, pady=(14, 6), fill="x")

fields = [
    ("Bore Diameter (in)", "in", "e.g. 4.0"),
    ("Rod Diameter (in)", "in", "e.g. 2.5"),
    ("Pressure (psi)", "PSI", "e.g. 2500"),
    ("Flow Rate (gpm)", "GPM", "e.g. 10"),
]

entries = []

label(card, text="INPUTS", bg=CARD, fg=ACCENT, font=("Segoe UI", 8, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

for i, (name, unit, hint) in enumerate(fields):
    label(card, f"{name}", bg=CARD).grid(row=i+1, column=0, sticky="w", pady=5)
    e = entry(card)
    e.insert(0, hint)
    e.config(fg=MUTED)

    def on_focus_in(ev, widget=e, placeholder=hint):
            if widget.get() == placeholder:
                widget.delete(0, "end")
                widget.config(fg=TEXT)

    def on_focus_out(ev, widget=e, placeholder=hint):
        if widget.get() == "":
            widget.insert(0, placeholder)
            widget.config(fg=MUTED)

    e.bind("<FocusIn>",  on_focus_in)
    e.bind("<FocusOut>", on_focus_out)
    e.grid(row=i+1, column=1, padx=10, pady=5)
    label(card, unit, bg=CARD, fg=MUTED).grid(row=i+1,column=2, sticky="w")
    entries.append(e)

    bore_e, rod_e, pres_e, flow_e = entries

    