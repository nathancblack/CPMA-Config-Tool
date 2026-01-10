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

    def uninstall_assets(self):
        shutil.rmtree(Path(self.data.app_path / "content"))
