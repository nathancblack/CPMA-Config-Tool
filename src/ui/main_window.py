import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from pathlib import Path
import shutil

from src.logic.settings import ALL_SETTINGS
from src.logic.paths import PathManager
from src.logic.config_io import dict_to_cfg, cfg_to_dict

class ConfigApp:
    def __init__(self, root, path_manager, install_manager):
        self.root = root
        self.ALL_SETTINGS = ALL_SETTINGS           
        self.option_boxes = []
        self.frames = []
        self.canvases = []
        self.scrollbars = []
        self.scrollable_frames = []

        self.path_manager = path_manager
        self.install_manager = install_manager
        

        self.setup_ui()

    def setup_ui(self):
        self.root.title("CPMA Config Tool")
        self.root.geometry("800x600")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

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

        main_frame = ttk.Frame(self.root, padding=(10), style="white.TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)


        # ADVANCED SETTINGS WINDOW
        # (Method defined below as open_advanced_settings)


        # TOP FRAME
        top_frame = ttk.Frame(main_frame, padding=10, relief="ridge")
        top_frame.grid(row=0, column=0, sticky="nsew")
        top_frame.columnconfigure(0, weight=1)


        ttk.Label(
            top_frame,
            text="Settings with blank input boxes will default to the value in your current config"
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(top_frame, text="Advanced Settings", command=self.open_advanced_settings).grid(
            row=0, column=1, sticky="e"
        )


        # SETTINGS NOTEBOOK
        self.settings_notebook = ttk.Notebook(main_frame)
        self.settings_notebook.grid(row=1, column=0, sticky="nsew", pady=10)
        self.settings_notebook.columnconfigure(0, weight=1)

        # On tab change, set focus to the notebook itself instead of the first option_box
        self.settings_notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)


        # Generates notebook tab titles and contents
        # (frames, canvases, etc. initialized in __init__)

        for i, (title, dictionary) in enumerate(self.ALL_SETTINGS):
            frame = ttk.Frame(self.settings_notebook)
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
            self.frames.append(frame)
            self.settings_notebook.add(frame, text=title)

            canvas = tk.Canvas(self.frames[i], background=bg_color, highlightthickness=0)
            canvas.grid(row=0, column=0, sticky="nsew")
            self.canvases.append(canvas)

            scrollbar = ttk.Scrollbar(self.frames[i], orient="vertical", command=(self.canvases[i]).yview)
            scrollbar.grid(row=0, column=1, sticky="nse")
            self.scrollbars.append(scrollbar)

            scrollable_frame = ttk.Frame(self.canvases[i], padding=10)
            self.scrollable_frames.append(scrollable_frame)
            self.canvases[i].create_window((0, 0), window=self.scrollable_frames[i], anchor="nw")
            self.canvases[i].grid(padx=10, pady=(20, 10))

            # scrollable_frame widget generation
            for i2, setting in enumerate(dictionary):
                # generates each setting label
                label = ttk.Label(
                    self.scrollable_frames[i],
                    font=("TkDefaultFont", 10, "bold"),
                    text=dictionary[setting]["label"],
                )
                label.grid(row=(i2 * 2), column=0, sticky="w")

                # generates each setting description
                desc = ttk.Label(
                    self.scrollable_frames[i], text=dictionary[setting].get("description")
                )
                desc.grid(row=(i2 * 2), column=1, sticky="w", padx=(40, 0))

                # generates each setting option_box
                value = dictionary[setting]["value"]
                option_box = None
                
                if dictionary[setting].get("type") == "discrete":
                    option_box = ttk.Combobox(
                        self.scrollable_frames[i],
                        values=([""] + dictionary[setting]["options"]),
                        state="readonly",
                        width=22,
                    )
                    if value:
                        option_box.set(value)
                elif dictionary[setting].get("type") == "bool":
                    option_box = ttk.Combobox(self.scrollable_frames[i], values=["", "0", "1"], state="readonly", width=22)
                    if value:
                        option_box.set(value)
                elif dictionary[setting].get("type") == "float" or "string" or "int":
                    option_box = ttk.Entry(self.scrollable_frames[i], width=22)
                    if value:
                        option_box.insert(0, value)
                self.option_boxes.append((dictionary, setting, option_box))

                # add vertical padding to the option_box unless its the last option_box in a tab
                if i2 == len(dictionary) - 1:
                    option_box.grid(row=(i2 * 2) + 1, column=0, sticky="ew")
                else:
                    option_box.grid(row=(i2 * 2) + 1, column=0, sticky="ew", pady=(0, 20))

                # generates option_box range and default value for applicable settings
                if dictionary[setting].get("game_default"):
                    default = f"Default: {dictionary[setting].get('game_default')}"
                    if dictionary[setting].get("max"):
                        range_text = f"Range: {dictionary[setting].get('min')} to {dictionary[setting].get('max')}"
                        label2 = ttk.Label(self.scrollable_frames[i], text=f"{range_text} {default}")
                    else:
                        label2 = ttk.Label(self.scrollable_frames[i], text=default)
                    label2.grid(row=(i2 * 2) + 1, column=1, sticky="nw", padx=(40, 0))

        # BOTTOM FRAME
        bottom_frame = ttk.Frame(main_frame, style="white.TFrame")
        bottom_frame.grid(row=2, column=0, sticky="nsew")
        bottom_frame.columnconfigure(0, weight=1)

        left_frame = ttk.Frame(bottom_frame, style="white.TFrame")
        left_frame.grid(row=0, column=0, sticky="w")

        right_frame = ttk.Frame(bottom_frame, style="white.TFrame")
        right_frame.grid(row=0, column=1, sticky="e")

        ttk.Button(left_frame, text="Clear Inputs", command=self.clear_inputs).grid(row=0, column=0)
        ttk.Button(right_frame, text="Save Config", command=self.save_config).grid(
            row=0, column=0, padx=(0, 5)
        )
        ttk.Button(right_frame, text="Export Config", command=lambda: self.export_config("Export Config")).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(right_frame, text="Launch Game", command=self.launch_game).grid(row=0, column=2)


        # Sets scrollregion once all widgets are added
        for i, frame in enumerate(self.scrollable_frames):
            self.scrollable_frames[i].update_idletasks()
            self.canvases[i].configure(
                yscrollcommand=self.scrollbars[i].set, scrollregion=self.canvases[i].bbox("all")
            )

        # Allows the user to scroll anywhere in the canvas
        self.root.bind_all("<MouseWheel>", self.on_mousewheel)
        self.root.unbind_class("TScrollbar", "<MouseWheel>")

    def open_advanced_settings(self):
        advanced_settings = tk.Toplevel(self.root)
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
        ttk.Button(frame1, text="Change CPMA Location", command=self.change_cpma_location).grid(row=1, column=0, sticky="ew")

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

    def on_tab_change(self, event):
        self.settings_notebook.focus_set()

    def save_config(self):
        for group in self.option_boxes:
            dictionary, setting, option_box = group[0], group[1], group[2]
            if option_box.get() != "":
                dictionary[setting]["value"] = option_box.get()
                self.path_manager.set_path("gui_cfg", Path(self.path_manager.get_path("cpma_folder")/"gui.cfg"))
                dict_to_cfg(self.path_manager.get_path("gui_cfg"))
        messagebox.showinfo("Config Saved", "Your config has been saved.")

    def clear_inputs(self):
        if messagebox.askyesno("Clear All", "This will clear all entered values. Continue?"):
            for group in self.option_boxes:
                option_box = group[2]
                if type(option_box) == ttk.Combobox:
                    option_box.current(0)
                elif type(option_box) == ttk.Entry:
                    option_box.delete(0, "end")

    def launch_game(self):
        self.path_manager.launch_game()
    
    def export_config(self):
        raw_path = self.path_manager.get_path("gui_cfg")
        if not raw_path:
            print("The config has not been generated yet.")
            return

        selected_folder = filedialog.askdirectory(
            title="Export config",
            mustexist=True,
            initialdir="C:/Program Files (x86)",
        )
        if selected_folder:
                    try:
                        shutil.copy2(raw_path, selected_folder)
                        messagebox.showinfo("Success", f"Config exported to:\n{selected_folder}")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to export file: {e}")


    def change_cpma_location(self):
        raw_path = Path(self.install_manager.data.paths["assets"])
        if raw_path.exists:
            selected_folder = filedialog.askdirectory(
                title="Select new loaction for Q3 files",
                mustexist=True,
                initialdir="C:/Porgram Files (x86)",
            )
            if selected_folder:
                self.install_manager.change_assets_location(selected_folder)
            else:
                print("Could not find selected folder")
        else:
            print("Game assets do not exist")

    def on_mousewheel(self, event):
        current_tab = self.settings_notebook.index(self.settings_notebook.select())
        canvas = self.canvases[current_tab]
        # Only scroll if cavas is taller than visible area
        if canvas.bbox("all") and canvas.bbox("all")[3] > canvas.winfo_height():
            canvas.yview_scroll(-1 * (event.delta // 120), "units")
        return "break"
