import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("CPMA Config Tool")
root.geometry("800x600")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

#style = ttk.Style()
#style.theme_use('clam')

main_frame = ttk.Frame(root, padding=(10))
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.rowconfigure(1, weight=1)
main_frame.columnconfigure(0, weight=1)


# TOP FRAME
top_frame = ttk.Frame(main_frame, padding=10, relief="solid")
top_frame.grid(row=0, column=0, sticky="nsew")
top_frame.columnconfigure(0, weight=1)


ttk.Label(top_frame, text="Settings with blank input boxes will default to the value in your own config").grid(row=0, column=0, sticky="w")
ttk.Button(top_frame, text="Advanced Settings").grid(row=0, column=1, sticky="e")


# SETTINGS NOTEBOOK
settings_notebook = ttk.Notebook(main_frame)
settings_notebook.grid(row=1, column=0, sticky="nsew", pady=10)

f1 = ttk.Frame(settings_notebook)
f2 = ttk.Frame(settings_notebook)

f1.rowconfigure(0, weight=1)
f1.columnconfigure(0, weight=1)

f2.rowconfigure(0, weight=1)
f2.columnconfigure(0, weight=1)

canvas1 = tk.Canvas(f1)
canvas2 = tk.Canvas(f2)
canvas1.grid(row=0, column=0, sticky="nsew")
canvas2.grid(row=0, column=0, sticky="nsew")
settings_notebook.columnconfigure(0, weight=1)

scrollbar1 = ttk.Scrollbar(f1, orient="vertical", command=canvas1.yview)
scrollbar2 = ttk.Scrollbar(f2, orient="vertical", command=canvas2.yview)
scrollbar1.grid(row=0, column=1, sticky="nse")
scrollbar2.grid(row=0, column=1, sticky="nse")

scrollable_frame1 = ttk.Frame(canvas1, padding=10)
scrollable_frame2 = ttk.Frame(canvas2, padding=10)

canvas1.create_window((0, 0), window=scrollable_frame1, anchor="nw")
canvas2.create_window((0, 0), window=scrollable_frame2, anchor="nw")

label1 = ttk.Label(scrollable_frame1, text="Line 1\nLine 2\n\n\nLine 3\n\n\nLine 4\n\n\nLine 5\n\n\nLine 1\n\n\nLine 2\n\n\nLine 3\n\n\nLine 4\n\n\nLine 5\n\n\nLine 1\n\n\nLine 2\n\n\nLine 3\n\n\nLine 4\n\n\nLine 5\n\n\nLine 1\n\n\nLine 2\n\n\nLine 3\n\n\nLine 4\n\n\nLast Line").grid(row=0, column=0)
label2 = ttk.Label(scrollable_frame2, text="Tab 2").grid(row=0, column=0)

settings_notebook.add(f1, text='One')
settings_notebook.add(f2, text='Two')


# BOTTOM FRAME
bottom_frame = ttk.Frame(main_frame)
bottom_frame.grid(row=2, column=0, sticky="e")
bottom_frame.columnconfigure(0, weight=1)

ttk.Button(bottom_frame, text="Save Config").grid(row=0, column=0, padx=(0,5))
ttk.Button(bottom_frame, text="Export Config").grid(row=0, column=1, padx=(0,5))
ttk.Button(bottom_frame, text="Launch Game").grid(row=0, column=2)



# Sets scrollregion once all widgets are added
scrollable_frame1.update_idletasks()
canvas1.configure(yscrollcommand=scrollbar1.set, scrollregion=canvas1.bbox("all"))
canvas2.configure(yscrollcommand=scrollbar2.set, scrollregion=canvas2.bbox("all"))


# Enable mousewheel scrolling anywhere in the Frame
def on_mousewheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

canvas1.bind_all("<MouseWheel>", on_mousewheel)

root.mainloop()
