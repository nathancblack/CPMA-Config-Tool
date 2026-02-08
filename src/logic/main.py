from pathlib import Path
import tkinter as tk
from src.logic.installer import InstallManager
from src.logic.paths import PathManager
from src.ui.main_window import ConfigApp 

root_folder_path_windows = Path(
    "C:/Users/natha/Programming Projects/CPMA-Config-Tool/assets/q3"
)

project_assets_windows = Path(
    "C:\\Users\\natha\\Programming Projects\\CPMA-Config-Tool\\assets"
)

project_assets_mac = Path(
    "/Users/nate/Programming/CPMA Config Tool/CPMA-Config-Tool/assets/"
)

root_folder_path_mac = Path(
    "/Users/nate/Programming/CPMA Config Tool/CPMA-Config-Tool/assets/Quake III Arena"
)

game_exe_path = Path(
    "C:\\Users\\docker\\Desktop\\Shared\\CPMA-Config-Tool\\assets\\Quake III Arena\\cnq3-x64.exe"
)

root_path_linux = Path(
    "C:\\Users\\docker\\Desktop\\Shared\\CPMA-Config-Tool\\assets\\Quake III Arena"
)

def main():
    path_manager = PathManager(project_assets_windows)
    install_manager = InstallManager(path_manager)
    path_manager.auto_select_paths(root_path_linux)
    path_manager.set_path("assets", root_path_linux) 
    path_manager.set_path("game_exe", game_exe_path)
    root = tk.Tk()
    app = ConfigApp(root, path_manager, install_manager)
    root.mainloop()
        

main()
