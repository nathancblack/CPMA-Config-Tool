from pathlib import Path

from installer import InstallManager
from paths import PathManager

root_folder_path = Path(
    "C:/Users/natha/Programming Projects/CPMA-Config-Tool/assets/q3"
)

autoexec_cfg_path = Path(
    "C:\\Users\\natha\\Programming Projects\\CPMA-Config-Tool\\assets\\q3\\cpma\\autoexec.cfg"
)


def main():
    path_manager = PathManager()
    install_manager = InstallManager(path_manager)

    path_manager.auto_select_paths(root_folder_path)
    # install_manager.install_assets()

    install_manager.uninstall_assets()


main()
