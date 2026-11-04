// SPDX-License-Identifier: GPL-3.0-or-later
/////////////////////////////////////////////////////////////////////////////////////////////////////
// Copyright (C) 2026 Emiliano Farías <efarias@iado-conicet.gob.ar>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.
/////////////////////////////////////////////////////////////////////////////////////////////////////

#ifndef UTILS_HPP
  #define UTILS_HPP
  #include <Arduino.h>
  #include "BluetoothSerial.h"
  #define GPS_UPDATE_IVAL_S 3
  
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  enum TimeSettingStatus{
  TS_NOT_SET,
  TS_WAITING_FOR_SECONDS,
  // TS_WAITING_FOR_TIMEZONE,
  TS_SET
  };
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  //------------------------------------------------------------------------------------------------
  void processReceivedStr(String& recvdStr);
  bool isItTimeNow();
  void waitForUserInput();
  // void printSpecialString(String& aStringM);
  void printSpecialCString(char* aStringM, bool hexM, bool oneMoreM);
  void assembleDataCStr(char* aCStringM,float temperatureM,float humidityM);
  void overwriteSpecialCString(char* aCStringM, uint8_t lengthM);
#endif