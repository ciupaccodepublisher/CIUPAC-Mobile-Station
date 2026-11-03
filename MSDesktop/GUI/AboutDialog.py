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

# INFO: This dialog displays the "Appropriate Legal Notices" required by section 5(d)
# of the GNU GPL v3: copyright notice, absence of warranty, the fact that the program
# may be conveyed under the GPL, and a way to read the license text.

import os

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (QDialog,
                               QDialogButtonBox,
                               QLabel,
                               QPlainTextEdit,
                               QPushButton,
                               QTabWidget,
                               QVBoxLayout)

APP_NAME= "MobileStationDesktop"
LICENSES_URL= "https://www.gnu.org/licenses/"
# ------------------------------------------------------------------------------------------------
def getProjectRootDirectory():
    # GUI/AboutDialog.py -> project root (same place where config.cfg and LICENSE.txt live,
    # both when running from source and when packaged with PyInstaller).
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ------------------------------------------------------------------------------------------------
def readTextFile(fullPath:str):
    try:
        with open(fullPath, "r", encoding="utf-8", errors="replace") as aFile:
            return aFile.read()
    except OSError:
        return (f"File not found: {os.path.basename(fullPath)}\n\n"
                f"The license texts are available at {LICENSES_URL}")
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LicenseViewerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Licenses")
        self.resize(760, 560)

        rootDir= getProjectRootDirectory()
        entries= [("License (GPLv3)", os.path.join(rootDir, "LICENSE.txt")),
                  ("Third-party credits", os.path.join(rootDir, "CREDITS.md"))]
        licensesDir= os.path.join(rootDir, "LICENSES")
        if os.path.isdir(licensesDir):
            for fileName in sorted(os.listdir(licensesDir)):
                entries.append((os.path.splitext(fileName)[0],
                                os.path.join(licensesDir, fileName)))

        fixedFont= QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        tabs= QTabWidget(self)
        for title, fullPath in entries:
            textView= QPlainTextEdit(self)
            textView.setReadOnly(True)
            textView.setFont(fixedFont)
            textView.setPlainText(readTextFile(fullPath))
            tabs.addTab(textView, title)

        buttons= QDialogButtonBox(QDialogButtonBox.StandardButton.Close, self)
        buttons.rejected.connect(self.reject)

        layout= QVBoxLayout(self)
        layout.addWidget(tabs)
        layout.addWidget(buttons)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"About {APP_NAME}")

        noticeLbl= QLabel(self)
        noticeLbl.setWordWrap(True)
        noticeLbl.setOpenExternalLinks(True)
        noticeLbl.setText(
            f"<h3>{APP_NAME}</h3>"
            "<p>Copyright &copy; 2026 Emiliano Far&iacute;as</p>"
            "<p>This program comes with <b>ABSOLUTELY NO WARRANTY</b>.</p>"
            "<p>This is free software: you can redistribute it and/or modify it under the "
            "terms of the GNU General Public License as published by the Free Software "
            "Foundation, either version 3 of the License, or (at your option) any later "
            "version.</p>"
            f"<p>See <a href=\"{LICENSES_URL}\">{LICENSES_URL}</a> or use the button below "
            "to read the full license text and the licenses of third-party components.</p>")

        buttons= QDialogButtonBox(QDialogButtonBox.StandardButton.Close, self)
        viewLicensesBtn= QPushButton("View licenses...", self)
        buttons.addButton(viewLicensesBtn, QDialogButtonBox.ButtonRole.ActionRole)
        viewLicensesBtn.clicked.connect(self.viewLicensesSlot)
        buttons.rejected.connect(self.reject)

        layout= QVBoxLayout(self)
        layout.addWidget(noticeLbl)
        layout.addWidget(buttons)
        self.setMinimumWidth(460)
    # ------------------------------------------------------------------------------------------------
    def viewLicensesSlot(self):
        LicenseViewerDialog(self).exec()
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
