import sys
import tkinter as tk
from pathlib import Path

# Allow running directly as `python src/logic/main.py` by putting the
# project root on sys.path before importing the `src` package.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.logic.installer import InstallManager
from src.logic.paths import PathManager
from src.ui.main_window import ConfigApp


def main():
    path_manager = PathManager()
    install_manager = InstallManager(path_manager)
    root = tk.Tk()
    ConfigApp(root, path_manager, install_manager)
    root.mainloop()


if __name__ == "__main__":
    main()
