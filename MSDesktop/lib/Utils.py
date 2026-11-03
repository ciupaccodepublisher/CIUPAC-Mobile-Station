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

import pynmea2
from datetime import datetime, timezone
import os
from .AknSettingsFileUtilities2602 import (SettingsFileIO)
from enum import Enum
import platform
from PySide6.QtCore import (QDir)
#####################################################################################################
class RecordMessageType(Enum):
    GPGGA_CLIMATE = 0
    ISOTIME_DECPOS_CLIMATE = 1
#####################################################################################################
class SettingsContainer:
    def __init__(self, mainScriptDirectory):
        self.configFileFullPath= os.path.join(mainScriptDirectory, 'config.cfg')
        self.configFileManager= SettingsFileIO(self.configFileFullPath)
    # ------------------------------------------------------------------------------------------------
    def read(self):
        self.configRead= True
        
        try:
            self.__settingsDict= self.configFileManager.loadSettingsDictFromFile()
        except:
            self.configRead= False

        if self.configRead:
            self.guiPresent= self.__settingsDict['guiPresent']=="True"
            self.btPresent= self.__settingsDict['btPresent']=="True"
            self.btConnectionWatchdogIvalS= int(self.__settingsDict['btConnectionWatchdogIvalS'])
            self.testing= self.__settingsDict['testing']=="True"
            self.testingWDIntervalS= int(self.__settingsDict['testingWDIntervalS'])
            self.consoleOutputEnabled= self.__settingsDict['consoleOutputEnabled']=="True"

            if self.__settingsDict['recordLineType']=="ISOTIME_DECPOS_CLIMATE":
                self.recordLineType= RecordMessageType.ISOTIME_DECPOS_CLIMATE
            else:
                self.recordLineType= RecordMessageType.GPGGA_CLIMATE

            try:
                self.storageDirectory= self.__settingsDict['storageDirectory']
            except:
                parentPath= QDir.homePath()
                if platform.system()== "Linux":
                    relativeStoragePath= os.path.join("Documents","CIUPACMobileStation")
                else:
                    relativeStoragePath= os.path.join("My Documents","CIUPACMobileStation")
                self.storageDirectory= os.path.join(parentPath,relativeStoragePath)

            storageFPPQdir= QDir(self.storageDirectory)
            if not storageFPPQdir.exists():
                storageFPPQdir.mkdir(storageFPPQdir.absolutePath())
            if self.consoleOutputEnabled:
                print(f"self.storageDirectory: {self.storageDirectory}")
    # ------------------------------------------------------------------------------------------------
    def save(self):
        if self.configRead:
            self.__settingsDict['guiPresent']= self.guiPresent
            self.__settingsDict['btPresent']= self.btPresent
            self.__settingsDict['btConnectionWatchdogIvalS']= self.btConnectionWatchdogIvalS
            self.__settingsDict['testing']= self.testing
            self.__settingsDict['testingWDIntervalS']= self.testingWDIntervalS
            self.__settingsDict['consoleOutputEnabled']= self.consoleOutputEnabled

            if self.recordLineType==RecordMessageType.ISOTIME_DECPOS_CLIMATE:
                self.__settingsDict['recordLineType']= "ISOTIME_DECPOS_CLIMATE"
            else:
                self.__settingsDict['recordLineType']= "GPGGA_CLIMATE"

            self.__settingsDict['storageDirectory']= self.storageDirectory

            self.configFileManager.saveSettingsDictToFile(self.__settingsDict)
#####################################################################################################
class IntervalCounter():
    def __init__(self,ticksPerPulseM:int,pulseAtFirstCheckM:bool):
        self.ticksPerPulse= ticksPerPulseM
        # If pulseAtFirstCheckM == true, first call to "cac" routines will return true.
        if (pulseAtFirstCheckM):
            self.counter= self.ticksPerPulse-1
        else:
            self.counter= 0
    # ----------------------------------------------------------------------------------------------------------
    def checkAndClear(self)->bool:
        self.counter+=1
        if self.counter >= self.ticksPerPulse:
            self.counter=0
            return True
        else:
            return False
    # ----------------------------------------------------------------------------------------------------------
    def reset(self):
        self.counter=0
