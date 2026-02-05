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
        URL = "https://github.com/nathancblack/CPMA-Config-Tool/releases/latest/download/assets.zip"
        zip_path = Path(location) / "assets.zip"
        with requests.get(URL, stream=True) as r:
            with open(zip_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        shutil.unpack_archive(zip_path, location)
        os.remove(zip_path)
        self.data.paths["assets"] = str(Path(location) / "content")
        self.data.update_paths_json()

    def change_assets_location(self, destination: Path):
        self.data.update_paths_dict()
        shutil.move(self.data.paths["assets"], destination)
        self.data.paths["assets"] = str(Path(destination) / "Quake III Arena")
        # How to handle updating paths.json?
        # Call auto_select_paths() here or UI ?
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
