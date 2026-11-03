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

import os
# ------------------------------------------------------------------------------------------------
class SettingsFileIO:
    def __init__(self, settingsFileFullPath):
        self.settingsFileFullPath= settingsFileFullPath

    # Load key-value pairs from a settings file, ignoring lines consisting
    # of just newlines and comments (lines starting with "#" character.
    def loadSettingsDictFromFile(self):
        settings = {}
        with open(self.settingsFileFullPath) as f:
            for line in f:
                cleanLine= line.strip()
                if cleanLine == "":
                    continue
                if cleanLine.split("#")[0]=="":
                    continue
                key, value = cleanLine.split("=")
                settings[key.strip()] = value.strip()
        return settings
    # ------------------------------------------------------------------------------------------------
    # Saves key-value pairs of a dict into settings file.
    # Only keys that exist in settings file are overwritten.
    # Comments and empty lines are preserved.
    def saveSettingsDictToFile(self, settingsDict):
        savedKeys= set()
        # First we load config file in memory, as list of lines.
        # The most robust way to use readlines() is with a with statement,
        # which ensures the file is automatically closed after its contents are read
        with open(self.settingsFileFullPath, 'r') as file:
            linesList = file.readlines()
        for k in range(len(linesList)):
                line= linesList[k]
                cleanLine= line.strip()
                # If it is a comment or just a newline, we skip it.
                if cleanLine == "":
                    continue
                if cleanLine.split("#")[0]=="":
                    continue
                # Otherwise:
                key, value = cleanLine.split("=")
                key= key.strip()
                # We search for the value of the key (in our program settings)
                # and replace the corresponding line of the line list.
                line= f"{key} = {settingsDict[key]}\n"
                linesList[k]= line
                savedKeys.add(key)

        # Keys not present in settings file are appended at the end of settings file.
        for key in settingsDict:
            if key not in savedKeys:
                line= f"{key} = {settingsDict[key]}\n"
                linesList.append(line)

        # Finally, we write the lines list to file
        try:
            with open(self.settingsFileFullPath, "w") as file:
                file.writelines(linesList)
        except:
                pass
        # DAD
        # except IOError as e:
            # print(f"Error handling file: {e}")
# ##########################################################################################
