from cx_Freeze import setup, Executable
import sys

build_exe_options = {
    "packages": ["pygame", "matplotlib", "numpy", "Pillow", "os", "sys", "json", "random", "datetime", "io"],
    "include_files": [
        "assets/",
        "data/",
        "saves/",
        "systems/",
        "ui/"
    ],
    "excludes": ["tkinter", "test"],
    "optimize": 2
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="FootballManager",
    version="1.0",
    description="FOOTYSUPER⁵: LEGENDARY EDITION - Football Career Manager",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, icon="assets/images/icon.ico")]
)