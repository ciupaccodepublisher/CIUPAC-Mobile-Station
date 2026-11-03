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

# TODO: Catch "qt.bluetooth.bluez: Cannot connect to profile/service."
# TODO: Code cleansing
# TODOs: * White background, Documents folder, connect to present device.
# Problems:
# * os.path.join evidentemente no es independiente del OS. Manda cadenas con /,\ o \\ mezcladas.
# * No logro que pyinstaller use el icono que esta en el subdir GUI, por eso esta duplicado en el root dir.
# * El programa guarda el config cfg en un directorio que se llama _internal o algo asi, en el directorio de instalacion.
# Pero luego no lo puede acceder por permisos de usuario, así que implica ejecutarlo como administrador. Hay que guardarlo en otro lugar.

# INFO: Debian:
# * qt6-base-dev-tools (used by Qt Designer)
# pyside6-tools (pyside6-uic)
# designer-qt6 (Qt Designer)
# python3-pyside6.qtcore python3-pyside6.qtwidgets python3-pyside6.qtbluetooth python3-nmea2

# cd /home/emilianof/.local/share/pipx/venvs/pyflowchart/
# ./bin/python3 ./lib/python3.13/site-packages/pyflowchart/ --output ~/tempo/example.html /home/emilianof/developing/MSDesktopPySide/CIUPAC-MS-Desktop.py


# INFO: PySide
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import (QIcon)
# from PySide6.QtCore import QFile
# if guiPresent:
from GUIMain import MainWindow
# import settings as settings
import sys, os
from lib.Utils import (SettingsContainer)

# ------------------------------------------------------------------------------------------------
mainScriptDirectory = os.path.dirname(__file__)
# ------------------------------------------------------------------------------------------------

config= SettingsContainer(mainScriptDirectory)
config.read()

app = QApplication(sys.argv)
iconFP= os.path.join(mainScriptDirectory, "GUI",'CIUPAC-MS-Desktop.ico')

app.setWindowIcon(QIcon(iconFP))

if config.guiPresent:
    window = MainWindow(config)
    window.show()
# INFO: This keeps window open. Why?
sys.exit(app.exec())
# ------------------------------------------------------------------------------------------------

