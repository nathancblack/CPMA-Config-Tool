import json
import os
import shutil
from pathlib import Path

import requests


class InstallManager:
    def __init__(self, path_manager):
        self.data = path_manager

    def install_assets(self):
        URL = "https://github.com/nathancblack/CPMA-Config-Tool/releases/latest/download/assets.zip"
        zip_path = self.data.app_path / "assets.zip"
        with requests.get(URL, stream=True) as r:
            with open(zip_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        shutil.unpack_archive(zip_path, self.data.app_path)
        os.remove(zip_path)
        self.data.paths["assets"] = str(Path(self.data.app_path / "content"))
        with open(self.data.app_path / "paths.json", "w") as f:
            json.dump(self.data.paths, f)

    def uninstall_assets(self):
        shutil.rmtree(Path(self.data.app_path / "content"))

    def test(self):
        print(self.data.paths)
