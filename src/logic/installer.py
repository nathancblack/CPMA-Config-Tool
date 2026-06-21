import os
import shutil
from pathlib import Path

import requests


class InstallManager:
    def __init__(self, path_manager):
        self.data = path_manager

    def install_assets(self, location=None):
        if location is None:
            location = self.data.app_path  # Install to local app data by default
        URL = "https://github.com/nathancblack/CPMA-Config-Tool/releases/latest/download/Q3.zip"
        zip_path = Path(location) / "Q3.zip"
        with requests.get(URL, stream=True) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        shutil.unpack_archive(zip_path, location)
        os.remove(zip_path)
        game_root = Path(location) / "Q3"
        self.data.paths["assets"] = str(game_root)
        self.data.auto_select_paths(game_root)
        self.data.paths["game_exe"] = str(game_root / "cnq3-x64.exe")
        self.data.update_paths_json()

    def change_assets_location(self, destination: Path):
        self.data.update_paths_dict()
        shutil.move(self.data.paths["assets"], destination)
        game_root = Path(destination) / "Q3"
        self.data.paths["assets"] = str(game_root)
        self.data.auto_select_paths(game_root)
        self.data.paths["game_exe"] = str(game_root / "cnq3-x64.exe")
        self.data.update_paths_json()

    def uninstall_assets(self):
        self.data.update_paths_dict()
        shutil.rmtree(Path(self.data.paths["assets"]))
        self.data.paths["assets"] = ""
        self.data.update_paths_json()

    def uninstall_all(self):
        #self.uninstall_assets()
        #print("Uninstalled assets")

        if os.path.exists(self.data.app_path):
            shutil.rmtree(self.data.app_path)
            print("Uninstalled CPMA Config Tool Folder")
        else:
            print("Folder was already deleted or does not exist.")
