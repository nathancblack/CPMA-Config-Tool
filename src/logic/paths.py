import json
from pathlib import Path


class PathsManager:
    def __init__(self):
        self.paths = {
            "root_folder": "",
            "cpma_folder": "",
            "autoexec_cfg": "",
            "gui_cfg": "",
            "game_exe": "",
        }

    def set_path(self, path_name: str, path: Path):
        self.paths[path_name] = str(path)
        with open("paths.json", "w") as f:
            json.dump(self.paths, f)


path_manager = PathsManager()
path_manager.set_path("root_folder", Path("LWALKSDLKASN"))
path_manager.set_path("cpma_folder", Path("Something"))
