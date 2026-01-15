import tkinter as tk
from tkinter import ttk

from src.logic.settings import ALL_SETTINGS

root = tk.Tk()
root.title("CPMA Config Tool")
root.geometry("800x600")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

style = ttk.Style()
style.theme_use('clam')
style.configure("TNotebook.Tab", width=200)


main_frame = ttk.Frame(root, padding=(10))
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.rowconfigure(1, weight=1)
main_frame.columnconfigure(0, weight=1)


# TOP FRAME
top_frame = ttk.Frame(main_frame, padding=10, relief="ridge")
top_frame.grid(row=0, column=0, sticky="nsew")
top_frame.columnconfigure(0, weight=1)


ttk.Label(top_frame, text="Settings with blank input boxes will default to the value in your own config").grid(row=0, column=0, sticky="w")
ttk.Button(top_frame, text="Advanced Settings").grid(row=0, column=1, sticky="e")


# SETTINGS NOTEBOOK
settings_notebook = ttk.Notebook(main_frame)
settings_notebook.grid(row=1, column=0, sticky="nsew", pady=10)
settings_notebook.columnconfigure(0, weight=1)

# Generates notebook tab titles and contents
frames = []
canvases = []
scrollbars = []
scrollable_frames = []
labels = []
for i, (title, _) in enumerate(ALL_SETTINGS):
    frame = ttk.Frame(settings_notebook)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frames.append(frame)
    settings_notebook.add(frame, text=title)

    canvas = tk.Canvas(frames[i])
    canvas.grid(row=0, column=0, sticky="nsew")
    canvases.append(canvas)

    scrollbar = ttk.Scrollbar(frames[i], orient="vertical", command=(canvases[i]).yview)
    scrollbar.grid(row=0, column=1, sticky="nse")
    scrollbars.append(scrollbar)

    scrollable_frame = ttk.Frame(canvases[i], padding=10)
    scrollable_frames.append(scrollable_frame)
    canvases[i].create_window((0, 0), window=scrollable_frames[i], anchor="nw")

    for x in range(100):
        label = ttk.Label(scrollable_frames[i], text=f"Tab {i}, Line {x}")
        labels.append(label)
        label.grid(row=x, column=0)


# BOTTOM FRAME
bottom_frame = ttk.Frame(main_frame)
bottom_frame.grid(row=2, column=0, sticky="e")
bottom_frame.columnconfigure(0, weight=1)

ttk.Button(bottom_frame, text="Save Config").grid(row=0, column=0, padx=(0,5))
ttk.Button(bottom_frame, text="Export Config").grid(row=0, column=1, padx=(0,5))
ttk.Button(bottom_frame, text="Launch Game").grid(row=0, column=2)



# Sets scrollregion once all widgets are added
for i, (title, _) in enumerate(ALL_SETTINGS):
    scrollable_frames[i].update_idletasks()
    canvases[i].configure(yscrollcommand=scrollbars[i].set, scrollregion=canvases[i].bbox("all"))

# Enable mousewheel scrolling anywhere in the Frame
for i, (title, _) in enumerate(ALL_SETTINGS):
    def on_mousewheel(event):
        (canvases[i]).yview_scroll(-1 * (event.delta // 120), "units")
    (canvases[i]).bind_all("<MouseWheel>", on_mousewheel)


root.mainloop()
