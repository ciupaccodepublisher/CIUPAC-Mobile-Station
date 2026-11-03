# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
#####################################################################################################
# Copyright (C) 2026 Emiliano Farías <efarias@iado-conicet.gob.ar>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://gnu.org>.
#####################################################################################################

# INFO: Development tool. It is NOT imported by the application nor packaged by PyInstaller.
#
# Generates GUI/<name>.py from GUI/<name>.ui using pyside6-uic and puts the project's
# licensing header at the top of every generated file (pyside6-uic would otherwise
# produce files without it, and any previous header is lost each time they are regenerated).
#
# Usage (from the project root directory):
#   python generateUiFiles.py                    # every GUI/*.ui
#   python generateUiFiles.py GUI/MainScreen.ui # only the given file(s)
#   python generateUiFiles.py --uic /path/to/pyside6-uic

import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile

HEADER= """# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
#####################################################################################################
# Copyright (C) 2026 Emiliano Farías <efarias@iado-conicet.gob.ar>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://gnu.org>.
#####################################################################################################

"""
CODING_LINE= "# -*- coding: utf-8 -*-"
# ------------------------------------------------------------------------------------------------
def generateOne(uicCmd:str, uiPath:str):
    pyPath= os.path.splitext(uiPath)[0] + ".py"
    with tempfile.TemporaryDirectory() as tmpDir:
        tmpOut= os.path.join(tmpDir, "generated.py")
        result= subprocess.run([uicCmd, uiPath, "-o", tmpOut],
                               capture_output=True, text=True)
        if result.returncode != 0 or not os.path.isfile(tmpOut):
            raise RuntimeError(f"pyside6-uic failed for {uiPath}:\n{result.stderr or result.stdout}")
        with open(tmpOut, "r", encoding="utf-8", newline="") as aFile:
            generated= aFile.read()

    # The generated file usually starts with its own coding line: keep only one.
    if generated.startswith(CODING_LINE):
        generated= generated[len(CODING_LINE):].lstrip("\r\n")
    if "SPDX-License-Identifier" in generated:
        raise RuntimeError(f"Unexpected SPDX line already present in the output for {uiPath}")

    with open(pyPath, "w", encoding="utf-8", newline="\n") as aFile:
        aFile.write(HEADER + generated)
    print(f"Generated {pyPath}")
# ------------------------------------------------------------------------------------------------
def main():
    parser= argparse.ArgumentParser(description="Generate GUI .py files from .ui files, adding the licensing header.")
    parser.add_argument("uiFiles", nargs="*", help="Qt Designer files (default: every GUI/*.ui)")
    parser.add_argument("--uic", default=None, help="Path to the pyside6-uic executable")
    args= parser.parse_args()

    rootDir= os.path.dirname(os.path.abspath(__file__))
    uicCmd= args.uic or shutil.which("pyside6-uic")
    if not uicCmd:
        sys.exit("pyside6-uic not found. Install PySide6 tools or pass --uic /path/to/pyside6-uic")

    uiFiles= args.uiFiles or sorted(glob.glob(os.path.join(rootDir, "GUI", "*.ui")))
    if not uiFiles:
        sys.exit("No .ui files found.")
    for uiPath in uiFiles:
        generateOne(uicCmd, uiPath)
# ------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
