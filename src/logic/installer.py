import os
import shutil
from pathlib import Path

import requests


def install_assets(destination: Path):
    URL = "https://github.com/nathancblack/CPMA-Config-Tool/releases/latest/download/assets.zip"
    zip_path = destination / "assets.zip"
    with requests.get(URL, stream=True) as r:
        with open(zip_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    shutil.unpack_archive(zip_path, destination)
    os.remove(zip_path)


def uninstall_assets():
    os.remove(Path())
