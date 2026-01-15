from pathlib import Path

from src.logic.installer import InstallManager
from src.logic.paths import PathManager

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

autoexec_cfg_path = Path(
    "C:\\Users\\natha\\Programming Projects\\CPMA-Config-Tool\\assets\\q3\\cpma\\autoexec.cfg"
)

game_exe_path = Path(
    "C:\\Users\\natha\\Programming Projects\\CPMA-Config-Tool\\assets\\q3\\cnq3-x64.exe"
)


def main():
    path_manager = PathManager(project_assets_windows)
    install_manager = InstallManager(path_manager)

    path_manager.paths["game_exe"] = str(game_exe_path)
    path_manager.update_paths_json()
    path_manager.launch_game()
    # path_manager.auto_select_paths(root_folder_path_windows)
    # install_manager.install_assets(project_assets_windows)

    # install_manager.uninstall_assets()

    # install_manager.uninstall_all()

    # install_manager.change_assets_location(Path(project_assets_windows / "new"))


main()
