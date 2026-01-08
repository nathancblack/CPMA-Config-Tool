import json
import os
from pathlib import Path


class PathManager:
    def __init__(self):
        self.paths = {
            "root_folder": "",
            "cpma_folder": "",
            "autoexec_cfg": "",
            "gui_cfg": "",
            "game_exe": "",
        }

        self._create_app_folder()

    def set_path(self, path_name: str, path: Path):
        self.paths[path_name] = str(path)
        with open("paths.json", "w") as f:
            json.dump(self.paths, f)

    def get_path(self, path_name: str):
        with open("paths.json", "r") as f:
            data = json.load(f)
            return Path(data.get(path_name))

    def handle_autoexec(self, path: Path):
        with open(path, "a") as f:
            f.write("exec gui")

    def _create_app_folder(self):
        path = os.getenv("LOCALAPPDATA")
        if path:
            path = Path(path) / "CPMA Config Tool"
            if not os.path.exists(path):
                os.mkdir(path)
                print(path)
            else:
                print("Folder already exists")
        else:
            print("Could not find Local App Data")


path_manager = PathManager()
# path_manager._create_app_folder()
