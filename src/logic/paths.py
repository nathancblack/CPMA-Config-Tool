import json
import os
import shutil
from pathlib import Path


class PathManager:
    def __init__(self, location=None):
        self.app_path = Path()
        self.paths = {
            "app_folder": self.app_path,
            "root_folder": "",
            "cpma_folder": "",
            "autoexec_cfg": "",
            "gui_cfg": "",
            "game_exe": "",
        }
        self._create_app_folder(location)

    def set_path(self, path_name: str, path: Path):
        self.paths[path_name] = str(path)
        with open(self.app_path / "paths.json", "w") as f:
            json.dump(self.paths, f)

    def get_path(self, path_name: str):
        with open(self.app_path / "paths.json", "r") as f:
            data = json.load(f)
            return Path(data.get(path_name))

    def handle_autoexec(self, autoexec_cfg_path: Path):
        if not os.path.exists(autoexec_cfg_path):
            open(autoexec_cfg_path, "x")

        with open(autoexec_cfg_path, "r+") as f:
            if "exec gui" not in f.read():
                f.write("\nexec gui")

    def _create_app_folder(self, location=None):
        path = location
        if path:
            path = Path(path) / "CPMA Config Tool"
            self.app_path = path
            if not os.path.exists(path):
                os.mkdir(path)
                print(path)
            else:
                print("Folder already exists")
        else:
            path = os.getenv("LOCALAPPDATA")
            if path:
                path = Path(path) / "CPMA Config Tool"
                self.app_path = path
                if not os.path.exists(path):
                    os.mkdir(path)
                    print(path)
                else:
                    print("Folder already exists")

            else:
                print("Could not find Local App Data")

    def auto_select_paths(self, root_folder: Path):
        missing = []
        cpma_folder = root_folder / "cpma"
        autoexec_cfg = cpma_folder / "autoexec.cfg"
        paths = {"cpma_folder": cpma_folder, "autoexec_cfg": autoexec_cfg}
        self.set_path("root_folder", root_folder)

        for path in paths:
            if os.path.exists(paths[path]):
                self.set_path(path, paths[path])
            else:
                missing.append(path)

        return missing

    def change_app_folder_path(self, new_path: Path):
        self.paths["app_folder"] = new_path

        with open(self.app_path / "paths.json", "w") as f:
            json.dump(self.paths, f)

        shutil.move(self.app_path, new_path)
        self.app_path = new_path

    def uninstall_all(self):
        os.remove(self.app_path)
