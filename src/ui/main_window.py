import tkinter as tk
from tkinter import messagebox, ttk

from src.logic.settings import ALL_SETTINGS

root = tk.Tk()
root.title("CPMA Config Tool")
root.geometry("800x600")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook.Tab", width=200, anchor="center", focuscolor="")
style.configure("TNotebook", background="#f3f3f3")
style.configure("white.TFrame", background="#f3f3f3")
bg_color = style.lookup("TFrame", "background")

style.map(
    "TCombobox",
    fieldbackground=[("readonly", "white")],
    selectbackground=[("readonly", "white")],
    selectforeground=[("readonly", "black")],
)

main_frame = ttk.Frame(root, padding=(10), style="white.TFrame")
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.rowconfigure(1, weight=1)
main_frame.columnconfigure(0, weight=1)


# ADVANCED SETTINGS WINDOW
def open_advanced_settings():
    advanced_settings = tk.Toplevel(root)
    advanced_settings.title("Advanced Settings")
    advanced_settings.geometry("400x300")
    advanced_settings.rowconfigure(0, weight=1)
    advanced_settings.columnconfigure(0, weight=1)

    main_frame = ttk.Frame(advanced_settings, padding=10, style="white.TFrame")
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.rowconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)
    main_frame.rowconfigure(2, weight=1)
    main_frame.columnconfigure(0, weight=1)

    frame1 = ttk.Frame(main_frame, padding=10, relief="ridge")
    frame1.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
    frame1.columnconfigure(0, weight=1)
    ttk.Label(frame1, text="Current CPMA Path").grid(
        row=0, column=0, sticky="ew", pady=(0, 5)
    )
    ttk.Button(frame1, text="Change CPMA Location").grid(row=1, column=0, sticky="ew")

    frame2 = ttk.Frame(main_frame, padding=10, relief="ridge")
    frame2.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
    frame2.columnconfigure(0, weight=1)
    ttk.Button(frame2, text="Install Game Assets").grid(
        row=0, column=0, sticky="ew", pady=(0, 5)
    )
    ttk.Label(
        frame2,
        text="Installs Quake 3 + CPMA files to your APPDATA folder",
        font=("TkDefaultFont", 8, "italic"),
    ).grid(row=1, column=0, sticky="ew")

    frame3 = ttk.Frame(main_frame, padding=10, relief="ridge")
    frame3.grid(row=2, column=0, sticky="nsew")
    frame3.columnconfigure(0, weight=1)
    ttk.Button(frame3, text="Uninstall CPMA Config Tool").grid(
        row=0, column=0, sticky="ew", pady=(0, 5)
    )
    ttk.Label(
        frame3,
        text="Completely removes the Config Tool and associated AppData",
        font=("TkDefaultFont", 8, "italic"),
    ).grid(row=1, column=0, sticky="ew")


# TOP FRAME
top_frame = ttk.Frame(main_frame, padding=10, relief="ridge")
top_frame.grid(row=0, column=0, sticky="nsew")
top_frame.columnconfigure(0, weight=1)


ttk.Label(
    top_frame,
    text="Settings with blank input boxes will default to the value in your own config",
).grid(row=0, column=0, sticky="w")
ttk.Button(top_frame, text="Advanced Settings", command=open_advanced_settings).grid(
    row=0, column=1, sticky="e"
)


# SETTINGS NOTEBOOK
settings_notebook = ttk.Notebook(main_frame)
settings_notebook.grid(row=1, column=0, sticky="nsew", pady=10)
settings_notebook.columnconfigure(0, weight=1)

# On tab change, set focus to the notebook itself instead of the first option_box
def on_tab_change(event):
    settings_notebook.focus_set()
settings_notebook.bind("<<NotebookTabChanged>>", on_tab_change)


# Generates notebook tab titles and contents
frames = []
canvases = []
scrollbars = []
scrollable_frames = []

