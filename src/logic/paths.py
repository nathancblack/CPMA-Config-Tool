import json
import os
import subprocess
import sys
from pathlib import Path


class PathManager:
    def __init__(self, location=None):
        self.app_path = Path()
        self.paths = {
            "root_folder": "",
            "cpma_folder": "",
            "autoexec_cfg": "",
            "gui_cfg": "",
            "game_exe": "",
            "assets": "",
        }
        self._create_app_folder()
         
        if (self.app_path / "paths.json").exists():
            try:
                with open(self.app_path / "paths.json", "r") as f:
                    saved_data = json.load(f)
                    self.paths.update(saved_data)
                    print("Loaded existing paths from paths.json")
            except (json.JSONDecodeError, OSError):
                print("Error loading JSON, starting with defaults.")
        
        self.update_paths_json()

    def is_configured(self):
        root = self.paths.get("root_folder", "")
        return root != "" and os.path.exists(root)

    def set_path(self, path_name: str, path: Path):
        self.paths[path_name] = str(path)
        self.update_paths_json()

    def get_path(self, path_name: str):
        self.update_paths_dict()
        value = self.paths.get(path_name, "")
        if value:
            return Path(value)
        return None

    def update_paths_json(self):
        with open(self.app_path / "paths.json", "w") as f:
            json.dump(self.paths, f)

    def update_paths_dict(self):
        with open(self.app_path / "paths.json", "r") as f:
            self.paths.update(json.load(f))

    def handle_autoexec(self, autoexec_cfg_path: Path):
        if not os.path.exists(autoexec_cfg_path):
            open(autoexec_cfg_path, "x")

        with open(autoexec_cfg_path, "r+") as f:
            if "exec gui" not in f.read():
                f.write("\nexec gui")

    def _create_app_folder(self):
        if sys.platform == "win32":
            base = os.getenv("LOCALAPPDATA") or os.path.expanduser("~")
        elif sys.platform == "darwin":
            base = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
        else:
            base = os.getenv("XDG_DATA_HOME") or os.path.join(
                os.path.expanduser("~"), ".local", "share"
            )

        self.app_path = Path(base) / "CPMA Config Tool"
        self.app_path.mkdir(parents=True, exist_ok=True)

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

    def launch_game(self):
        self.update_paths_dict()
        exe = self.paths.get("game_exe", "")
        if not exe or not os.path.exists(exe):
            return False
        # Run from the game directory so Quake can locate its files.
        subprocess.Popen([exe], cwd=str(Path(exe).parent))
        return True
