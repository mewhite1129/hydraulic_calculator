import math
import tkinter as tk
from tkinter import messagebox


def calculate(bore_in, rod_in, pressure_psi, flow_gpm):
    """
    Returns extend/retract force (lbf) and speed (in/min),
    plus bore_area and annulus_area for display purposes.

    flow_gpm: gallons per minute → convert to in³/min (1 gal = 231 in³)
    """
    bore_area = math.pi * (bore_in / 2) ** 2  # in²
    rod_area = math.pi * (rod_in / 2) ** 2  # in²
    annulus_area = bore_area - rod_area  # in² (retract side)
    flow_in3 = flow_gpm * 231  # in³/min

    extend_force = pressure_psi * bore_area  # lbf
    retract_force = pressure_psi * annulus_area  # lbf
    extend_speed = flow_in3 / bore_area  # in/min
    retract_speed = flow_in3 / annulus_area  # in/min

    return (
        extend_force,
        retract_force,
        extend_speed,
        retract_speed,
        bore_area,
        annulus_area,
    )


def run_gui():
    root = tk.Tk()
    root.title("Hydraulic Cylinder Calculator")
    root.resizable(False, False)

    # STYLES
    bg_color = "#1e2130"
    card_color = "#272b3d"
    accent_color = "#4fc3f7"
    text_color = "#e0e6f0"
    muted_color = "#8a93b0"
    green_color = "#69f0ae"
    yellow_color = "#ffd740"
    font_normal = ("Segoe UI", 10)
    font_bold = ("Segoe UI", 10, "bold")
    font_small = ("Segoe UI", 8)
    font_heading = ("Segoe UI", 8, "bold")

    root.configure(bg=bg_color)

    def make_label(parent, text, **kw):
        return tk.Label(
            parent,
            text=text,
            bg=kw.pop("bg", card_color),
            fg=kw.pop("fg", text_color),
            font=kw.pop("font", font_normal),
            **kw,
        )

    def make_entry(parent):
        return tk.Entry(
            parent,
            bg="#323757",
            fg=text_color,
            font=font_normal,
            insertbackground=accent_color,
            relief="flat",
            width=14,
            highlightthickness=1,
            highlightcolor=accent_color,
            highlightbackground=muted_color,
        )

    def bind_placeholder(entry_widget, placeholder):
        def on_focus_in(_event):
            if entry_widget.get() == placeholder:
                entry_widget.delete(0, "end")
                entry_widget.config(fg=text_color)

        def on_focus_out(_event):
            if entry_widget.get() == "":
                entry_widget.insert(0, placeholder)
                entry_widget.config(fg=muted_color)

        entry_widget.bind("<FocusIn>", on_focus_in)
        entry_widget.bind("<FocusOut>", on_focus_out)

    # TITLE BAR
    title_bar = tk.Frame(root, bg=accent_color, pady=8)
    title_bar.pack(fill="x")
    tk.Label(
        title_bar,
        text="Hydraulic Cylinder Calculator",
        bg=accent_color,
        fg="#0d1117",
        font=font_bold,
    ).pack()

    # INPUT CARD
    card = tk.Frame(root, bg=card_color, padx=24, pady=20)
    card.pack(padx=16, pady=(14, 6), fill="x")

    fields = [
        ("Bore Diameter (in)", "in", "e.g. 4.0"),
        ("Rod Diameter (in)", "in", "e.g. 2.5"),
        ("Pressure (psi)", "PSI", "e.g. 2500"),
        ("Flow Rate (gpm)", "GPM", "e.g. 10"),
    ]

    entries = []

    make_label(card, "INPUTS", bg=card_color, fg=accent_color, font=font_heading).grid(
        row=0, column=0, columnspan=3, sticky="w", pady=(0, 10)
    )

    placeholders = [field[2] for field in fields]

    for i, (name, unit, hint) in enumerate(fields):
        make_label(card, name, bg=card_color).grid(
            row=i + 1, column=0, sticky="w", pady=5
        )
        e = make_entry(card)
        e.insert(0, hint)
        e.config(fg=muted_color)
        bind_placeholder(e, hint)
        e.grid(row=i + 1, column=1, padx=10, pady=5)
        make_label(card, unit, bg=card_color, fg=muted_color).grid(
            row=i + 1, column=2, sticky="w"
        )
        entries.append(e)

    # RESULTS CARD
    res_card = tk.Frame(root, bg=card_color, padx=24, pady=16)
    res_card.pack(padx=16, pady=6, fill="x")

    make_label(
        res_card, "RESULTS", bg=card_color, fg=accent_color, font=font_heading
    ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

    result_data = [
        ("Extend Force", green_color, "lbf"),
        ("Retract Force", yellow_color, "lbf"),
        ("Extend Speed", green_color, "in/min"),
        ("Retract Speed", yellow_color, "in/min"),
    ]
    result_vars = [tk.StringVar(value="—") for _ in result_data]

    for i, ((name, color, unit), var) in enumerate(zip(result_data, result_vars)):
        make_label(res_card, name, bg=card_color, fg=muted_color).grid(
            row=i + 1, column=0, sticky="w", pady=4
        )
        tk.Label(
            res_card,
            textvariable=var,
            bg=card_color,
            fg=color,
            font=("Segoe UI", 11, "bold"),
            width=12,
            anchor="e",
        ).grid(row=i + 1, column=1, padx=10)
        make_label(res_card, unit, bg=card_color, fg=muted_color).grid(
            row=i + 1, column=2, sticky="w"
        )

    # INFO LINE
    info_var = tk.StringVar(value="")
    tk.Label(
        res_card, textvariable=info_var, bg=card_color, fg=muted_color, font=font_small
    ).grid(row=6, column=0, columnspan=3, sticky="w", pady=(10, 0))

    # CALCULATE BUTTON LOGIC
    def on_calculate():
        try:
            vals = []
            for e, ph in zip(entries, placeholders):
                raw = e.get().strip()
                if raw == ph:
                    raise ValueError("Fill in all fields.")
                vals.append(float(raw))

            bore, rod, pres, flow = vals

            if rod >= bore:
                raise ValueError("Rod diameter must be less than bore diameter.")
            if any(v <= 0 for v in vals):
                raise ValueError("All values must be positive.")

            ef, rf, es, rs, bore_area, annulus_area = calculate(bore, rod, pres, flow)
            flow_in3 = flow * 231

            result_vars[0].set(f"{ef:,.1f}")
            result_vars[1].set(f"{rf:,.1f}")
            result_vars[2].set(f"{es:,.2f}")
            result_vars[3].set(f"{rs:,.2f}")

            info_var.set(
                f"Bore Area: {bore_area:.3f} in²  |  "
                f"Annulus Area: {annulus_area:.3f} in²  |  "
                f"Flow: {flow_in3:.1f} in³/min"
            )

        except ValueError as ex:
            messagebox.showerror("Input Error", str(ex))

    def on_clear():
        for v in result_vars:
            v.set("—")
        info_var.set("")

    # BUTTONS
    btn_frame = tk.Frame(root, bg=bg_color, pady=10)
    btn_frame.pack()

    tk.Button(
        btn_frame,
        text="Calculate",
        bg=accent_color,
        fg="#0d1117",
        font=font_bold,
        relief="flat",
        padx=20,
        pady=8,
        command=on_calculate,
        cursor="hand2",
        activebackground="#81d4fa",
        activeforeground="#0d1117",
    ).pack(side="left", padx=6)

    tk.Button(
        btn_frame,
        text="Clear",
        bg=card_color,
        fg=muted_color,
        font=font_normal,
        relief="flat",
        padx=14,
        pady=8,
        command=on_clear,
        cursor="hand2",
    ).pack(side="left", padx=6)

    root.bind("<Return>", lambda event: on_calculate())

    # FOOTER
    tk.Label(
        root,
        text="Units: inches · PSI · GPM → lbf · in/min",
        bg=bg_color,
        fg=muted_color,
        font=font_small,
    ).pack(pady=(0, 10))

    root.mainloop()


if __name__ == "__main__":
    run_gui()
