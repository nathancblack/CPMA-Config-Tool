import re
from pathlib import Path

from settings import (
    AUDIO_SETTINGS,
    HUD_SETTINGS,
    KEYBIND_SETTINGS,
    MOUSE_SETTINGS,
    PLAYER_SETTINGS,
    VIDEO_SETTINGS,
    WEAPON_SETTINGS,
)

SETTINGS = [
    MOUSE_SETTINGS,
    VIDEO_SETTINGS,
    AUDIO_SETTINGS,
    HUD_SETTINGS,
    PLAYER_SETTINGS,
    WEAPON_SETTINGS,
    KEYBIND_SETTINGS,
]


def dict_to_cfg(gui_path: Path):
    with open(gui_path, "w") as f:
        for group in SETTINGS:
            for setting, value in group.items():
                if group != KEYBIND_SETTINGS and value["value"] is not None:
                    f.write(f'seta {setting} "{value["value"]}"\n')
                elif group == KEYBIND_SETTINGS and value["value"] is not None:
                    f.write(f'bind {value["value"]} "{setting}"\n')


def cfg_to_dict(gui_path: Path):
    with open(gui_path) as f:
        text = f.read()

        seta_dict = {}
        bind_dict = {}
        seta_matches = re.findall(r'seta\s+(\w+)\s+"(.*?)"', text)
        bind_matches = re.findall(r'bind\s+(\S+)\s+"(.*?)"', text)
        # print(f"Seta matches: {seta_matches}")
        # print(f"Bind matches: {bind_matches}")
        for setting, value in seta_matches:
            seta_dict[setting] = value

        for value, setting in bind_matches:
            bind_dict[setting] = value

        for group in SETTINGS:
            for setting, value in group.items():
                if setting in seta_dict.keys() and group != KEYBIND_SETTINGS:
                    value["value"] = seta_dict[setting]
                if setting in bind_dict and group == KEYBIND_SETTINGS:
                    value["value"] = bind_dict[setting]


# Testing functions
def test_read_write():
    gui_cfg = Path(
        "C:\\Users\\natha\\Programming Projects\\CPMA-Config-Tool\\assets\\q3\\cpma\\gui.cfg"
    )
    test_path = Path(
        "C:\\Users\\natha\\Programming Projects\\CPMA-Config-Tool\\src\\logic\\test.cfg"
    )
    cfg_to_dict(gui_cfg)
    dict_to_cfg(test_path)


test_read_write()


def see_dict_values():
    for group in SETTINGS:
        for setting in group.items():
            print(setting)


# see_dict_values()