#####################################################################################################
class StationMsgManager():
    # TODO: Keep coding this class
    def __init__(self,configF:SettingsContainer):
        self.config= configF
        self.__isFirstMsg= True
    # ----------------------------------------------------------------------------------------------------------
    def beginOfNewSeries(self):
        self.__isFirstMsg= True
    # ----------------------------------------------------------------------------------------------------------
    def processMsg(self, msgM:str):
        self.__msg= msgM
        self.isAValidMsg= False
        # __gpggaMsgsLst=[]
        if self.__msg.startswith("$GPGGA"):
            __gpggaMsgsLst= self.__msg.split("$")
            # This means we've got more that one GPGGA msg in received string
            # Just one is used. This should never happen anyways.
            if len(__gpggaMsgsLst)>2:
                if self.config.consoleOutputEnabled:
                    print("TOO MANY data msgs per packet!")
            __gpggaMsg= "$"+__gpggaMsgsLst[1]
            __gpggaStrLst= __gpggaMsg.split(",")
            self.temperature= __gpggaStrLst[-2]
            self.humidity= __gpggaStrLst[-1]
            # Removing last two elements in list (temp and humidity)
            __gpggaStrLst= __gpggaStrLst[:-2]
            # Creating a string with values of list separated by commas.
            self.gpggaStr= ','.join(__gpggaStrLst)

            # Trying to get "raise ChecksumError(pynmea2.nmea.ChecksumError: ('checksum does not match:"
            # caught and ignore that packet
            try:
                # NMEASentence format / structure at top of this file.
                self.nmeaObj = pynmea2.parse(self.gpggaStr)
            except pynmea2.ChecksumError:
                if self.config.consoleOutputEnabled:
                    print("Checksum error.")
            except pynmea2.ParseError:
                if self.config.consoleOutputEnabled:
                    print("Unparseable msg.")
            else:
                __gpsQuality= int(self.nmeaObj.gps_qual)
                if self.config.consoleOutputEnabled:
                    satsQty= int(self.nmeaObj.num_sats)
                    print("Sats number: %d, GPS quality: %f\n" % (satsQty,__gpsQuality))
                if __gpsQuality > 0:
                    self.isAValidMsg= True
                    if self.__isFirstMsg:
                        # datetime.today().strftime('%Y-%m-%d')
                        # self.__currentDate = datetime.date.now(timezone.utc).isoformat()
                        self.__currentDateStr= datetime.now(timezone.utc).date().isoformat()
                        self.__previousMsgTimeStamp= self.nmeaObj.timestamp
                        self.__isFirstMsg= False
                else:
                    if self.config.consoleOutputEnabled:
                        print("Bad quality")
    # ----------------------------------------------------------------------------------------------------------
    def getRecordString(self):
        if self.config.recordLineType == RecordMessageType.GPGGA_CLIMATE:
            __returnStr= self.__msg
        elif self.config.recordLineType == RecordMessageType.ISOTIME_DECPOS_CLIMATE:
            __ggaTimestamp= self.nmeaObj.timestamp
            # It means there was a 00:00 crossing, date must be updated.
            if __ggaTimestamp < self.__previousMsgTimeStamp:
                self.__currentDateStr= datetime.now(timezone.utc).date().isoformat()
            self.__previousMsgTimeStamp= __ggaTimestamp
            __returnStr= self.__currentDateStr+"T"+self.nmeaObj.timestamp.isoformat()
            __returnStr= __returnStr+","+str(self.nmeaObj.latitude)+","+str(self.nmeaObj.longitude)
            __returnStr= __returnStr+","+str(self.temperature)+","+str(self.humidity)
        return __returnStr+"\r\n"
#####################################################################################################
class FileReader():
    def __init__(self,filePath:str,storedCSVM:bool=False):
        self.__isAStoredCSV= storedCSVM
        fileDescriptor = open(filePath, 'r')
        self.fileLines = fileDescriptor.readlines()
        fileDescriptor.close()
        self.linesIter= iter(self.fileLines)
    # ----------------------------------------------------------------------------------------------------------
    def getNextLine(self)->str:
        noNMEALine= True
        while noNMEALine:
            aLine= next(self.linesIter)
            if aLine.startswith("$"):
                noNMEALine= False
        return aLine.strip()
    # # ----------------------------------------------------------------------------------------------------------
#####################################################################################################
