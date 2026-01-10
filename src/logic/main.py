from pathlib import Path

from installer import install_assets
from paths import PathManager


def main():
    path_manager = PathManager()

    root_folder_path = Path(
        "C:/Users/natha/Programming Projects/CPMA-Config-Tool/assets/q3"
    )

    autoexec_cfg_path = Path(
        "C:\\Users\\natha\\Programming Projects\\CPMA-Config-Tool\\assets\\q3\\cpma\\autoexec.cfg"
    )

    path_manager.auto_select_paths(root_folder_path)

    install_assets(path_manager.app_path)

    # install_manager.uninstall_assets()


main()