option_boxes = []
for i, (title, dictionary) in enumerate(ALL_SETTINGS):
    frame = ttk.Frame(settings_notebook)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frames.append(frame)
    settings_notebook.add(frame, text=title)

    canvas = tk.Canvas(frames[i], background=bg_color, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")
    canvases.append(canvas)

    scrollbar = ttk.Scrollbar(frames[i], orient="vertical", command=(canvases[i]).yview)
    scrollbar.grid(row=0, column=1, sticky="nse")
    scrollbars.append(scrollbar)

    scrollable_frame = ttk.Frame(canvases[i], padding=10)
    scrollable_frames.append(scrollable_frame)
    canvases[i].create_window((0, 0), window=scrollable_frames[i], anchor="nw")
    canvases[i].grid(padx=10, pady=(20, 10))

    # scrollable_frame widget generation
    for i2, setting in enumerate(dictionary):
        # generates each setting label
        label = ttk.Label(
            scrollable_frames[i],
            font=("TkDefaultFont", 10, "bold"),
            text=dictionary[setting]["label"],
        )
        label.grid(row=(i2 * 2), column=0, sticky="w")

        # generates each setting description
        desc = ttk.Label(
            scrollable_frames[i], text=dictionary[setting].get("description")
        )
        desc.grid(row=(i2 * 2), column=1, sticky="w", padx=(40, 0))

        # generates each setting option_box
        value = dictionary[setting]["value"]
        if dictionary[setting].get("type") == "discrete":
            option_box = ttk.Combobox(
                scrollable_frames[i],
                values=([""] + dictionary[setting]["options"]),
                state="readonly",
                width=22,
            )
            if value:
                option_box.set(value)
        elif dictionary[setting].get("type") == "bool":
            option_box = ttk.Combobox(scrollable_frames[i], values=["", "0", "1"], state="readonly", width=22)
            if value:
                option_box.set(value)
        elif dictionary[setting].get("type") == "float" or "string" or "int":
            option_box = ttk.Entry(scrollable_frames[i], width=22)
            if value:
                option_box.insert(0, value)
        option_boxes.append((dictionary, setting, option_box))

        # add vertical padding to the option_box unless its the last option_box in a tab
        if i2 == len(dictionary) - 1:
            option_box.grid(row=(i2 * 2) + 1, column=0, sticky="ew")
        else:
            option_box.grid(row=(i2 * 2) + 1, column=0, sticky="ew", pady=(0, 20))

        # generates option_box range and default value for applicable settings
        if dictionary[setting].get("game_default"):
            default = f"Default: {dictionary[setting].get('game_default')}"
            if dictionary[setting].get("min") and dictionary[setting].get("max"):
                range = f"Range: {dictionary[setting].get('min')} to {dictionary[setting].get('max')}"
                label2 = ttk.Label(scrollable_frames[i], text=f"{range}, {default}")
            else:
                label2 = ttk.Label(scrollable_frames[i], text=default)
            label2.grid(row=(i2 * 2) + 1, column=1, sticky="nw", padx=(40, 0))


def save_config():
    for group in option_boxes:
        dictionary = group[0]
        setting = group[1]
        option_box = group[2]

        dictionary[setting]["value"] = option_box.get()
    messagebox.showinfo("Config Saved", "Your config has been saved.")


def clear_inputs():
    if messagebox.askyesno("Clear All", "This will clear all entered values. Continue?"):
        for group in option_boxes:
            option_box = group[2]
            if type(option_box) == ttk.Combobox:
                option_box.current(0)
            elif type(option_box) == ttk.Entry:
                option_box.delete(0, "end")


# BOTTOM FRAME
bottom_frame = ttk.Frame(main_frame, style="white.TFrame")
bottom_frame.grid(row=2, column=0, sticky="nsew")
bottom_frame.columnconfigure(0, weight=1)

left_frame = ttk.Frame(bottom_frame, style="white.TFrame")
left_frame.grid(row=0, column=0, sticky="w")

right_frame = ttk.Frame(bottom_frame, style="white.TFrame")
right_frame.grid(row=0, column=1, sticky="e")

ttk.Button(left_frame, text="Clear Inputs", command=clear_inputs).grid(row=0, column=0)
ttk.Button(right_frame, text="Save Config", command=save_config).grid(
    row=0, column=0, padx=(0, 5)
)
ttk.Button(right_frame, text="Export Config").grid(row=0, column=1, padx=(0, 5))
ttk.Button(right_frame, text="Launch Game").grid(row=0, column=2)


# Sets scrollregion once all widgets are added
for i, frame in enumerate(scrollable_frames):
    scrollable_frames[i].update_idletasks()
    canvases[i].configure(
        yscrollcommand=scrollbars[i].set, scrollregion=canvases[i].bbox("all")
    )


# Allows the user to scroll anywhere in the canvas
def on_mousewheel(event):
    current_tab = settings_notebook.index(settings_notebook.select())
    canvas = canvases[current_tab]
    # Only scroll if cavas is taller than visible area
    if canvas.bbox("all") and canvas.bbox("all")[3] > canvas.winfo_height():
        canvas.yview_scroll(-1 * (event.delta // 120), "units")
    return "break"


root.bind_all("<MouseWheel>", on_mousewheel)
root.unbind_class("TScrollbar", "<MouseWheel>")

root.mainloop()
